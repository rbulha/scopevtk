import serial
import struct

class CSerialCaptureBase():
    def __init__(self):
        pass
    def Connect(self, iport):
        self.ser = serial.Serial(iport)
        self.ser.timeout = 10
    def Disconnect(self):
        self.ser.close()
    def SelectChannel(self,ch):
        if ch == 1:
            cmd = struct.pack('BBBB',2,8,19,0)
            self.ser.write(cmd)
            
    def Capture(self,Npoints):
        cmd = struct.pack('6B',0,255,0,0,1,3)
        self.ser.write(cmd) 
        retorno = self.ser.read(Npoints)
        if len(retorno) == Npoints:
            dados = struct.unpack('2000H',retorno)
            return dados
        else:
            print 'Falha na captura'
    def FindTSW1205(self):
        available = []
        que1 = struct.pack('BB',3,16)
        ack1 = struct.pack('8B',19,19,19,19,19,19,19,19)
        que2 = struct.pack('BB',3,17)
        ack2 = struct.pack('8B',4,4,4,4,4,4,4,4) 
        for i in range(256):
            try:
                s = serial.Serial(i)
                s.timeout = 5
                s.write(que1)
                retorno = s.read(8)
                if len(retorno):
                    print struct.unpack('8B',retorno)
                if len(retorno) == 8 and ack1 == struct.unpack('8B',retorno):
                    s.write(que2)
                    retorno = s.read(8)
                    print struct.unpack('8B',retorno)
                    if len(retorno) == 8 and ack2 == struct.unpack('8B',retorno):
                        available.append( (i, s.portstr))
                s.close()
            except serial.SerialException:
                pass
        return available                

def tester():
    ser = CSerialCaptureBase()
    ser.Connect(6)      
    ser.SelectChannel(1)
    print ser.Capture(1000)
    
if __name__ == '__main__':
    tester()    
            