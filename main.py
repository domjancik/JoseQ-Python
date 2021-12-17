import mido

msg = mido.Message('not_on', note=60)

outputs = mido.get_output_names()
port = mido.open_output(outputs[0])

while (True):
    if (ser.in_waiting() > 0):
        # read the bytes and convert from binary array to ASCII
        data_str = ser.read(ser.inWaiting()).decode('ascii') 
        # print the incoming string without putting a new-line
        # ('\n') automatically after every print()
        print(data_str, end='') 

    # Put the rest of your code you want here
    
    # Optional, but recommended: sleep 10 ms (0.01 sec) once per loop to let 
    # other threads on your PC run during this time. 
    time.sleep(0.01) 