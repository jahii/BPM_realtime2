import json
from random import randint
from time import sleep
import serial
from .models import NewTable
from channels.generic.websocket import WebsocketConsumer
import mysql.connector


mydb = mysql.connector.connect(
    host = "localhost",
    user = 'root',
    port = '3306',
    passwd = '',
    database = 'SAMPLE',
    auth_plugin = 'mysql_native_password',

)


port = '/dev/ttyACM0'
baudRate = 115200 #baudrate 수정
serialPort= serial.Serial(port,baudRate)


def Decode(serialLine): 
    serialLineDe = serialLine.decode() 
    serialLineStr = str(serialLineDe)

    if serialLineStr[0] =='B': #첫문자 검사 B
        data = str(serialLineStr[1:-2])
        part1, part2, part3 = data.split(",")
        return int(part1), int(part2), int(part3)
    else : 
        print ("Error_Wrong Signal") 
        return 9999,9999,9999


def SerialRead():  # return list [Ard1,Ard2]
    if serialPort.readable():
        readLine = serialPort.readline()
        code = Decode(readLine)
        print(code)

        mycursor = mydb.cursor()
        sql = "INSERT INTO new_table (bpm, ibi, mysignal) VALUES (%s, %s, %s)"
        val = (code[0], code[1], code[2])
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted")
        return code

    else:
        print("fail from _Ardread_")


def read_DB():
    signal = NewTable.objects.latest('id')

    return signal.bpm, signal.ibi, signal.mysignal




class WSConsumer(WebsocketConsumer) :
    def connect(self):
        self.accept()
        while True:
            if serialPort.readable():
                SerialRead()
                readLine = serialPort.readline() 
                # BPM, interval, raw = Decode(readLine)
                BPM, interval, raw = read_DB()
                self.send(json.dumps({'BPM':BPM,'interval':interval, 'raw': raw}))         

#MSG = serial.Serial("COM3",9600)
'''
def Decode(A):
    A = A.decode()
    A = str(A)

    if A[0]=='S':
        MSG_dec=int(A[1:9])


        return MSG_dec

    else:
        return False

class WSConsumer(WebsocketConsumer) :
    def connect(self):
        self.accept()
        data = Serial_data()
        while True:
            if MSG.readable():
                LINE = MSG.readline()
                code = Decode(LINE)
                data.data = code
                data.save()
                self.send(json.dumps({'message': code}))
'''
        # for i in range(50):
        #     self.send(json.dumps({'message': i}))
        #     sleep(0.5)

