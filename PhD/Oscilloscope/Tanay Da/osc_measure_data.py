#LAST DATA INFO
# 20-01-25 DATA WITH MUON ONLY TAKEN WITH LEAD (Pb) CHEMBER
#Trigger no.:: 5954 One After Arrival Time ::1.219 Sec


import pyvisa
import time
from signal import signal, SIGINT
from sys import exit
import csv
CHANNEL='CH1'
def setup_measurements(scope):
    # Reset the scope and configure measurements
    #scope.write('*RST')
    #scope.write('AUTOS EXECUTE') # Auto-set the waveform
    #scope.write('acquire:stopafter SEQUENCE') # single

    # Configure measurements for CH1
    # Peak-to-Peak (Vpp)
    #scope.write('MEASUrement:MEAS1:REFLevel:PERCENT 40')
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
def fetch_measurements(scope):
    # Fetch all measurements
    #scope.write('MEASUrement:MEAS1:REFLevel:VALUE 2')
    vpp = scope.query('MEASUrement:MEAS1:VALue?').strip()
    area = scope.query('MEASUrement:MEAS2:VALue?').strip()
    
    rise_time = scope.query('MEASUrement:MEAS3:VALue?').strip()
    fall_time = scope.query('MEASUrement:MEAS4:VALue?').strip()
    return  vpp,area,rise_time, fall_time 

def get_vpp_measurement():
    vpp=scope.query('MEASUrement:MEAS1:value?').strip()
    area = scope.query('MEASUrement:MEAS2:VALue?').strip()
    return float(vpp)*1000,float(area)*1e9
def chk_operation_complete():    
    while True:
        status=acquire_data_on_trigger()
        if(status==1):
            break
def handler(signal_received, frame):
    
    stop1=time.time()
    #chk_operation_complete()
    scope.write('acquire:stopafter RUN')
    print("SIGINT or CTRL-C detected. Exiting gracefully, total Time "+str(stop1-start1))
    #print("Total 3F trigger= "+str(Total3FTrig)+" Total 4F Trigger= "+str(Total4FTrig)+" Efficiency is= "+str(float(100.0*Total4FTrig/Total3FTrig)))
    exit(0)

signal(SIGINT, handler)        
def acquire_data_on_trigger():
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
ip_address = '192.16.13.181'  # Replace with your oscilloscope's IP address
rm = pyvisa.ResourceManager('@py')
scope = rm.open_resource(f'TCPIP::{ip_address}::INSTR')
setup_measurements(scope)
# Configure trigger (adjust settings as needed)
#scope.write('SELECT:CH1 OFF')
#scope.write('SELECT:CH3 ON')
#scope.write('TRIGger:SOURCE CH3')
#scope.write('TRIGger:LEVel 1.0V')
#scope.write('TRIGger:SLOPe RISing')

    # Configure acquisition
start1=time.time()  
'''scope.write('MEASUrement:MEAS1:souRCE CH1')
scope.write('MEASUrement:MEAS1:TYPE PK2PK')
scope.write(f'MEASUrement:MEAS2:SOUrce CH1')
scope.write('MEASUrement:MEAS2:TYPE AREA')'''

scope.write('ACQUIRE:STATE OFF')
scope.write('SAVE:WAVEFORM:FILEFORMAT CSV')
scope.write('ACTONEVent:ACTION:SAVEWFM:STATE 0')
OUTPUT_FILE = 'triggered_measurements_HPGE_CO60_TH_25mV.csv' # Output CSV file

ii=0
nEvent=10000000
Trigger=0
time_r=0
time_start=time.time()
append='a'#w
with open(  OUTPUT_FILE , append, newline='') as f:
    writer = csv.writer(f)
    if append!='w':
        writer.writerow(['Trigger_No','Timeduration_ns', 'Vpp_mV', 'Rise_Time_ns', 'Fall_Time_ns', 'Area_V_ns'])

    while ii<nEvent:
        scope.write('ACQUIRE:STATE OFF')
        scope.write('acquire:stopafter SEQUENCE') # single
        scope.write('ACQUIRE:STATE ON')
        ii=ii+1    
        vpp_old=0.0
        while True:
            status=acquire_data_on_trigger()
            if(status==1):
                #waveform_data = scope.query_binary_values('CURVE?').decode('utf-8')
                time_stop=time.time()
                timedur=time_stop-time_start
                time_r=round(timedur,4)
                #file_path = f'SAVe:WAVEform ALL, "E:/CSI_DATA/CSI_SET5_TH_140.0MV_ANODE_CO60_1500V/CO60_TH_0.10V_CSI_TRGNO_{Trigger}_TIME_{time_r}_sec_DATE_110225_0Pb.csv"'
                #file_path = f'SAVe:WAVEform ALL, "E:/WITH_SOURCE_TH_1.5V_SINP_TRGNO_{Trigger}_TIME_{timedur}_sec.csv"'
                #scope.write('ACQUIRE:STATE ON')
            # while True:
                        #status=scope.query("ACQuire:STATE?").strip()
                #vpp,area=get_vpp_measurement()
                #vpp=scope.query('MEASUrement:MEAS1:value?').strip()
                #rea = scope.query('MEASUrement:MEAS2:VALue?').strip()
                vpp,area,rise,fall=fetch_measurements(scope)

                        #if(vpp!=vpp_old):
                        #    print(f'Trigger no.:: {Trigger} One After Arrival Time ::{round(timedur,3)} Sec Value peak to peak:: {vpp*1000}  Area ::{area*1e12} ')
                        #    vpp_old=vpp
                        #scope.write('*WAI')
                        #scope.write('*cls')

                        #if status=='0':
                writer.writerow([
                    Trigger,
                    time_r,
                   vpp,
                   rise,
                   fall,
                   area
                    ])                        
                #  break
                f.flush()
                
                #time.sleep(0.1)
                #scope.write('ACQUIRE:STATE OFF')
                #scope.write(file_path)
                time_start=time_stop
                #chk_operation_complete()
                #scope.write('*WAI')
                #scope.write('*cls')
                #scope.write('FILESystem:MOUNT:DRIve  \"I:;192.16.13.200;D$;sumandg;HGCAL1234\"')
                #scope.write('SAVe:IMAGe \"I:\"')
                #scope.write('ACTONEVent:ACTION:SAVEIMAGE:STATE 1')
                #scope.write('SAVE:IMAGe \"E:/Temp.png\"')
                print(f'Trigger no.:: {Trigger} One After Arrival Time ::{round(time_r,3)} Sec Value peak to peak:: {vpp} Area under the pulse :: {area}, Rise:: {rise}   Fall:: {fall}')
                Trigger=Trigger+1
                #time.sleep(0.001)
                break

scope.close()
rm.close()
