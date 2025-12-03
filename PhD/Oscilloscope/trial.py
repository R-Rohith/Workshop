import socket

s = socket.socket()
s.connect(("10.10.13.216", 5025))
s.sendall(b":WAV:FORM BYTE\n:WAV:SOUR CHAN2\n:RUN\n")
s.sendall(b":WAV:DATA?\n")


#x_increment = float(scope.query(":WAV:XINC?"))
#x_origin = float(scope.query(":WAV:XOR?"))
#scope.clear();
y_increment = float(scope.query(":WAV:YINC?"))
y_origin = float(scope.query(":WAV:YOR?"))
y_reference = float(scope.query(":WAV:YREF?"))

raw_data = s.recv(100000)



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
plt.title("Oscilloscope Waveform (CH1)")

plt.ylabel("Voltage (V)")
plt.grid(True)
plt.savefig("trial.png")

# 11. Close session
scope.close()

np.savetxt("agilent_waveform.csv", np.column_stack((times, voltages)), delimiter=",", header="Time,Voltage")


