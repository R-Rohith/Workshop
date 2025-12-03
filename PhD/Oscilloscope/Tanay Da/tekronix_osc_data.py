#LAST DATA INFO
# 20-01-25 DATA WITH MUON ONLY TAKEN WITH LEAD (Pb) CHEMBER
#Trigger no.:: 5954 One After Arrival Time ::1.219 Sec


import pyvisa
import time
from signal import signal, SIGINT
from sys import exit
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

# Configure trigger (adjust settings as needed)
#scope.write('SELECT:CH1 OFF')
#scope.write('SELECT:CH3 ON')
#scope.write('TRIGger:SOURCE CH3')
#scope.write('TRIGger:LEVel 1.0V')
#scope.write('TRIGger:SLOPe RISing')

    # Configure acquisition
start1=time.time()    
scope.write('ACQUIRE:STATE OFF')
scope.write('SAVE:WAVEFORM:FILEFORMAT CSV')
scope.write('ACTONEVent:ACTION:SAVEWFM:STATE 1')

ii=0
nEvent=50000
Trigger=0
time_start=time.time()
while ii<nEvent:
    scope.write('ACQUIRE:STATE OFF')
    scope.write('acquire:stopafter SEQUENCE') # single
    scope.write('ACQUIRE:STATE ON')
    ii=ii+1    
    while True:
        status=acquire_data_on_trigger()
        if(status==1):
            #waveform_data = scope.query_binary_values('CURVE?').decode('utf-8')
            time_stop=time.time()
            timedur=time_stop-time_start
            time_r=round(timedur,3)
            file_path = f'SAVe:WAVEform ALL, "E:/CSI_DATA/CSI_SET5_TH_140.0MV_ANODE_CO60_1500V/CO60_TH_0.10V_CSI_TRGNO_{Trigger}_TIME_{time_r}_sec_DATE_110225_0Pb.csv"'
            #file_path = f'SAVe:WAVEform ALL, "E:/WITH_SOURCE_TH_1.5V_SINP_TRGNO_{Trigger}_TIME_{timedur}_sec.csv"'

            time_start=time_stop
            scope.write(file_path)
            
            chk_operation_complete()
            scope.write('*WAI')
            scope.write('*cls')
            #scope.write('FILESystem:MOUNT:DRIve  \"I:;192.16.13.200;D$;sumandg;HGCAL1234\"')
            #scope.write('SAVe:IMAGe \"I:\"')
            #scope.write('ACTONEVent:ACTION:SAVEIMAGE:STATE 1')
            #scope.write('SAVE:IMAGe \"E:/Temp.png\"')
            print(f'Trigger no.:: {Trigger} One After Arrival Time ::{round(timedur,3)} Sec')
            Trigger=Trigger+1
            #time.sleep(0.001)
            break

scope.close()
rm.close()
