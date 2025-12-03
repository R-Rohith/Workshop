import pyvisa
import time
import csv
from datetime import datetime

# Configuration
RESOURCE_ADDRESS = 'TCPIP0::192.16.13.181::INSTR' # Replace with your scope's address
CHANNEL = 'CH1' # Measurement channel (e.g., CH1)
OUTPUT_FILE = 'oscilloscope_measurements_th90mV.csv' # Output CSV file
MEASUREMENT_INTERVAL = 1 # Time between measurements (seconds)

def setup_measurements(scope):
    # Reset the scope and configure measurements
    #scope.write('*RST')
    #scope.write('AUTOS EXECUTE') # Auto-set the waveform
    #scope.write('acquire:stopafter SEQUENCE') # single

    # Configure measurements for CH1
    # Peak-to-Peak (Vpp)
    scope.write('MEASUrement:MEAS1:REFLevel:PERCENT 40')
    scope.write(f'MEASUrement:MEAS1:SOUrce {CHANNEL}')
    scope.write('MEASUrement:MEAS1:TYPE PK2PK')
    #scope.write('MEASUrement:MEAS1:REFLevel:VALUE 3')
    # Rise Time (10% to 90% by default)
    scope.write(f'MEASUrement:MEAS2:SOUrce {CHANNEL}')
    scope.write('MEASUrement:MEAS2:TYPE AREA')
    
    # Fall Time (90% to 10% by default)
    scope.write(f'MEASUrement:MEAS3:SOUrce {CHANNEL}')
    scope.write('MEASUrement:MEAS3:TYPE RISE')
    
    # Area (integrated area under the waveform)
    scope.write(f'MEASUrement:MEAS4:SOUrce {CHANNEL}')
    scope.write('MEASUrement:MEAS4:TYPE FALL')
    
    # Optional: Set averaging for stability
    #scope.write('ACQuire:MODe AVERage')
    #scope.write('ACQuire:NUMAVg 16') # Average 16 acquisitions

def fetch_measurements(scope):
    # Fetch all measurements
    #scope.write('MEASUrement:MEAS1:REFLevel:VALUE 2')
    vpp = scope.query('MEASUrement:MEAS1:VALue?').strip()
    area = 0#scope.query('MEASUrement:MEAS2:VALue?').strip()
    
    rise_time = 0#scope.query('MEASUrement:MEAS3:VALue?').strip()
    fall_time = 0#scope.query('MEASUrement:MEAS4:VALue?').strip()
    
    
    return {
        'Vpp_(mV)': float(vpp)*1e3,
        'Rise_Time_(ns)': float(rise_time)*1e9,
        'Fall_Time_(ns)': float(fall_time)*1e9,
        'Area_(mV*ns)': float(area)*1e9
    }
def acquire_data_on_trigger(scope):
    try:
        # Wait for acquisition to complete with increased timeout
        start_time = time.time()
        while True:
            opc_response = scope.query('*OPC?')
            if opc_response.strip() == '1':
                return 1
                #break
    except pyvisa.errors.VisaIOError as e:
        return 0
def main():
    rm = pyvisa.ResourceManager('@py')
    
    try:
        # Connect to the oscilloscope
        scope = rm.open_resource(RESOURCE_ADDRESS)
        scope.timeout = 10000 # 10-second timeout
        print(f"Connected to: {scope.query('*IDN?')}")
        scope.write('ACQUIRE:STATE RUN')
        scope.write('*WAI')
        # Configure measurements
        setup_measurements(scope)
        vpp_old=0
        Trigger=0
        # Create CSV file and write headers
        time_start=time.time()
        with open(OUTPUT_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Trigger_No','Timeduration_ns', 'Vpp_mV', 'Rise_Time_ns', 'Fall_Time_ns', 'Area_V_ns'])
            
            # Continuous measurement loop (Ctrl+C to stop)
            while True:
                #timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                scope.write('ACQUIRE:STATE ON')
                measurements = fetch_measurements(scope)
                #scope.write('ACQUIRE:STATE STOP')
                #scope.write('acquire:stopafter SEQUENCE')
                #while True:
                #    status=scope.query("ACQuire:STATE?").strip()
                #    if status=='0':
                #       break
                #acquire_data_on_trigger(scope)
                
                #scope.write('ACQUIRE:STATE STOP')
                #time.sleep(0.1)
                # Write data to CSV
                vpp= measurements['Vpp_(mV)']
                if vpp!= vpp_old and vpp>70: #and vpp<20000:
                    time_stop=time.time()
                    timedur=time_stop-time_start
                    time_start=time_stop
                    writer.writerow([
                        Trigger,
                        timedur,
                        measurements['Vpp_(mV)'],
                        measurements['Rise_Time_(ns)'],
                        measurements['Fall_Time_(ns)'],
                        measurements['Area_(mV*ns)']
                        ])
                
                    print(f"Trigger no.: {Trigger} | Timedur: {round(timedur,2)} | Vpp: {round(measurements['Vpp_(mV)'],3)} mV | " +
                          f"Rise: {round(measurements['Rise_Time_(ns)'],3)} ns | Fall: {round(measurements['Fall_Time_(ns)'],3)} ns | " +
                          f"Area: {round(measurements['Area_(mV*ns)'],3)} mV*ns")
                    scope.write('*WAI')
                    scope.write('*cls')
                    measurements=[]
                    vpp_old=vpp
                    Trigger=Trigger+1
                    #break
                
                #time.sleep(MEASUREMENT_INTERVAL)
    
    except KeyboardInterrupt:
        print("Measurement stopped by user.")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'scope' in locals():
            scope.close()
        print("Disconnected from the oscilloscope.")

if __name__ == '__main__':
    main()