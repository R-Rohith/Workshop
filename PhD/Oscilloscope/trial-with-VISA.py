#import socket

#IP = '10.10.13.216'   # Oscilloscope IP
#PORT = 5025            # Standard SCPI port

#with socket.create_connection((IP, PORT)) as s:
#    s.sendall(b'*IDN?\n')
#    print(s.recv(4096).decode())

import pyvisa
import numpy as np
import matplotlib.pyplot as plt
import time

# 1. Open VISA resource manager
rm = pyvisa.ResourceManager()

# 2. List all connected instruments
print(rm.list_resources())  # Get VISA address like 'USB0::...::INSTR'

# TCPIP0::10.10.13.216::INSTR

scope = rm.open_resource('TCPIP0::10.10.13.216::INSTR')  # Replace with your VISA address
scope.timeout = 10000  # Set timeout in ms

# 4. Identify instrument
print("Connected to: "+scope.query('*IDN?'))


# Step 3: Set data source and format
scope.write(":WAV:SOURCE CHAN2")
scope.write(":WAV:TYPE RAW")          
scope.write(":WAV:VIEW ALL")          
scope.write(":WAV:FORMAT BYTE")              # 1-byte unsigned int data
if(scope.write(":WAV:STR ON")):
	print("success")

# the below two don't work
#scope.write(":WAV:POINTS:MODE RAW")          # All available points
#scope.write(":WAV:POINTS 100000")              # Number of points to transfer (adjustable)

# Step 4: Get waveform scaling parameters
x_increment = float(scope.query(":WAV:XINC?"))
x_origin = float(scope.query(":WAV:XOR?"))
scope.clear();
y_increment = float(scope.query(":WAV:YINC?"))
y_origin = float(scope.query(":WAV:YOR?"))
y_reference = float(scope.query(":WAV:YREF?"))


starttime=time.time()
duration=10
count=0
# Step 5: Request waveform data
#while(True):#time.time()<=starttime+duration):
scope.write(":WAV:DATA?")
raw_data = scope.read_raw()
#	count+=1
#	print(count);

# Step 6: Parse binary block
# The first few bytes are a header like: #4500<data>
# Find the header length and skip it
header_length = int(raw_data[1:2])
num_digits = int(raw_data[2:2+header_length])
data_start = 2 + header_length
waveform = np.frombuffer(raw_data[data_start:], dtype=np.uint8)

# Step 7: Apply scaling to waveform
voltages = (waveform - y_reference) * y_increment + y_origin
times = np.arange(len(voltages)) * x_increment + x_origin

# 10. Plot waveform
plt.plot(times, voltages)
plt.title("Oscilloscope Waveform (CH2)")

plt.ylabel("Voltage (V)")
plt.grid(True)
plt.savefig("trial.png")

# 11. Close session
scope.close()

np.savetxt("agilent_waveform.csv", np.column_stack((times, voltages)), delimiter=",", header="Time,Voltage")


