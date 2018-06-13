import serial
import Settings


ser = serial.Serial(Settings.COMPortName, Settings.COMBaudRate)
while(ser.is_open == True):
    rfidtag = ''
    incomingByte = ser.read(3)
    for i in incomingByte:
        rfidtag = rfidtag + str(i)
    print(rfidtag)