import ROOT
import pandas as pd
import time
import os
                             #filename, column_name,column_name,scale,scale2, hist_name, hist_title, nbins, xmin1, xmax1,lw_cut1
def create_and_fill_histogram(filename, column_name,ref_column_name,scale,ref_scale, hist_name, hist_title, nbins, xmin, xmax,lw_cut):

    try:
        df = pd.read_csv(filename)
        print(df)  # Use pandas for efficient CSV reading
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{filename}' is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: Could not parse file '{filename}'. Check the format.")
        return None
    except Exception as e: # Catch any other potential Pandas exception
        print(f"An error occurred while reading the file: {e}")
        return None

    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in the file.")
        return None

    hist = ROOT.TH1F(hist_name, hist_title, nbins, xmin, xmax)

    for value1,value2 in zip(df[column_name]*scale,df[ref_column_name]*ref_scale):
       # print(value)
        if float(value2)>lw_cut:
            hist.Fill(value1)
    
    return hist,len(df)



def update_histogram(df_new,last_size, column_name,ref_column_name, scale,ref_scale,hist,lw_cut):

    if column_name not in df_new.columns:
        print(f"Error: Column '{column_name}' not found in the updated file.")
        return False
    chkp=False
    try:
        new_data = df_new.iloc[last_size:]
        #print(new_data)
        for value1,value2 in zip(new_data[column_name]*scale,new_data[ref_column_name]*ref_scale):
            if  float(value2)>lw_cut:
                hist.Fill(value1)
                chkp=True
        if(chkp==True):
            return True
        else:
            return False
    
    except Exception as e:
        print(f"Error during efficient update: {e}")
        # Fallback to less efficient but more robust update if the above fails:
        print("Falling back to full file re-read for update.")
        hist.Reset() # Clear the histogram
        for value1,value2 in zip(new_data[column_name]*scale,new_data[ref_column_name]*ref_scale):
            if  float(value2)>lw_cut:
                hist.Fill(value1)
        return True # Even if fallback is used, we consider it a success.



# Example usage:

filename = "triggered_measurements_CO60_TH_20mV.csv" # Replace with your file name
column_name = "Vpp_mV"  
column_name2 = "Area_V_ns"      # Replace with the column you want to histogram
hist_name = "Peak To Peak voltage mV"
hist_name2 = "Pulse Area nVs"
scale=1000
scale2=-1e9
lw_cut1=50.
lw_cut2=12.0


hist_title = "Distribution of Vpp (mV)"
hist_title2 = "Distribution of Area (nVs)"

nbins = 1200
xmin1 = 0       # Set appropriate min and max values
xmax1 = 5500   

nbins2=480
xmin2 = 0       # Set appropriate min and max values
xmax2 = 480   


# Initial histogram creation:
hist1,last_size = create_and_fill_histogram(filename, column_name,column_name,scale,scale, hist_name, hist_title, nbins, xmin1, xmax1,lw_cut1)

hist2,last_size2= create_and_fill_histogram(filename, column_name2,column_name, scale2,scale,hist_name2, hist_title2, nbins2, xmin2, xmax2,lw_cut1)

c = ROOT.TCanvas("c1", "Canvas", 800, 600)
c.Divide(2,1)

if hist1: # Only proceed if the initial histogram was created successfully
    c.cd(1)
    hist1.Draw()
    c.Update()

if hist2:
    c.cd(2)
    hist2.Draw()    
    c.Update()

    while True: # Update loop
        time.sleep(0.02)  # Check for updates every 5 seconds (adjust as needed)
        if os.path.exists(filename): # Check file exists before attempting to update
            
            data = pd.read_csv(filename)
            if len(data) > last_size:
            #    new_data = data.iloc[last_size:]  # Get the new rows added
            # Process or plot the new rows
            # column_name,ref_column_name, scale,ref_scale
                if update_histogram(data,last_size, column_name,column_name,scale,scale, hist1,lw_cut1):
                    c.cd(1)
                    hist1.Draw() # Redraw the histogram
                    c.Update()  # Update the canvas
                    print("Height Histogram updated.")
                if update_histogram(data,last_size2, column_name2,column_name,scale2,scale, hist2,lw_cut1):
                    c.cd(2)
                    hist2.Draw() # Redraw the histogram
                    c.Update()  # Update the canvas
                    print("Area Histogram updated.")
                
                
                last_size = len(data) 
                last_size2 = len(data) 
            
            
            
            
            else:
                pass
               # print("Wait.")
        else:
            print("File not found, exiting.")
            break # Exit loop if file is no longer present

    input("Press Enter to exit.") # Keep the canvas open until the user presses Enter
