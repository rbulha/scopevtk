# -*- coding: utf-8 -*-
from time import *
from Tkinter import *
import threading
import thread
from random import *
from ctypes import *
#from PIL import Image, ImageTk
import os
import os.path
from USBXpress import USBXpress
from USBXpress import CLogger
import vtk
import wx
import wx.aui
import wx.lib.newevent
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
from vtk import vtkRenderWindow, vtkRenderer
#from Templates.FrameLateral_xrc import xrcConfiguracao
from FrameLateral_xrc import xrcConfiguracao
from FrameLateral_xrc import xrcAnalog
from FrameLateral_xrc import xrcSonarRanging
import serial

(UpdatePlotEvent, EVT_UPDATE_PLOT) = wx.lib.newevent.NewEvent()
#evento para gerar gráfico de analise digital
(UpdateDigitalPlotEvent, EVT_UPDATE_DIGITAL_PLOT) = wx.lib.newevent.NewEvent()

wxID_FRMPANEL = wx.NewId()
wxID_FRM = wx.NewId()

VTK_DATA_ROOT = '\\Data'

class TesteTempo:
  def UseTime(self):
    t1 = time()
    sleep(2.5)
    t2 = time()
    self.tempo = t2 - t1
  def PrintTime(self):
    print self.tempo, "tempo usando time()" 
  def UseClock(self):
    c1 = clock()
    sleep(2.5)
    c2 = clock()
    self.processo = c2 - c1      
  def PrintClock(self):
    print self.processo, "tempo usando clock()"


class Plotter:
  def __init__(self, mainwin):
    self.largura = 300
    self.altura  = 300
    self.centro  = self.altura / 2 
    self.PotCanv = Canvas(mainwin, width=self.largura, height=self.altura)
    self.PotCanv.pack(side=RIGHT, fill='both', expand='yes')
    self.plot_list = []
    self.y = 0
    self.x = 0
    self.plot_list.append(0)
    self.plot_list.append(0)    
    self.plot_list.append(self.x)
    self.plot_list.append(self.y)
    self.line = self.PotCanv.create_line(self.plot_list, fill="red")
  def AddPoint(self,y):
    #normaliza a coordenada
    ny = y / 255.0
    ny = (ny * self.centro) + self.centro
    self.x += 1
    self.plot_list.append(self.x)
    self.y = ny
    self.plot_list.append(self.y)
    self.PotCanv.delete(self.line)
    self.line = self.PotCanv.create_line(self.plot_list, fill="red")
    

class ShellFrame:
  def __init__(self, mainwin):
    self.root = mainwin 
    mainwin.geometry("750x250+10+400")
    #Frame com botoes de controle
    self.LeftFrame = Frame(self.root)
    self.LeftFrame.pack(side=TOP, expand='yes',fill=X)
    #Frame com entradas do usuario
    self.CentralFrame = Frame(self.root)
    self.CentralFrame.pack(side=TOP, expand='no', fill=X)
    #Frame de saida do console
    self.BottomFrame = Frame(self.root)
    self.BottomFrame.pack(side=BOTTOM, expand='yes', fill=X)
    self.fechar = Button(self.LeftFrame, text="Fechar", fg="red", command=self.Finaliza)
    self.fechar.pack(side=BOTTOM, fill=X)
    #cria entrada do usuario
    self.UserPrompt = Entry(self.CentralFrame,text='>')
    self.UserPrompt.pack(side=TOP, fill=X)
    self.UserPrompt.bind("<Return>", self.UserEntry)
    #self.UserPrompt.insert(0,'>')    
    #coloca o foco da janela na entrada do usuario
    self.UserPrompt.focus_set() 
    #utilit class
    #Criar a saida do console
    LogOut = Text(self.BottomFrame,font=('courier', 9, 'normal'))
    LogOut.pack(side=BOTTOM, fill=X)
    self.Log = CLogger(LogOut, TRUE)    
    #inicia conexao USB
    self.USBXpress = USBXpress(self.Log)    
    
    DevN = self.USBXpress.GetDevNumber()
    self.Log.OUT("Encontado dispositivos:\n")
    Texto = ''
    for Devs in range(DevN):
      devicestr = self.USBXpress.GetDevString(Devs)
      self.Log.OUT("-- device: %d -> %256.256s",(Devs,devicestr))
      self.Log.OUT("\n")
    self.Help()
   
  def Finaliza(self):
    self.USBXpress.CloseDevice()
    self.root.quit()
  def Help(self):
    self.Log.OUT("Comandos disponiveis:\n")
    self.Log.OUT("-- Conexão\n")
    self.Log.OUT("   > connect [dev number] : conecta com uma placa de numero indicado\n")
    self.Log.OUT("   > disconnect           : desconecta\n")
    self.Log.OUT("-- Comandos gerais\n")        
    self.Log.OUT("   > cls                  : limpa tela de saida do programa\n")
    self.Log.OUT("   > exit                 : termina aplicação\n")
    self.Log.OUT("-- Comandos especiais\n")        
    self.Log.OUT("   > scope                : Inicia ociloscopio com device selecionado\n")    
  def UserEntry(self, event):
    Command = event.widget.get()
    event.widget.delete(0, END)
    Parser = Command.lstrip().split(' ')
    if Parser[0] == 'scope':
      if self.USBXpress.IsConnected():
        application = ScopeApp(self,self.Log)
        application.MainLoop()
    if Parser[0] == 'status':  
      if self.USBXpress.IsConnected():   
        ret = self.USBXpress.BoardReadStatus()
        self.Log.OUT('Tipo.........: %d\n',ret[0])
        self.Log.OUT('Porta4.......: %X\n',ret[5])
        self.Log.OUT('Aquisição....: %d\n',ret[6])
    if Parser[0] == 'help':
      self.Help()
    if Parser[0] == 'connect':
      Dev = Parser[1] 
      if self.USBXpress.IsConnected():
        self.Log.OUT('Desconectando device...\n')
        self.USBXpress.CloseDevice()
        self.Log.OUT('--> Device desconectado!\n')        
      retorno = self.USBXpress.ConnectaDev(int(Dev))
      self.Log.OUT(retorno)
    if Parser[0] == 'disconnect':
      self.USBXpress.CloseDevice()
      self.Log.OUT('Device desconectado\n')
    if Parser[0] == 'read':      
      ret = self.USBXpress.ReadRaw()
      self.Log.OUT("Read Raw\n")
      for bts in ret:
        self.Log.OUT("--> %s\n",hex(bts))
    if Parser[0] == 'exit':  
      self.Finaliza()    
    if Parser[0] == 'cls':  
      self.Log.Clear()    
    if Parser[0] == 'checkrxqueue':
      ret = self.USBXpress.CheckRXQueue()
      self.Log.OUT("  Bytes na fila de RX = %d \n",ret)
    if Parser[0] == 'readsynch':
      bytesleft = self.USBXpress.CheckRXQueue()      
      if bytesleft != 0:
        if bytesleft > 20:
          ret = self.USBXpress.ReadRawSynch(20)
        else:                 
          ret = self.USBXpress.ReadRawSynch(bytesleft)
        self.Log.OUT("Read %d bytes (Raw Synch - Don't flush the RX buffer):\n", len(ret))
        for bts in ret:
          self.Log.OUT("--> %s\n",hex(bts))                            
        ret = self.USBXpress.CheckRXQueue()
        self.Log.OUT("  Bytes na fila de RX = %d \n",ret)
      else:
        self.Log.OUT("  There is nothing to read RX = %d \n",bytesleft)  
    if Parser[0] == 'writeraw':
      size = int(Parser[1])
      print 'escreve=',size
      if size > 0 and size < 4001:     
        wbuffer = [0xFF]*size        
        ret = self.USBXpress.WriteRaw(len(wbuffer),wbuffer)   
        self.Log.OUT("Write Raw -- ret=%d\n",ret)
        
        
class VtkSNRender(vtk.vtkRenderer):
    def __init__(self, nome):
      #vtk.vtkRenderer.__init__(self)
      self.label_t = nome
      self.scree_text_offset = 10
      self.ShowLabel()
    def SetLabel(self, nome):
      self.label_t = nome
      self.text_label.SetInput(self.label_t)
    def SetMode(self, mode):
      if mode == 'scope':
        self.SetBackground(0.1, 0.2, 0.4)
      elif mode == '8chScope':          
        self.SetBackground(0.1, 0.2, 0.4)
    def SetQuadrant(self, Quadrant):
      if Quadrant == 'BL': #Botton left
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.0, 0.5, 0.5)
        self.SetBackground(0.1, 0.2, 0.4)
      if Quadrant == 'TL': #Top left
        self.SetViewport(0.0, 0.5, 0.5, 1.0)
        self.SetBackground(0.1, 0.2, 0.5)
      if Quadrant == 'BR': #Botton right          
        self.SetViewport(0.5, 0.0, 1.0, 0.5)
        self.SetBackground(0.1, 0.2, 0.6)
      if Quadrant == 'TR': #Top right           
        self.SetViewport(0.5, 0.5, 1.0, 1.0)
        self.SetBackground(0.1, 0.2, 0.7)                     
    def SetViewPoint(self, View):
        if View == 'Top':
          self.camera = self.GetActiveCamera()
          self.camera.SetFocalPoint(0, 0, 0)
          self.camera.SetPosition(0, 0, 1)          
          self.camera.SetViewUp(0, 1, 0)
          #self.label_t = 'Top'
        if View == 'Left':
          self.camera = self.GetActiveCamera()
          print self.camera 
          self.camera.SetFocalPoint(0, 0, 0)
          self.camera.SetPosition(0, 1, 0)
          self.camera.SetViewUp(1, 0, 0)
          #self.camera.OrthogonalizeViewUp()
          #self.ResetCameraClippingRange()
          print 'modificada'
          print self.camera
          #self.label_t = 'Left'
        if View == 'Right':
          self.camera = self.GetActiveCamera()
          print self.camera 
          self.camera.SetFocalPoint(0, 0, 0)
          self.camera.SetPosition(1, 0, 0)
          self.camera.SetViewUp(0, 1, 0)
          #self.label_t = 'Right' 
        if View == '3d':
          self.camera = self.GetActiveCamera()
          print self.camera 
          self.camera.SetFocalPoint(0, 0, 0)
          self.camera.SetPosition(1000, 1000, 1000)
          self.camera.SetViewUp(0, 0, -1)
          self.ResetCamera()  
                  
        self.ResetCameraClippingRange()           
        #self.ShowLabel()
            
    def ShowLabel(self):
      self.tprop = vtk.vtkTextProperty()
      size = self.GetSize()
      self.text_label = vtk.vtkTextActor()
      #self.text_label.ScaledTextOn()
      self.text_label.SetPosition(10, size[1] - 12)
      self.text_label.SetInput(self.label_t) 
      
      self.tprop.SetFontSize(12)
      self.tprop.SetFontFamilyToArial()
      self.tprop.SetJustificationToLeft()
      #self.tprop.BoldOn()
      #self.tprop.ItalicOn()
      self.tprop.ShadowOn()
      self.tprop.SetColor(0.9, 0.8, 0.8)
      self.text_label.SetTextProperty(self.tprop)
      self.AddActor2D(self.text_label)
    def UpdateSize(self):
      size = self.GetSize() 
      self.text_label.SetPosition(10, size[1] - 12)   
    def InitiateScreenText(self):
      '''
      self.tpropScren = vtk.vtkTextProperty()
      size = self.GetSize()
      self.text_screen = vtk.vtkTextActor()
      self.text_screen.SetPosition(10, 10)
      self.text_screen.SetInput(' ') 
      
      self.tpropScren.SetFontSize(10)
      self.tpropScren.SetFontFamilyToArial()
      self.tpropScren.SetJustificationToLeft()
      #self.tprop.BoldOn()
      #self.tprop.ItalicOn()
      #self.tpropScren.ShadowOn()
      self.tpropScren.SetColor(0.9, 0.8, 0.8)
      self.text_screen.SetTextProperty(self.tpropScren)
      '''
      #self.scree_text_offset = 10
      self.textMapper = vtk.vtkTextMapper()
      tprop = self.textMapper.GetTextProperty()
      tprop.SetFontFamilyToArial()
      tprop.SetFontSize(10)
      #tprop.BoldOn()
      #tprop.ShadowOn()
      tprop.SetColor(0.5, 0.9, 0.5)
      self.textActor = vtk.vtkActor2D()
      self.textActor.VisibilityOff()
      self.textActor.SetMapper(self.textMapper)

      self.AddActor2D(self.textActor)                                 
    def SetScreenText(self,x,y,text):
      self.textActor.VisibilityOff()
      self.textActor.SetPosition(x, y-self.scree_text_offset)
      self.scree_text_offset = self.scree_text_offset + 10
      self.textMapper.SetInput(text) 
      self.textActor.VisibilityOn()
    
class Cursor(vtk.vtkProbeFilter):
    def __init__(self,source):
      self.line = vtk.vtkLineSource()
      self.line.SetResolution(800)
      self.line.SetPoint1(0,800,0)
      self.line.SetPoint2(800,800,0)
      
      self.SetInputConnection(self.line.GetOutputPort())
      self.SetSource(source)
      '''    
      self.CursorPoints = vtk.vtkPoints()
      self.CursorPoints.InsertPoint(0,0,0,0)
      self.CursorPoints.InsertPoint(position,0,0,0)
      
      self.CursorValues = vtk.vtkFloatArray()
      self.CursorValues.SetName("Cursor")
      self.CursorValues.InsertValue(0,600)
      self.CursorValues.InsertValue(position,600)

      self.SetPoints(self.CursorPoints)
      #self.GetPointData().SetScalars(self.CursorValues)
      '''
      
                    
class VtkSpace:
    def __init__(self, parent,title,mode='scope'):
      self.Parent = parent
      self.iren = wxVTKRenderWindowInteractor(self.Parent,-1,size = self.Parent.GetSize())
      self.iren.SetPosition((0,0))
      self.renwin = self.iren.GetRenderWindow()
      self.renwin.StereoCapableWindowOn()
      self.renwin.StereoRenderOff()
      self.renScope = VtkSNRender(' ')
      self.renScope.SetMode(mode)
      self.renwin.AddRenderer(self.renScope)
      
      #Constantes de tela
      self.H_MAX = 800
      self.V_MAX = 1030
      
      self.V_MAX_UNIT = 3.3
      self.H_MAX_UNIT = 0.004 
      
      self.V_DIG_MAX_UNIT = 3.3
      self.H_DIG_MAX_UNIT = 65000
      
      self.points = vtk.vtkPoints()
      self.values = vtk.vtkFloatArray()
      
      self.PontosNaTela = 0
      
      self.values.SetName("Volts")
      toggle = 0.0
      edge = 500
      for i in range(self.H_MAX+6000):
        self.points.InsertPoint(i,0,0,0)
        self.values.InsertValue(i,toggle)
        if i == edge:
          if toggle:
            toggle = 0.0
          else:  
            toggle = self.V_MAX_UNIT/2
          edge = edge + 500
        self.PontosNaTela += 1 
        
      #self.values.InsertValue(0,0)  

      self.polydata1 = vtk.vtkPolyData()
      self.polydata1.SetPoints(self.points)
      self.polydata1.GetPointData().SetScalars(self.values)
      #self.polydata1.SetLines(self.lines)
      
      #self.XCursorLine = Cursor(self.polydata1)
    
      self.xyplot = vtk.vtkXYPlotActor()
      self.xyplot.AddInput(self.polydata1)
      #self.xyplot.AddInput(self.XCursorLine.GetOutput())
      self.xyplot.GetProperty().SetColor(0, 1, 0)
      self.xyplot.GetProperty().SetLineWidth(1)
      self.xyplot.GetProperty().SetPointSize(2)
      
      self.xyplot.GetAxisLabelTextProperty().SetFontSize(1)
      self.xyplot.GetAxisLabelTextProperty().BoldOff()
      
      self.xyplot.PlotPointsOn()
      self.xyplot.PlotLinesOn()
      
      self.xyplot.SetTitle(title)
      self.xyplot.SetXTitle("")
      self.xyplot.SetYTitle("")
      self.xyplot.GetPositionCoordinate().SetValue(0.02, 0.1, 0)
      self.xyplot.GetPosition2Coordinate().SetValue(0.99, 0.9, 0)
      #self.SetDigitalPlotRange()
      
      #viewX = 400.0
      #viewY = 600.0
      #self.xyplot.ViewportToPlotCoordinate( self.renScope, viewX, viewY)
      #print 'coordenadas X: ',viewX
      #print 'coordenadas Y: ',viewY 	
      
      self.PlotWidget = vtk.vtkXYPlotWidget()
      self.PlotWidget.SetXYPlotActor(self.xyplot)
      self.PlotWidget.SetInteractor(self.iren)
      
      self.renScope.AddActor2D(self.xyplot)
    def SetAnalogPlotRange(self):
      self.h_max = self.H_MAX
      self.h_min = 0
      self.v_min = 0
      self.v_max = self.V_MAX_UNIT           
      self.xyplot.SetXRange(0,self.H_MAX)
      self.xyplot.SetYRange(0,self.V_MAX_UNIT) 
      self.renwin.Render()
    def SetDigitalPlotRange(self):
      self.h_max = self.H_DIG_MAX_UNIT
      self.h_min = 0
      self.v_min = 0
      self.v_max = self.V_DIG_MAX_UNIT      
      self.xyplot.SetXRange(0,self.H_DIG_MAX_UNIT)
      self.xyplot.SetYRange(0,self.V_DIG_MAX_UNIT)
      self.renwin.Render() 
    def SetPlotRange(self,h_min, h_max,v_min, v_max):
      self.h_max = h_max
      self.h_min = h_min
      self.v_min = v_min
      self.v_max = v_max
      self.xyplot.SetXRange(h_min,h_max)
      self.xyplot.SetYRange(v_min,v_max) 
      self.renwin.Render()
    def SetDataRange(self,h_max,h_max_unit,v_max,v_max_unit):   
      self.H_MAX = h_max
      self.V_MAX = v_max
      self.V_MAX_UNIT = h_max_unit
      self.H_MAX_UNIT = v_max_unit
      self.xyplot.SetXRange(0,h_max)
      self.xyplot.SetYRange(0,v_max_unit) 
      self.renwin.Render()             
    def GetPlotRange(self):
      Range={}
      Range['h_min'] = self.h_min
      Range['h_max'] = self.h_max
      Range['v_min'] = self.v_min
      Range['v_max'] = self.v_max      
      return Range       
    def SetCliplingLookuptable(self, tipo):
      if tipo == 'Green':
        lut = vtk.vtkLookupTable()
        lut.SetHueRange(0.0, 0.66667)
        lut.SetAlphaRange(0.0,0.8)
        self.PickPlaneZ.SetLookupTable(lut)
        self.PickPlaneY.SetLookupTable(lut)
        self.PickPlaneX.SetLookupTable(lut)                       
    def UpdateSize(self):
      size = self.Parent.GetSize()
      self.iren.UpdateSize(size.GetWidth(),size.GetHeight()) 
      self.renScope.UpdateSize()

    def UpdateLabel(self, nome):
      self.renScope.SetLabel(nome)
      
    def GetActiveVolume(self):
      return self.Vol3D
    
    def Points(self, mode):
      if self.xyplot.GetPlotPoints():
        self.xyplot.PlotPointsOff()
        return 0
      else:  
        self.xyplot.PlotPointsOn()
        return 1
        
      
    def Lines(self, mode):
      if self.xyplot.GetPlotLines():
        self.xyplot.PlotLinesOff()
        return 0 
      else:
        self.xyplot.PlotLinesOn()
        return 1   
    
    def UpdateDataPlot(self, data):
      self.values = vtk.vtkFloatArray()
      self.values.SetName("Volts")
      #self.values = self.polydata1.GetPointData().GetScalars()
      #print 'data size: ',self.values.GetDataSize()
      ''' teste
      r = Random(35)
      for i in range(800):
        number = r.random()
        number=number*10
        self.values.InsertNextValue(number)    
      self.polydata1.GetPointData().SetScalars(self.values)  
      '''
      '''if self.PontosNaTela >= 1600:
        #self.values.Initialize()
        self.values = vtk.vtkFloatArray()  
        self.PontosNaTela = 0
      '''    
      for byte in data:
        volts = (float(byte)/self.V_MAX)*self.V_MAX_UNIT
        self.values.InsertNextValue(volts)
        #self.PontosNaTela+=1
      
      self.polydata1.GetPointData().SetScalars(self.values)
      self.renwin.Render()
      
    def UpdateDataDigitalPlot(self, data):
      self.values = vtk.vtkFloatArray()
      self.values.SetName("Transitions")
      self.renScope.InitiateScreenText()
      toggle = 0.0
      timecount = ' '
      edges_found = data[0]
      
      word_found = ''
      edges_in_word = 0
      last_count = 0
      bits_inter_edge = 0
      counter_per_bit = 200
      edge_counter = 0
      start_time_trip = 0
      stop_time_trip = 0
      
      MAX_EDGES_DETECT = 23
      
      HI_V = self.V_DIG_MAX_UNIT 
      LO_V = 0.2
      toggle = HI_V
      index = 1
      for i in range(self.H_DIG_MAX_UNIT):
        #self.points.InsertPoint(i,0,0,0)
        if index < 800:
          self.values.InsertValue(i,toggle)
          if i == data[index]:
            index = index + 1
            if toggle == LO_V:
              toggle = HI_V
            else:  
              toggle = LO_V
            
            edge_counter = edge_counter + 1
            
            if stop_time_trip == 0:
              if start_time_trip != 0:
                stop_time_trip = i
            
              if edge_counter >= 10 and start_time_trip == 0:
                start_time_trip = i
  
              
            if edges_in_word < MAX_EDGES_DETECT:
              bits_inter_edge = (i-last_count) / counter_per_bit
              #word_found = word_found + ('%04d '%(i-last_count))
              for bits in range(bits_inter_edge):
                word_found = word_found + ('%d '%(toggle/HI_V))
              last_count = i
              edges_in_word = edges_in_word + 1              
      '''      
      for byte in data:
        #self.values.InsertNextValue(byte)
        self.values.InsertNextValue(toggle)
        #atualstr = ('%05d ')%(byte-lastcounter)
        atualstr = ('%05d ')%byte
        lastcounter = byte
        timecount = timecount + atualstr
        if toggle == 0.0 :
          toggle = 512.0
        else:
          toggle = 0.0  
        #self.PontosNaTela+=1
      '''
      statistics = ('Bordas detectadas: %05d - ')%edges_found
      self.renScope.Clear()
      self.polydata1.GetPointData().SetScalars(self.values)
      size = self.Parent.GetSize()
      #self.renScope.SetScreenText(30,size.GetHeight()-20,(statistics+word_found))
      time_trip = ('tempo de voo=%d')%(stop_time_trip-start_time_trip)
      self.renwin.Render()
      return (statistics+word_found+'\n'+time_trip)

class BasicThread:
    def __init__(self, indentificador, parent):
        self.id = indentificador
        self.parent = parent
        self.keepGoing = self.running = False
        self.event = threading.Event()
        self.event.clear()

    def start(self):
        self.keepGoing = self.running = True
        thread.start_new_thread(self.run, ())

    def stop(self):
        self.keepGoing = self.running = False
        
    def wait(self, timeout):  
        self.event.wait(timeout) 

    def IsRunning(self):
        return self.running

    def run(self):
        print 'rodando virtual'

class Plot_Thread_TSW1250(BasicThread):
  def __init__(self, indentificador, parent, device):
    BasicThread.__init__(self, indentificador, parent)
    self.device = device
  def run(self):
    print 'running dialog, ',self.id 
    while self.IsRunning():
        pass    
class Plot_Thread(BasicThread):
  def __init__(self, indentificador, parent):
    BasicThread.__init__(self, indentificador, parent)
    self.Waiting = True
    self.trigger = 0xFF #definido 0x00 não usar trigger e != 0x00 usar
    print "init thread: ", self.id
  def SetTrigger(self, trigger):
    self.trigger = trigger  
  def run(self):
    print 'running dialog, ',self.id 
    count = 3
    self.Waiting = True 
    while self.IsRunning() and self.Waiting:
      #count += 1
      self.parent.USBXpress.FlushBuffers()
      bufferwrite     = [27]*5
      bufferwrite[1]  = self.trigger
      print bufferwrite
      if self.parent.USBXpress.WriteRaw(len(bufferwrite),bufferwrite) == 5:
        print 'PEDIU BUST'
        while self.parent.USBXpress.CheckRXQueue() == 0 and self.IsRunning():
          sleep(0.1)
        if self.IsRunning():  
          bytestoread = self.parent.USBXpress.CheckRXQueue()
          print 'bites to read: ',bytestoread
          returnbuffer = self.parent.USBXpress.ReadRawSynch(bytestoread)  
          print 'buffer read len: ',len(returnbuffer)
          self.parent.integerdata = []
          lowbyte = False
          baixo = 0
          alto = 0
          for byte in returnbuffer:
            if lowbyte:
              baixo = 0x0000 | byte
              inteiro = baixo | alto
              lowbyte = False
              self.parent.integerdata.append(inteiro)
              baixo = 0
              alto = 0
            else:
              alto = (0x0000 | byte) << 8
              inteiro = baixo | alto
              lowbyte = True
         
          print 'dados inteiros len: ', len(self.parent.integerdata)      
          evt = UpdatePlotEvent(Obj = self.parent)
          wx.PostEvent(self.parent, evt)
      #self.wait(0.500)
      self.wait(1)
      #if count > 1000000:
      #  self.stop()
    print 'bye thread %d'%self.id
    
class Digital_Plot_Thread(BasicThread):
  def __init__(self, indentificador, parent, usbeam=False):
    BasicThread.__init__(self, indentificador, parent)
    self.Waiting = True
    self.UsBeam = usbeam
    print "init digital plot thread: ", self.id
  def SendUSBeam(self, toggle):
    self.UsBeam = toggle  
  def run(self):
    print 'running digital thread, ',self.id 
    count = 3
    self.Waiting = True 
    #while self.IsRunning() and self.Waiting:
    self.parent.USBXpress.FlushBuffers()
    if self.UsBeam:
      bufferwrite = [30]*5
      bufferwrite[1] = self.parent.pulse_cycles
    else:
      bufferwrite = [29]*5
    print bufferwrite
    if self.parent.USBXpress.WriteRaw(len(bufferwrite),bufferwrite) == 5:
      print 'PEDIU BUST'
    while self.parent.USBXpress.CheckRXQueue() == 0 and self.IsRunning():
        sleep(0.1)
    
    bytestoread = self.parent.USBXpress.CheckRXQueue()
    print 'bites to read: ',bytestoread
    #textout = "Received %d bytes\n"% bytestoread
    #self.TextOutput.WriteText(textout) 
    if bytestoread > 0:
      returnbuffer = self.parent.USBXpress.ReadRawSynch(bytestoread)  
      print 'buffer read len: ',len(returnbuffer)
      self.parent.integerdata = []
      lowbyte = False
      baixo = 0
      alto = 0
      for byte in returnbuffer:
        if lowbyte:
          baixo = 0x0000 | byte
          inteiro = baixo | alto
          lowbyte = False
          self.parent.integerdata.append(inteiro)
          baixo = 0
          alto = 0
        else:
          alto = (0x0000 | byte) << 8
          inteiro = baixo | alto
          lowbyte = True
      
      print 'dados inteiros len: ', len(self.parent.integerdata)     
        
    evt = UpdateDigitalPlotEvent(Obj = self.parent)
    wx.PostEvent(self.parent, evt)
    print 'digital plot done!'
    self.stop()

class CSonar_Scope(wx.EvtHandler):
    def __init__(self,parent,device,console):
      wx.EvtHandler.__init__(self)
      self.integerdata = []
      self.pulse_cycles = 5
      self.parent = parent
      self.TextOutput = console
      self.VtkPane  = self.CreateVtkCtrl()
      self.VtkSpace = VtkSpace(self.VtkPane,'Sonar scope')
      self.parent._mgr.AddPane(self.VtkPane, 
                               wx.aui.AuiPaneInfo().Name("Sonar Scope").
                               CenterPane().CloseButton(True).MaximizeButton(True))
      self.PainelSonar = xrcSonarRanging(self.parent)                        
      self.parent._mgr.AddPane(self.PainelSonar, wx.aui.AuiPaneInfo().
                        Name("Sonar").Caption("Sonar").
                        Left().CloseButton(True).MaximizeButton(True))
      self.parent._mgr.Update()
      
      self.VtkSpace.UpdateSize()   
       
      LogOut = Text(font=('courier', 9, 'normal'))
      self.USBXpress = USBXpress(CLogger(LogOut, TRUE))
      retorno = self.USBXpress.ConnectaDev(device)
      print retorno
      self.TextOutput.WriteText(('Device %d connected - Sonar Scope\n'%device)) 

      self.PainelSonar.Bind(wx.EVT_BUTTON, self.OnButton_send_sonar_ping, self.PainelSonar.Button_send_pulse)
      
      self.PainelSonar.Bind(wx.EVT_SPINCTRL, self.OnSpinctrl_Spin_cycles, self.PainelSonar.Spin_cycles)
      
      self.PainelSonar.Bind(wx.EVT_SCROLL, self.OnScroll_Slider_zoom, self.PainelSonar.Slider_zoom)

      self.Bind(EVT_UPDATE_DIGITAL_PLOT, self.OnUpdatePlotArea)
      
      self.VtkPane.Bind(wx.EVT_SIZE, self.OnSize)

      self.digital_plot_thread = Digital_Plot_Thread(1,self)

    def OnScroll_Slider_zoom(self, evt):
        #print evt
        h_max = self.PainelSonar.Slider_zoom.GetValue() 
        self.VtkSpace.SetPlotRange(0, h_max,0, 3.3)
             
    def OnSpinctrl_Spin_cycles(self, evt):
        if self.PainelSonar.Spin_cycles.GetValue() > 0 :
           self.pulse_cycles = self.PainelSonar.Spin_cycles.GetValue()        
    def OnUpdatePlotArea(self, event):
      rettext = self.VtkSpace.UpdateDataDigitalPlot(self.integerdata)
      self.TextOutput.WriteText(rettext + '\n')         
    def OnButton_send_sonar_ping(self, evt):
      if self.digital_plot_thread.IsRunning():
        self.digital_plot_thread.stop()
        self.TextOutput.WriteText('Stop US pulse capturing\n') 
      else:
        self.digital_plot_thread.SendUSBeam(True)
        self.digital_plot_thread.start()
        self.TextOutput.Clear()
        self.TextOutput.WriteText('Start US pulse capturing\n')   
            
    def CreateVtkCtrl(self):
        VtkPanel = wx.Panel(id=wxID_FRMPANEL, name='vtkpanel', parent=self.parent,
              pos=wx.Point(0, 0), size=wx.Size(500, 600),
              style=wx.TAB_TRAVERSAL)
        VtkPanel.SetBackgroundColour(wx.Colour(128, 128, 128)) 
        return VtkPanel 
    def OnSize(self, event):
        self.VtkSpace.UpdateSize()
        event.Skip()         
          
class CBase_Scope(wx.EvtHandler):
    def __init__(self,parent,device,console,mode='scope',name='base'):
        wx.EvtHandler.__init__(self)          
        self.integerdata = [0,0]
        self.parent = parent
        self.TextOutput = console
        self.VtkPane  = self.CreateVtkCtrl()
        self.VtkSpace = VtkSpace(self.VtkPane, 'Analog scope',mode)
        self.VtkPane.Bind(wx.EVT_SIZE, self.OnSize)
        self.parent._mgr.AddPane(self.VtkPane, 
                               wx.aui.AuiPaneInfo().Name(name).
                               Left().CloseButton(True).MaximizeButton(True))
                               #CenterPane().CloseButton(True).MaximizeButton(True))        
        self.parent._mgr.Update()
        self.VtkSpace.UpdateSize()                 
        
    def CreateVtkCtrl(self):
        VtkPanel = wx.Panel(id=wxID_FRMPANEL, name='vtkpanel', 
                parent=self.parent,
                pos=wx.Point(0, 0), size=wx.Size(500, 600),
                style=wx.TAB_TRAVERSAL)
        VtkPanel.SetBackgroundColour(wx.Colour(128, 128, 128)) 
        return VtkPanel 
    def OnSize(self, event):
        self.VtkSpace.UpdateSize()
        event.Skip()         
    def OnUpdatePlotArea(self, event):
        self.VtkSpace.UpdateDataPlot(self.integerdata) 

                                                              
class CAnalog_Scope(CBase_Scope):
    def __init__(self,parent,device,console,name='analog'):
      CBase_Scope.__init__(self,parent,device,console,'scope',name)
      self.PainelAnalog = xrcAnalog(self.parent)                        
      self.PainelAnalog.Button_onoff_analog.Enable(True) 
      LogOut = Text(font=('courier', 9, 'normal'))      
      self.USBXpress = USBXpress(CLogger(LogOut, TRUE))
      retorno = self.USBXpress.ConnectaDev(device)
      print retorno
      self.TextOutput.WriteText(('Device %d connected - Analog Scope\n'%device)) 

      self.PainelAnalog.Bind(wx.EVT_BUTTON, self.OnButton_onoff_analog_capture, self.PainelAnalog.Button_onoff_analog)

      self.Bind(EVT_UPDATE_PLOT, self.OnUpdatePlotArea)
      
      self.PainelAnalog.Bind(wx.EVT_SCROLL, self.OnScroll_Slider_zoom, self.PainelAnalog.Slider_zoom)
      
      self.PainelAnalog.Bind(wx.EVT_SCROLL, self.OnScroll_Slider_position, self.PainelAnalog.Slider_position)
      
      self.plot_thread = Plot_Thread(0,self) 

    def OnScroll_Slider_position(self, evt):
        #print evt
        Range = self.VtkSpace.GetPlotRange()
        view_win = Range['h_max'] - Range['h_min']
        h_max = Range['h_max']+self.PainelAnalog.Slider_position.GetValue()
        h_min = self.PainelAnalog.Slider_position.GetValue()
        h_max = h_min+view_win
        if h_min < 0:
          h_min = 0
        if h_min >= 790:
          h_min = 790
        if h_max > 800:
          h_max = 800
        if h_max < 10:
          h_max = 10  
        if h_max <= h_min:
          h_min = h_max - 10      
        self.VtkSpace.SetPlotRange(h_min, h_max,0, 3.3)
      
    def OnScroll_Slider_zoom(self, evt):
        #print evt
        Range = self.VtkSpace.GetPlotRange()
        h_max = self.PainelAnalog.Slider_zoom.GetValue() 
        if h_max > 800:
          h_max = 800
        if h_max < 10:
          h_max = 10  
        self.VtkSpace.SetPlotRange(Range['h_min'], h_max,0, 3.3)
        
    def OnButton_onoff_analog_capture(self, evt):        
          if self.plot_thread.IsRunning():
            self.plot_thread.stop()
            self.USBXpress.FlushBuffers()
            bufferwrite = [28]*5
            print bufferwrite
            if self.USBXpress.WriteRaw(len(bufferwrite),bufferwrite) == 5:
              print 'STOP BUST'            
            self.TextOutput.WriteText('Stop capturing\n') 
          else:
            self.VtkSpace.SetAnalogPlotRange()
            if self.PainelAnalog.Check_trigger.IsChecked():
              self.plot_thread.SetTrigger(0xFF)
            else:
              self.plot_thread.SetTrigger(0x00)  
            self.plot_thread.start()
            self.TextOutput.WriteText('Start capturing\n') 
         
    def OutputToFile(self):                
        media = sum(self.integerdata) / len(self.integerdata)
        
        tempo     = localtime()
        timestamp = strftime("(%Y-%m-%d-%H-%M-%S) ", tempo)
        
        dadostr = " media = %f \n" % media
        
        linha =  timestamp + dadostr  
        self.FILE = open(self.filename,"a+")     
          
        self.FILE.writelines(linha) 
      
        self.FILE.close()
        
class CTSW1250(CBase_Scope):
    def __init__(self,parent,device,console,simulate=False,name='tsw1250'):
        CBase_Scope.__init__(self,parent,device,console,'scope',name)
        self.simulate = simulate
        if simulate:
            print "[CTSW1250] Init in simulate mode"
            self.integerdata = self.LoadSimulateData()
            print '[CTSW1250] Loaded %d points'%len(self.integerdata)
            print '[CTSW1250] data range:',(len(self.integerdata),max(self.integerdata))
            self.VtkSpace.SetDataRange(len(self.integerdata),10.0,max(self.integerdata),10.0)
            #self.VtkSpace.SetPlotRange(0, len(self.integerdata),0, max(self.integerdata))
            self.OnUpdatePlotArea(0)
        else:
            self.plot_thread = Plot_Thread_TSW1250(1,self,device)
    def LoadSimulateData(self):
        file = open('dump_ch1_4096_dec.txt','r')
        dadostr = file.readlines()
        dado = []
        for value in dadostr:
            dado.append(int(value))
        file.close()    
        return dado

class CConfigPanel(xrcConfiguracao):
    def __init__(self, parent):
        xrcConfiguracao.__init__(self, parent)
        self.parent = parent
    def OnButton_wxButtonRefreshSerial(self, evt):
        available = []
        self.wx_combo_serial_list.Clear()
        available.append( (257, 'Simulador'))
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append( (i, s.portstr))
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        for i,dev in enumerate(available):        
            print dev
            self.wx_combo_serial_list.Insert(('Port: %s'%dev[1]),i)
    def OnButton_wxInitiateView(self, evt):
        dev = self.wx_combo_serial_list.GetSelection()
        print '[CConfigPanel.OnButton_wxInitiateView] dev=',dev
        if dev != wx.NOT_FOUND :
            DevString = self.wx_combo_serial_list.GetValue() 
            if DevString == 'Port: Simulador':
               self.AnalogScope = CTSW1250(self.parent, None, self.parent.TextOutput,True)
            else:
               self.AnalogScope = CTSW1250(self.parent, None, self.parent.TextOutput)      
              
class ScopeFrm(wx.Frame):
    def __init__(self, parent, output):
      wx.Frame.__init__(self, id=wxID_FRM, name='frm', parent=None,
        pos=wx.Point(0, 0), size=wx.Size(1000, 400),
        style=wx.DEFAULT_FRAME_STYLE, title='Scope 8051')
    
      #self.VtkPane = self.CreateVtkCtrl()
      
      #self.VtkSpace1 = VtkSpace(self.VtkPane)
      
      self.USBXpress = parent.USBXpress
      
      tempo     = localtime()
      timestamp = strftime("%Y-%m-%d-%H-%M-%S.dat", tempo)
      self.filename = timestamp
      
      # tell FrameManager to manage this frame        
      self._mgr = wx.aui.AuiManager()
      self._mgr.SetManagedWindow(self)      
      self.TextOutput = self.CreateTextCtrl()                  
      self.TreeControl = self.CreateTreeCtrl()     
      self._mgr.AddPane(self.TreeControl, wx.aui.AuiPaneInfo().
                        Name("Files").Caption("Tree Pane").
                        Left().CloseButton(True).MaximizeButton(True)) 
                        
      #self.PainelControle = xrcConfiguracao(self)
      self.PainelControle = CConfigPanel(self)                        
      self._mgr.AddPane(self.PainelControle, wx.aui.AuiPaneInfo().
                        Name("Config").Caption("Configuração").
                        Left().CloseButton(True).MaximizeButton(True))      
                        
      self._mgr.AddPane(self.TextOutput, wx.aui.AuiPaneInfo().
                        Name("Output").Caption("Status").
                        Bottom().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))                         
      
      #self._mgr.AddPane(self.VtkPane, wx.aui.AuiPaneInfo().Name("VTK window").
      #                  CenterPane())
      
      self._mgr.Update()
      
      #self.VtkSpace1.UpdateSize()
      
      for dev in range(self.USBXpress.GetDevNumber()):
        self.PainelControle.Combo_devices.Insert(('Device %d'%dev),dev)
        #if self.USBXpress.IsConnected():
        #  self.USBXpress.CloseDevice()
      self.PainelControle.Combo_devices.SetSelection(0)    

      saida = VTK_DATA_ROOT
      saida = 'Plot:' + saida + '\n'
      self.TextOutput.WriteText(saida) 
            
      self.Bind(wx.EVT_SIZE, self.OnSize)
      
      self.Bind(wx.EVT_BUTTON, self.OnButton_Button_conect, self.PainelControle.Button_conect)
      
      self.Bind(wx.EVT_BUTTON, self.OnButton_Button_disconnect, self.PainelControle.Button_disconnect)
      
      self.Bind(wx.EVT_BUTTON, self.OnButton_Button_refresh_devices, self.PainelControle.Button_refresh_devices)
      
    def OnButton_Button_refresh_devices(self, evt):
      print 'refresh list'
      self.PainelControle.Combo_devices.Clear()
      for dev in range(self.USBXpress.GetDevNumber()):
        print 'refresh list dev=%d'%dev
        self.PainelControle.Combo_devices.Insert(('Device %d \n'%dev),dev)
        if self.USBXpress.IsConnected():
          print 'device %d connected'%dev #self.USBXpress.CloseDevice()
      self.PainelControle.Combo_devices.SetSelection(0)
      print 'refresh list end' 
                 
    def OnButton_Button_disconnect(self, evt):  
      self.USBXpress.CloseDevice()
      self.TextOutput.WriteText('Device disconnected\n')
      #self.PainelControle.Button_onoff_analog.Enable(False)
      
    def OnButton_Button_conect(self, evt):
        dev = self.PainelControle.Combo_devices.GetSelection()  
        if dev != wx.NOT_FOUND :
          retorno = self.USBXpress.ConnectaDev(dev)
          print retorno
          if self.USBXpress.IsConnected():
            ret = self.USBXpress.BoardReadStatus()
            self.USBXpress.CloseDevice()
            if ret[0] == 8 : #SCOPE8051 board(8) 
              print ('Device %d connected'%dev)
              if ret[1] == 1 : #class analog(1)
                self.AnalogScope = CAnalog_Scope(self, dev, self.TextOutput)
              if ret[1] == 2 : #class sonar(2)
                self.SonarScope = CSonar_Scope(self, dev, self.TextOutput)
            else:
              error = wx.MessageDialog(self, ('Device %d are not an analog scope board'%dev),'Connection error',wx.ICON_EXCLAMATION )
              error.ShowModal()
              print ('dev %d are not an analog scope board'%dev)
                          
    def OnUpdateDigitalPlotArea(self, event):      
      bytestoread = self.USBXpress.CheckRXQueue()
      print 'bites to read: ',bytestoread
      textout = "Received %d bytes\n"% bytestoread
      self.TextOutput.WriteText(textout) 
      if bytestoread > 0:
        returnbuffer = self.USBXpress.ReadRawSynch(bytestoread)  
        print 'buffer read len: ',len(returnbuffer)
        integerdata = []
        lowbyte = False
        baixo = 0
        alto = 0
        for byte in returnbuffer:
          if lowbyte:
            baixo = 0x0000 | byte
            inteiro = baixo | alto
            lowbyte = False
            integerdata.append(inteiro)
            baixo = 0
            alto = 0
          else:
            alto = (0x0000 | byte) << 8
            inteiro = baixo | alto
            lowbyte = True
        
        print 'dados inteiros len: ', len(integerdata)  
        
        rettext = self.VtkSpace1.UpdateDataDigitalPlot(integerdata)
        self.TextOutput.WriteText(rettext + '\n')     
    
    def CreateVtkCtrl(self):
        VtkPanel = wx.Panel(id=wxID_FRMPANEL, name='vtkpanel', parent=self,
              pos=wx.Point(0, 0), size=wx.Size(500, 600),
              style=wx.TAB_TRAVERSAL)
              
        VtkPanel.SetBackgroundColour(wx.Colour(128, 128, 128)) 
           
        return VtkPanel      
    def CreateTreeCtrl(self):

        tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        
        root = tree.AddRoot("Scope",0)
        items = []

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16,16)))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16,16)))
        tree.AssignImageList(imglist)

        volume3D = tree.AppendItem(root, "AD channel", 0)
        items.append(volume3D)

        USPulse = tree.AppendItem(volume3D, "Send US pulse", 1)
        
        OpacItem = tree.AppendItem(volume3D, "Channel", 1)
        tree.AppendItem(OpacItem, "Ch1 on/off", 1)
        tree.AppendItem(OpacItem, "Ch1 digital on/off", 1)
        tree.AppendItem(OpacItem, "Ch1 Send US pulse on/off", 1)
        tree.AppendItem(OpacItem, "Ch1 Points", 1)
        tree.AppendItem(OpacItem, "Ch1 Lines", 1)
        tree.AppendItem(OpacItem, "Ch1 set range Dig", 1)
        tree.AppendItem(OpacItem, "Ch1 set range Dig Zoom", 1)
        
        ADConfig = tree.AppendItem(volume3D, "AD config", 1)
        tree.AppendItem(ADConfig, "SMCLK 12MHz", 1)
        tree.AppendItem(ADConfig, "SMCLK 6MHz", 1)
        tree.AppendItem(ADConfig, "SMCLK 3MHz", 1)
        tree.AppendItem(ADConfig, "SMCLK 1.5MHz", 1)        

        ColorItem = tree.AppendItem(root, "Coloração", 0)
        items.append(ColorItem)
        tree.AppendItem(ColorItem, "Green", 1)
        tree.AppendItem(ColorItem, "Ultra-som", 1)
        tree.AppendItem(ColorItem, "Ultra-som BC", 1)
        tree.AppendItem(ColorItem, "Elastografia", 1)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivate, tree)
        
        tree.Expand(root)
        return tree
    
    def OnItemActivate(self, event):
        item = event.GetItem()

        if self.TreeControl.GetItemText(item) == "SMCLK 12MHz":
          bufferwrite = [32]*5
          bufferwrite[1] = 1
          print bufferwrite
          if self.USBXpress.WriteRaw(len(bufferwrite),bufferwrite) == 5:
            print 'Muda frequencia para 12Mhz'        
            self.TextOutput.WriteText('Muda frequencia para 12Mhz\n')        
        if self.TreeControl.GetItemText(item) == "SMCLK 6MHz":
          bufferwrite = [32]*5
          bufferwrite[1] = 2
          print bufferwrite
          if self.USBXpress.WriteRaw(len(bufferwrite),bufferwrite) == 5:
            print 'Muda frequencia para 6MHz'        
            self.TextOutput.WriteText('Muda frequencia para 6MHz\n')             
        if self.TreeControl.GetItemText(item) == "SMCLK 3MHz":
          bufferwrite = [32]*5
          bufferwrite[1] = 3
          print bufferwrite
          if self.USBXpress.WriteRaw(len(bufferwrite),bufferwrite) == 5:
            print 'Muda frequencia para 3MHz'        
            self.TextOutput.WriteText('Muda frequencia para 3MHz\n')        
        if self.TreeControl.GetItemText(item) == "SMCLK 1.5MHz":
          bufferwrite = [32]*5
          bufferwrite[1] = 4
          print bufferwrite
          if self.USBXpress.WriteRaw(len(bufferwrite),bufferwrite) == 5:
            print 'Muda frequencia para 1.5MHz'        
            self.TextOutput.WriteText('Muda frequencia para 1.5MHz\n')        
                
        if self.TreeControl.GetItemText(item) == "Send US pulse":
          bufferwrite = [31]*5
          print bufferwrite
          if self.USBXpress.WriteRaw(len(bufferwrite),bufferwrite) == 5:
            print 'PEDIU PULSO US'        
            self.TextOutput.WriteText('PEDIU PULSO US\n')
        if self.TreeControl.GetItemText(item) == "Ch1 set range Dig Zoom":
          print "Ch1 set range Dig Zoom"
          self.VtkSpace1.SetPlotRange(2000,3.3)        
        if self.TreeControl.GetItemText(item) == "Ch1 set range Dig":
          print "clicou Ch1 set range Dig"
          self.VtkSpace1.SetDigitalPlotRange()
        if self.TreeControl.GetItemText(item) == "Ch1 Send US pulse on/off":
          print "clicou Ch1 Send US pulse on/off"
          if self.digital_plot_thread.IsRunning():
            self.digital_plot_thread.stop()
            self.TextOutput.WriteText('Stop US pulse capturing\n') 
          else:
            self.digital_plot_thread.SendUSBeam(True)
            self.digital_plot_thread.start()
            self.TextOutput.Clear()
            self.TextOutput.WriteText('Start US pulse capturing\n')             
        if self.TreeControl.GetItemText(item) == "Ch1 digital on/off":
          print "clicou Ch1 digital on/off"
          if self.digital_plot_thread.IsRunning():
            self.digital_plot_thread.stop()
            self.TextOutput.WriteText('Stop digital capturing\n') 
          else:
            #self.VtkSpace1.SetDigitalPlotRange()
            self.digital_plot_thread.start()
            self.TextOutput.Clear()
            self.TextOutput.WriteText('Start digital capturing\n')        
        if self.TreeControl.GetItemText(item) == "Ch1 on/off":
          print "clicou Ch1 on/off"
          if self.plot_thread.IsRunning():
            self.plot_thread.stop()
            #self.VtkSpace1.UpdateLabel('IDLE')
            self.TextOutput.WriteText('Stop capturing\n') 
          else:
            self.VtkSpace1.SetAnalogPlotRange()
            self.plot_thread.start()
            #self.VtkSpace1.UpdateLabel('RUNNING')
            self.TextOutput.WriteText('Start capturing\n') 
        if self.TreeControl.GetItemText(item) == "Ch1 Points":
          ret = self.VtkSpace1.Points('on')
          self.TextOutput.WriteText(('Point %d\n')%ret)
        if self.TreeControl.GetItemText(item) == "Ch1 Lines": 
          ret = self.VtkSpace1.Lines('on')
          self.TextOutput.WriteText(('Lines %d\n')%ret)   
                                    
    def OnSelChanged(self, event):
        item = event.GetItem()
        print self.TreeControl.GetItemText(item) 
        event.Skip()    

    def CreateTextCtrl(self):

        text = ("Aplicativo iniciado: %d")%(wxID_FRM)

        return wx.TextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)
             
    def OnSize(self, event):
        #self.VtkSpace1.UpdateSize()
        event.Skip()         
        

class ScopeApp(wx.App):
    def __init__(self, parent, output):
        wx.App.__init__(self,0)
        self.parent = parent
        self.main = ScopeFrm(self.parent,output)
        self.main.Show()
        self.SetTopWindow(self.main)
        
class ScopeNoShell:
    def __init__(self):
      LogOut = Text(font=('courier', 9, 'normal'))
      Log = CLogger(LogOut, TRUE)           
      self.USBXpress = USBXpress(Log)
      application = ScopeApp(self,Log)
      application.MainLoop()      
      '''
      for dev in range(self.USBXpress.GetDevNumber()):
        if self.USBXpress.IsConnected():
          self.USBXpress.CloseDevice()
        retorno = self.USBXpress.ConnectaDev(dev)
        print retorno
        if self.USBXpress.IsConnected():
          ret = self.USBXpress.BoardReadStatus()
          if ret[0] == 8: #SCOPE8051 board
            application = ScopeApp(self,Log)
            application.MainLoop()
            return
      '''  
def main():
    print 'The command line arguments are:'
    for arg in sys.argv:
      print arg
    print 'End.'
    
    if len(sys.argv) > 1:
      if sys.argv[1]=='scope': 
        print 'NO GUI mode'
        ScopeNGUI = ScopeNoShell()
    else:
      root = Tk()
      MeuFrame = ShellFrame(root)    
      root.mainloop()
    
if __name__ == '__main__':
    main()    
    

