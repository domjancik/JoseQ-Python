import serial
from time import sleep

with serial.Serial('COM2', 115200, timeout=1) as ser:
    while True:
        if (ser.in_waiting > 0):
            line: bytes = ser.readline()
            print(line.decode('ascii'))

        sleep(0.1)

"""
To test locally:
- Setup a null-modem COM emulator, eg. for Windows HHD Virtual Serial Port Tools (free version works well) 
- Use the following code in REPL to setup a port and send messages (the terminating \n is important so messages are received immediately)

import serial
ser = serial.Serial('COM1', 115200 )
ser.write(b'STOP:OFF\n')       
"""
