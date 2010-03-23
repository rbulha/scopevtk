# -*- coding: utf-8 -*-
from time import *
from Tkinter import *
from threading import Thread
from random import *
from ctypes import *
#from PIL import Image, ImageTk
import os
import os.path

class CLogger:
  def __init__(self, saida, bTiming=FALSE):
    self.saida   = saida
    self.bTiming = bTiming
    self.fgcolor='black'
    self.saida.config(fg=self.fgcolor)
  def SetTimestamp(bTiming=TRUE):
    self.bTiming = bTiming
  def OUT(self, formato, parametros = (), color='black'):
    tempo     = localtime()
    timestamp = strftime("(%Y/%m/%d %H:%M:%S) ", tempo)
    saida = formato % parametros
    print saida
    if self.bTiming == TRUE:
      saida = timestamp + saida
    self.saida.config(fg=color)  
    self.saida.insert(END,saida) 
  def Clear(self):
    self.saida.delete(1.0, END)
   
''' Comandos usados para comunicaçao entre HOST e device
#define CMD_LED1              1
#define CMD_LED2              2
#define CMD_SETTIME           3  
#define CMD_M1                4
#define CMD_M2                5
#define CMD_M3                6  
#define CMD_M4                7
#define CMD_ALL_M             8
#define CMD_LCD_PUT           9
#define CMD_LCD_REFRESH       10
#define CMD_LCD_CLEAR         11
#define CMD_SET_FREQS         12
#define CMD_SEND_UART1        13
#define CMD_C2_RESET          14
#define CMD_C2_GET_ID         15
#define CMD_C2_CRC_OK         16
#define CMD_C2_DW_LINE        17
#define CMD_C2_ERASE_DEVICE   18
#define CMD_PKG_WRITE         19
#define CMD_PKG_READ          20
#define CMD_INIT_FW_READ      21
'''
class USBXpress:
  def __init__(self, LogOut):
    self.SiUSBXp = windll.SiUSBXp 
    print self.SiUSBXp
    self.NumeroDeDevices = c_ulong() 
    self.DeviceHandle    = c_ulong(0)
    self.IN_size = 16
    self.OUT_size = 16
    self.LogOut = LogOut
    #python nao usa ponteiros nativamente para isso ele possui a funcao byref que passa a referencia da variavel   
    retorno = self.SiUSBXp.SI_GetNumDevices(byref(self.NumeroDeDevices))
    print "retorno:",retorno," Numero de devices:", self.NumeroDeDevices
    #falta conectar o device
  def IsConnected(self):
    if self.DeviceHandle.value > 0:
      return True
    else:
      return False  
  def GetDevNumber(self):
    return self.NumeroDeDevices.value
  def GetDevString(self, DevNum):
    #define SI_RETURN_SERIAL_NUMBER 0x00
    #define SI_RETURN_DESCRIPTION 0x01
    #define SI_RETURN_LINK_NAME 0x02
    #define SI_RETURN_VID 0x03
    #define SI_RETURN_PID 0x04  
    devstring  = create_string_buffer(256)
    devnumber  = c_ulong(DevNum)
    retorno = self.SiUSBXp.SI_GetProductString(devnumber, devstring, 0x04)
    print "retorno:",retorno," Device string:", devstring.raw
    return devstring.raw
  def ConnectaDev(self, DeviceN):
    if DeviceN < self.NumeroDeDevices.value:
      self.SelectedDevice = c_ulong(DeviceN)
      retorno = self.SiUSBXp.SI_Open(self.SelectedDevice, byref(self.DeviceHandle))
      if retorno == 0:
        print "retorno:",retorno," device:",self.SelectedDevice," handle:", self.DeviceHandle
        Texto = 'Device %d conectado com sucesso\n' % DeviceN
        return Texto 
      else:
        return 'Falha no SI_Open!\n'   
    else:
      return 'Device %d nao existe!\n' % DeviceN    
  def Leitura(self):
    lista   = []
    retorno = self.SiUSBXp.SI_FlushBuffers(self.DeviceHandle,0,0)
    if retorno == 0:
      readbuffer  = create_string_buffer(16)
      bytesread   = c_ulong()
      bytestoread = c_ulong(self.IN_size) 
      retorno     = self.SiUSBXp.SI_Read(self.DeviceHandle, readbuffer, bytestoread, byref(bytesread), None)
      if retorno == 0:
        print 'bytestoread..:',bytestoread
        print 'bytesread....:',bytesread
        bufferRAW   = readbuffer.raw
        lista.append(ord(bufferRAW[0]))
        lista.append(ord(bufferRAW[1]))
        temperaturaLM35 = ((ord(bufferRAW[2]) * 3.2) / 1024.0)/0.010;
        lista.append(temperaturaLM35)
        lista.append(ord(bufferRAW[3]))
        temperaturaInterna = ((ord(bufferRAW[4]) * 3.2) / 1024.0)/0.010;
        lista.append(temperaturaInterna)
        lista.append(ord(bufferRAW[5]))
        lista.append(ord(bufferRAW[6]))
        lista.append(ord(bufferRAW[7]))
        lista.append(ord(bufferRAW[8]))
        lista.append(ord(bufferRAW[9]))
        lista.append(ord(bufferRAW[10]))
        lista.append(ord(bufferRAW[11]))
        lista.append(ord(bufferRAW[12]))
        lista.append(ord(bufferRAW[13]))
        lista.append(ord(bufferRAW[14]))
        lista.append(ord(bufferRAW[15]))
    return lista    
  def ReadRaw(self):
    lista   = []
    retorno = self.SiUSBXp.SI_FlushBuffers(self.DeviceHandle,0,0)
    if retorno == 0:
      readbuffer  = create_string_buffer(15)
      bytesread   = c_ulong()
      bytestoread = c_ulong(self.IN_size) 
      retorno     = self.SiUSBXp.SI_Read(self.DeviceHandle, readbuffer, bytestoread, byref(bytesread), None)
      if retorno == 0:
        #print 'bytestoread..:',bytestoread
        #print 'bytesread....:',bytesread
        bufferRAW   = readbuffer.raw
        lista.append(ord(bufferRAW[0]))
        lista.append(ord(bufferRAW[1]))
        lista.append(ord(bufferRAW[2]))
        lista.append(ord(bufferRAW[3]))
        lista.append(ord(bufferRAW[4]))
        lista.append(ord(bufferRAW[5]))
        lista.append(ord(bufferRAW[6]))
        lista.append(ord(bufferRAW[7]))
        lista.append(ord(bufferRAW[8]))
        lista.append(ord(bufferRAW[9]))
        lista.append(ord(bufferRAW[10]))
        lista.append(ord(bufferRAW[11]))
        lista.append(ord(bufferRAW[12]))
        lista.append(ord(bufferRAW[13]))
        lista.append(ord(bufferRAW[14]))
    return lista
          
  def ReadDevice(self):
    retorno = self.SiUSBXp.SI_FlushBuffers(self.DeviceHandle,0,0)
    #print "Flush retorno:",retorno  
    readbuffer  = create_string_buffer(15)
    bytesread   = c_ulong()
    bytestoread = c_ulong(self.IN_size) 
    retorno     = self.SiUSBXp.SI_Read(self.DeviceHandle, readbuffer, bytestoread, byref(bytesread), None)
    bufferRAW   = readbuffer.raw
    temperaturaLM35 = ((ord(bufferRAW[2]) * 3.2) / 1024.0)/0.010;
    print "Read retorno:",retorno," handle:", self.DeviceHandle,"bytes to read:",bytestoread,"read:",bytesread#,"buffer:",repr(bufferRAW)
    print "Sw1 :%(led)x" % {'led':ord(bufferRAW[0])}
    print "Sw2 :%(led)x" % {'led':ord(bufferRAW[1])}
    print "LM35:%(led)f" % {'led':temperaturaLM35}
    self.Pot = ord(bufferRAW[3])  
    print "Pot :%(led)d" % {'led':ord(bufferRAW[3])}        
    print "Temp:%(led)d" % {'led':ord(bufferRAW[4])}  
    self.Led1 = ord(bufferRAW[5])     
    print "Led1:%(led)d" % {'led':ord(bufferRAW[5])}
    self.Led2 = ord(bufferRAW[6])        
    print "Led2:%(led)x" % {'led':ord(bufferRAW[6])}        
    print "M1  :%(led)d" % {'led':ord(bufferRAW[7])}
    print "M2  :%(led)d" % {'led':ord(bufferRAW[8])}
    tempo = localtime()
    print "Tempo do PC  : ",strftime("%Y/%m/%d %H:%M:%S", tempo)
    print "Tempo do R2D2:    %(ano)02d/%(mes)02d/%(dia)02d %(hora)02d:%(min)02d:%(seg)02d" % \
      { 'ano':ord(bufferRAW[14]), 'mes':ord(bufferRAW[13]), 'dia':ord(bufferRAW[12]), 'hora':ord(bufferRAW[9]),'min':ord(bufferRAW[10]), 'seg':ord(bufferRAW[11]) }
#    print "H   :%(led)d" % {'led':ord(bufferRAW[9])}
#    print "M   :%(led)d" % {'led':ord(bufferRAW[10])}  
#    print "S   :%(led)d" % {'led':ord(bufferRAW[11])}
#    print "D   :%(led)d" % {'led':ord(bufferRAW[12])}
#    print "M   :%(led)d" % {'led':ord(bufferRAW[13])}
#    print "A   :%(led)d" % {'led':ord(bufferRAW[14])}
    segundosPC = tempo[3]*3600 + tempo[4]*60 + tempo[5]
    segundosMC = ord(bufferRAW[9])*3600 + ord(bufferRAW[10])*60 + ord(bufferRAW[11])
    segundosPC = float(segundosPC)
    segundosMC = float(segundosMC)    
    print "PC (seg):",segundosPC," MC (seg):",segundosMC
    print "Relacao tempo(PC/MC): %(pc)0.7f  (MC/PC): %(mc)0.7f" % \
      { 'pc':(segundosPC/segundosMC), 'mc':(segundosMC/segundosPC) }
  # ReadRawSynch - nao faz flush no buffer para ler    
  def ReadRawSynch(self, size):
    lista   = []
    if self.IsConnected():
      readbuffer  = create_string_buffer(size)
      bytesread   = c_ulong()
      bytestoread = c_ulong(size) 
      retorno     = self.SiUSBXp.SI_Read(self.DeviceHandle, readbuffer, bytestoread, byref(bytesread), None)
      if retorno == 0:
        #print 'bytestoread..:',bytestoread
        #print 'bytesread....:',bytesread
        bufferRAW   = readbuffer.raw
        for i,Raw in enumerate(bufferRAW):
          if i < bytesread.value:
            lista.append(ord(Raw))
    return lista
  def WriteRaw(self, size, wbuffer):
    if self.IsConnected():  
      writebuffer  = create_string_buffer('\x00'*size)
      byteswroted  = c_ulong()
      bytestowrite = c_ulong(size)
      for i,bytes in enumerate(wbuffer):
        writebuffer[i] = chr(bytes)
      ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
      print 'wirteraw ret=',ret
      return byteswroted.value
    return 0  
  def MoveServo(self, servo, angle):
    writebuffer  = create_string_buffer('\x00'*15)
    charangle = chr(angle)
    if servo == 1:
      writebuffer[0]  = chr(4) 
      writebuffer[5] = charangle
    if servo == 2: 
      writebuffer[0]  = chr(5)
      writebuffer[6] = charangle
    if servo == 3:
      writebuffer[0]  = chr(6) 
      writebuffer[7] = charangle
    if servo == 4:
      writebuffer[0]  = chr(7) 
      writebuffer[8] = charangle
    raw = writebuffer.raw
    print "write servo:", servo," angle:",charangle, "buffer:", repr(raw)    
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(15)
    retorno      = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    print "Write retorno:",retorno," handle:", self.DeviceHandle,"bytes to write:",bytestowrite,"write:",byteswroted
  def SetRTC(self):
    writebuffer  = create_string_buffer('\x00'*15)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(15)
    tempo = localtime()
    writebuffer[0]  = chr(3)
    writebuffer[9]  = chr(tempo[3])
    writebuffer[10] = chr(tempo[4])
    writebuffer[11] = chr(tempo[5])
    writebuffer[12] = chr(tempo[2])
    writebuffer[13] = chr(tempo[1])
    writebuffer[14] = chr(07)
    return self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    #print "Write retorno:",retorno," handle:", self.DeviceHandle,"bytes to write:",bytestowrite,"write:",byteswroted
  def SendUART1Char(self, SendChar):
    writebuffer  = create_string_buffer('\x00'*5)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(5)
    tempo = localtime()
    writebuffer[0]  = chr(13)
    writebuffer[1]  = chr(SendChar)
    return self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
  def ApagaLeds(self):
    writebuffer     = create_string_buffer('\x00'*4)
    writebuffer[0]  = chr(2)
    writebuffer[2]  = chr(0)
    byteswroted     = c_ulong()
    bytestowrite    = c_ulong(4)
    retorno         = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    print "Write retorno:",retorno," handle:", self.DeviceHandle,"bytes to write:",bytestowrite,"write:",byteswroted
  def AcendeLeds(self):
    writebuffer     = create_string_buffer('\xFF'*4)
    writebuffer[0]  = chr(2)
    writebuffer[2]  = chr(1)
    byteswroted     = c_ulong()
    bytestowrite    = c_ulong(4)
    retorno         = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    print "Write retorno:",retorno," handle:", self.DeviceHandle,"bytes to write:",bytestowrite,"write:",byteswroted
  def CloseDevice(self):
    if self.DeviceHandle != 0:
      retorno = self.SiUSBXp.SI_Close(self.DeviceHandle)
      self.DeviceHandle = c_ulong(0)
      print "Close retorno:",retorno
      self.LogOut.OUT('device closed:\n')
  def FlushBuffers(self):
    retorno = self.SiUSBXp.SI_FlushBuffers(self.DeviceHandle,0,0)
    print "Flush retorno:",retorno
    self.LogOut.OUT('device flushed:\n')
  def PutLCD(self,x,y,ch):
    writebuffer  = create_string_buffer('\x00'*15)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(15)
    writebuffer[0]  = chr(9)
    writebuffer[1]  = chr(x)
    writebuffer[2]  = chr(y)
    writebuffer[3]  = chr(FontLookup[ord(ch) - 32][0] << 1)
    writebuffer[4]  = chr(FontLookup[ord(ch) - 32][1] << 1)
    writebuffer[5]  = chr(FontLookup[ord(ch) - 32][2] << 1)
    writebuffer[6]  = chr(FontLookup[ord(ch) - 32][3] << 1)
    writebuffer[7]  = chr(FontLookup[ord(ch) - 32][4] << 1)
    retorno      = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    print "PutLCD ", (ord(ch) - 32)," retorno:",retorno," handle:", self.DeviceHandle,"bytes to write:",bytestowrite,"write:",byteswroted
  def RefreshLCD(self):    
    writebuffer  = create_string_buffer('\x00'*15)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(15)
    writebuffer[0]  = chr(10)
    retorno      = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    print "Refresh retorno:",retorno," handle:", self.DeviceHandle,"bytes to write:",bytestowrite,"write:",byteswroted
  def ClearLCD(self):    
    writebuffer  = create_string_buffer('\x00'*15)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(15)
    writebuffer[0]  = chr(11)
    retorno      = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    print "Clear retorno:",retorno," handle:", self.DeviceHandle,"bytes to write:",bytestowrite,"write:",byteswroted
  def C2ReadID(self):
    writebuffer  = create_string_buffer('\x00'*3)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(3)
    writebuffer[0]  = chr(15)
    return self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
  def C2Reset(self):
    writebuffer  = create_string_buffer('\x00'*3)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(3)
    writebuffer[0]  = chr(14)
    return self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)          
  def C2TestCRC(self):
    writebuffer  = create_string_buffer('\x00'*50)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(50)
    writebuffer[0]  = chr(16)
    writebuffer[48]  = chr(11)
    writebuffer[49]  = chr(11)
    ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    return byteswroted.value
  def C2SendLine(self, lista):
    writebuffer  = create_string_buffer('\x00'*50)
    byteswroted  = c_ulong()
    length = len(lista) + 1
    bytestowrite = c_ulong(length)
    writebuffer[0]  = chr(17)
    for i,token in enumerate(lista):
      writebuffer[i+1]  = chr(token)
    ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    return byteswroted.value    
  def C2IsPTboard(self):
    retorno = self.SiUSBXp.SI_FlushBuffers(self.DeviceHandle,0,0)
    if retorno == 0:  
      if self.RequestStatus():
        sleep(0.1)
        while self.CheckRXQueue()==0:
          sleep(0.1)
        readbuffer  = create_string_buffer(10)
        bytesread   = c_ulong()
        bytestoread = c_ulong(10) 
        retorno     = self.SiUSBXp.SI_Read(self.DeviceHandle, readbuffer, bytestoread, byref(bytesread), None)
        if retorno == 0:
          bufferRAW   = readbuffer.raw
          if ord(bufferRAW[0]) == 0x07:
            return True
    return False
  def BoardReadStatus(self):
    retorno = self.SiUSBXp.SI_FlushBuffers(self.DeviceHandle,0,0)
    if retorno == 0:  
      if self.RequestStatus():
        sleep(0.1)
        while self.CheckRXQueue()==0:
          sleep(0.1)
        return self.ReadRawSynch(10)  
    return None          
  def C2EraseDevice(self):
    writebuffer  = create_string_buffer('\x00'*5)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(5)
    writebuffer[0]  = chr(18) #comando de erase device
    writebuffer[1]  = chr(18) #byte de confirmação
    ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    return byteswroted.value
  def ForcaPacote(self):
    writebuffer  = create_string_buffer('\x00'*5)
    byteswroted  = c_ulong()
    bytestowrite = c_ulong(5)
    writebuffer[0]  = chr(19) #comando forca envio de um pacote de 2kb
    writebuffer[1]  = chr(19) #byte de confirmação
    ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
    return byteswroted.value   
  def CheckRXQueue(self):
    NumBytesInQueue  = c_ulong()
    QueueStatus      = c_ulong()
    '''
    Return Value: SI_STATUS = SI_SUCCESS = 0x00 
    or 
    SI_DEVICE_IO_FAILED  = 0x08 
    SI_INVALID_HANDLE    = 0x01 
    SI_INVALID_PARAMETER = 0x06 
    '''     
    ret = self.SiUSBXp.SI_CheckRXQueue(self.DeviceHandle, byref(NumBytesInQueue), byref(QueueStatus))
    if ret != 0:
      print 'CheckRWQueue failure: code=%d' % QueueStatus.value
      return 0
    else:  
      return NumBytesInQueue.value      
  def ReadPacket(self, tipo, size):
    '''Função generica para leitra USB em pacotes de ate 4k
       E de responsabilidade do HOST monitorar a fila RX ate que todo pacote seja consumido
       O tipo informa ao Device o que mandar!
    '''
    if size < 4001 and self.IsConnected():    
      writebuffer  = create_string_buffer('\x00'*5)
      byteswroted  = c_ulong()
      bytestowrite = c_ulong(5)
      writebuffer[0]  = chr(20)   #comando pede o envio de um pacote
      writebuffer[1]  = chr(tipo) #tipo do pacote
      writebuffer[2]  = chr(size) #tamanho do pacote 0 = 4k
      ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
      return byteswroted.value
    return 0              
  def C2_PrepareToReadFW(self):
    if self.IsConnected():  
      writebuffer  = create_string_buffer('\x00'*5)
      byteswroted  = c_ulong()
      bytestowrite = c_ulong(5)
      writebuffer[0]  = chr(21) #comando reseta comunicação de pacotes
      writebuffer[1]  = chr(21) #confimação
      writebuffer[2]  = chr(21) #confimação
      ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
      return byteswroted.value
    return 0
  def RequestStatus(self):
    if self.IsConnected():  
      writebuffer  = create_string_buffer('\x00'*5)
      byteswroted  = c_ulong()
      bytestowrite = c_ulong(5)
      writebuffer[0]  = chr(22) #comando reseta comunicação de pacotes
      writebuffer[1]  = chr(22) #confimação
      writebuffer[2]  = chr(22) #confimação
      ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
      print 'wirte req status ret=',ret
      return byteswroted.value
    return 0
  def C2_PrepareToSendFW(self, addH, addL, size):
    if self.IsConnected():  
      writebuffer  = create_string_buffer('\x00'*5)
      byteswroted  = c_ulong()
      bytestowrite = c_ulong(5)
      writebuffer[0]  = chr(23)   #comando inicia comunicação de pacotes
      writebuffer[1]  = chr(addH) #address HIGH byte
      writebuffer[2]  = chr(addL) #address LOW  byte
      nH = (size & 0xFF00) >> 8
      nL =  size & 0x00FF
      writebuffer[3]  = chr(nH)   #size HIGH byte
      writebuffer[4]  = chr(nL)   #size LOW  byte      
      ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
      print 'wirte init ret=',ret
      return byteswroted.value
    return 0                      
  def C2_SendFWPkg(self, addH, addL, size, codebuffer):
    if self.IsConnected():  
      self.C2_PrepareToSendFW(addH, addL, size)
      sleep(0.5)
      while self.CheckRXQueue() == 0:
        sleep(0.1)
      lista = self.ReadRawSynch(60)
      if lista[0] == 0x07: #confirma recebimento
        writebuffer  = create_string_buffer('\x00'*size)
        print 'tamanho do buffer geral=',len(writebuffer)
        byteswroted  = c_ulong()
        bytestowrite = c_ulong(size)
        for index,bytes in enumerate(codebuffer):
          writebuffer[index] = chr(bytes)
        print 'tamanho do codebuffer=',len(codebuffer)  
        print 'tamanho do buffer geral=',len(writebuffer)
        print 'bytes to write=',bytestowrite.value   
        ret = self.SiUSBXp.SI_Write(self.DeviceHandle, writebuffer, bytestowrite, byref(byteswroted), None)
        print 'wirte pkg ret=',ret
        return byteswroted.value
      else:
        print 'Init communication fail!'  
        return 0        
    else:
      print 'device not connected!'  
      return 0                      
            
