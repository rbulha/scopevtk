import serial
import struct
import time

class CSerialCaptureBase:
    def __init__(self):
        print '[CSerialCaptureBase] - Init'
    def Connect(self, iport):
        try:
            self.ser = serial.Serial(port=iport,baudrate=460800)
            self.ser.timeout = 10
        except serial.SerialException:
            print '[CSerialCaptureBase.Connect] - Connect fail'
    def InitTSW1205(self):
        try:
            que1 = struct.pack('BB',3,16)
            self.ser.write(que1)
            time.sleep(0.1)        
            que2 = struct.pack('BB',3,17)
            self.ser.write(que2)
            time.sleep(0.1)            
            cmd = struct.pack('38B',0x00,0xFF,0x00,0x00,0x12,0x20,0x02,0x08,0x13,0x00,0x0F,0x01,0x05,0x80,0x05,0x00
            ,0x05 ,0x40 ,0x05 ,0x00 ,0x0F ,0x00 ,0x0D ,0xFF ,0x0E ,0xFF ,0x05 ,0x80 ,0x05 ,0x00 ,0x05 ,0x40
            ,0x05 ,0x00 ,0x0D ,0x00 ,0x0E ,0x00 )
            self.ser.write(cmd)
            time.sleep(0.1)  
            self.ser.flushInput()          
        except serial.SerialException:
            print '[CSerialCaptureBase.InitTSW1205] - Init fail'
    def Disconnect(self):
        self.ser.close()
    def SeletcDataLength(self,data_length):
        try:
            #if data_length == 4096:
            cmd = struct.pack('BB',0x4,0x12)
            self.ser.write(cmd)            
        except serial.SerialException:
            print '[CSerialCaptureBase.SeletcDataLength] - SeletcDataLength fail'
    def SelectChannel(self,ch):
        try:
            if ch == 1:
                cmd = struct.pack('BBBB',2,8,19,0)
                self.ser.write(cmd)
        except serial.SerialException:
            print '[CSerialCaptureBase.SelectChannel] - SelectChannel fail'
    def OneShotCapture(self, iport, ch, Npoints):
        self.Connect(iport)
        self.SelectChannel(ch)
        data = self.Capture(Npoints)
        self.Disconnect()
        return data        
    def Capture(self,Npoints):
        cmd = struct.pack('6B',0,255,0,0,1,3)
        self.ser.flushInput()
        self.ser.write(cmd)
        time.sleep(0.01) 
        # TSW1205 send data in 12bits masked in 16bits Big-endian
        unpack_format = '>%dH'%(Npoints)
        retorno = self.ser.read(Npoints*2)
        if len(retorno) == (Npoints*2):
            dados_unp = struct.unpack(unpack_format,retorno)
            dados_m = []
            for valor in dados_unp:
                dados_m.append((valor&0x0FFF)) #take only the 12bts
            return dados_m
        else:
            print '[CSerialCaptureBase.Capture] Capture fail'
            return []
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
    ser.Connect(5)
    ser.InitTSW1205()    
    time.sleep(0.1)  
    ser.SelectChannel(1)
    time.sleep(0.1)
    ser.SeletcDataLength(4096)
    time.sleep(0.1)
    t0 = time.time()
    dados = ser.Capture(4096)
    t1 = time.time()
    ser.Disconnect()
    f = open('teste.txt','w')
    for valor in dados:
        saida = '%d\n'%(valor)
        f.write(saida)
    f.close()
    print 'Captura demorou: %f sec'%(t1-t0)
    
if __name__ == '__main__':
    tester()    
            
