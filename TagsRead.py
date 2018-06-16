import serial
import Settings

f = open("tags.txt", "w")

ser = serial.Serial(Settings.COMPortName, Settings.COMBaudRate)
while(ser.is_open == True):
    rfidtag = ''
    incomingByte = ser.read(3)
    for i in incomingByte:
        rfidtag = rfidtag + str(i)
    try:
        print(rfidtag+": "+str(Settings.TagsIntoNumbers[rfidtag]))
    except:
        number = input(rfidtag+": ")
        if len(number)>0:
            f.write("\"{0}\":{1},\n".format(rfidtag, number))
