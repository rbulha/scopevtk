from time import *
from Tkinter import *
import threading
import thread
from random import *
from ctypes import *
from PIL import Image, ImageTk
import os
import os.path
from USBXpress import USBXpress
import vtk
import wx
import wx.aui
import wx.lib.newevent
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
from vtk import vtkRenderWindow, vtkRenderer

(UpdatePlotEvent, EVT_UPDATE_PLOT) = wx.lib.newevent.NewEvent()

wxID_FRMPANEL = wx.NewId()
wxID_FRM = wx.NewId()

VTK_DATA_ROOT = '\\Data'

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
        application = ScopeApp(self)
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
      self.ShowLabel()
    def SetMode(self, mode):
      if mode == 'scope':
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
      
class VtkSpace:
    def __init__(self, parent):
      self.Parent = parent
      self.iren = wxVTKRenderWindowInteractor(self.Parent,-1,size = self.Parent.GetSize())
      self.iren.SetPosition((0,0))
      self.renwin = self.iren.GetRenderWindow()
      self.renwin.StereoCapableWindowOn()
      self.renwin.StereoRenderOff()
      self.renScope = VtkSNRender('SINGLE')
      self.renScope.SetMode('scope')
      self.renwin.AddRenderer(self.renScope)
      
      self.points = vtk.vtkPoints()
      self.values = vtk.vtkIntArray()
      
      
      self.values.SetName("Volts")
      for i in range(800):
        self.points.InsertPoint(i,0,0,0)
        self.values.InsertNextValue(i+10)

      self.polydata1 = vtk.vtkPolyData()
      self.polydata1.SetPoints(self.points)
      self.polydata1.GetPointData().SetScalars(self.values)
      #self.polydata1.SetLines(self.lines)
      
    
      self.xyplot = vtk.vtkXYPlotActor()
      self.xyplot.AddInput(self.polydata1)
      self.xyplot.GetProperty().SetColor(0, 0, 0)
      self.xyplot.GetProperty().SetLineWidth(2)
      
      self.xyplot.SetTitle("Scope")
      self.xyplot.SetXTitle("")
      self.xyplot.SetYTitle("")
      self.xyplot.GetPositionCoordinate().SetValue(0.1, 0.1, 0)
      self.xyplot.GetPosition2Coordinate().SetValue(0.9, 0.9, 0)
      self.xyplot.SetXRange(0,800)
      self.xyplot.SetYRange(0,1023)
      
      self.renScope.AddActor2D(self.xyplot)
      
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

    def GetActiveVolume(self):
      return self.Vol3D
    
    def UpdateDataPlot(self, data):
      self.values = vtk.vtkFloatArray()
      self.values.SetName("Volts")
      ''' teste
      r = Random(35)
      for i in range(800):
        number = r.random()
        number=number*10
        self.values.InsertNextValue(number)    
      self.polydata1.GetPointData().SetScalars(self.values)  
      '''
      for byte in data:
        self.values.InsertNextValue(byte)
      self.polydata1.GetPointData().SetScalars(self.values)        
      self.renwin.Render()

class BasicThread:
    def __init__(self):
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

class Plot_Thread(BasicThread):
  def __init__(self, indentificador, parent):
    BasicThread.__init__(self)
    self.id = indentificador
    self.parent = parent
    self.Waiting = True
    print "init thread: ", self.id
  def run(self):
    print 'running dialog, ',self.id 
    count = 3
    self.Waiting = True 
    while self.IsRunning() and self.Waiting:
      count += 1
      evt = UpdatePlotEvent(Obj = self.parent)
      wx.PostEvent(self.parent, evt)
      self.wait(0.100)
      if count > 100000:
        self.stop()
    print 'bye thread'


class ScopeFrm(wx.Frame):
    def __init__(self, parent):
      wx.Frame.__init__(self, id=wxID_FRM, name='frm', parent=None,
        pos=wx.Point(0, 0), size=wx.Size(1000, 400),
        style=wx.DEFAULT_FRAME_STYLE, title='Scope 8051')
    
      self.VtkPane = self.CreateVtkCtrl()
      
      self.VtkSpace1 = VtkSpace(self.VtkPane)
      
      self.USBXpress = parent.USBXpress
      
      # tell FrameManager to manage this frame        
      self._mgr = wx.aui.AuiManager()
      self._mgr.SetManagedWindow(self)      
          
      self.TreeControl = self.CreateTreeCtrl()     
      self._mgr.AddPane(self.TreeControl, wx.aui.AuiPaneInfo().
                        Name("Files").Caption("Tree Pane").
                        Left().CloseButton(True).MaximizeButton(True)) 
                        
      self.TextOutput = self.CreateTextCtrl()                  
      self._mgr.AddPane(self.TextOutput, wx.aui.AuiPaneInfo().
                        Name("Output").Caption("Status").
                        Bottom().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))                         
      
      self._mgr.AddPane(self.VtkPane, wx.aui.AuiPaneInfo().Name("VTK window").
                        CenterPane())
      
      self._mgr.Update()
      
      self.VtkSpace1.UpdateSize()
      
      saida = VTK_DATA_ROOT
      saida = 'Plot:' + saida + '\n'
      self.TextOutput.WriteText(saida) 
            
      self.Bind(wx.EVT_SIZE, self.OnSize)
      
      self.Bind(EVT_UPDATE_PLOT, self.OnUpdatePlotArea)
      
    def OnUpdatePlotArea(self, event):
      self.USBXpress.FlushBuffers()
      bufferwrite = [27]*5
      print bufferwrite
      if self.USBXpress.WriteRaw(len(bufferwrite),bufferwrite) == 5:
        while self.USBXpress.CheckRXQueue() == 0:
          sleep(0.1)
        bytestoread = self.USBXpress.CheckRXQueue()
        print 'bites to read: ',bytestoread
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
          
        self.VtkSpace1.UpdateDataPlot(integerdata)      
      
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

        OpacItem = tree.AppendItem(volume3D, "Channel", 1)
        tree.AppendItem(OpacItem, "Ch1", 1)

        ColorItem = tree.AppendItem(root, "Coloração", 0)
        items.append(ColorItem)
        tree.AppendItem(ColorItem, "Green", 1)
        tree.AppendItem(ColorItem, "Ultra-som", 1)
        tree.AppendItem(ColorItem, "Ultra-som BC", 1)
        tree.AppendItem(ColorItem, "Elastografia", 1)

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivate, tree)
        
        self.plot_thread = Plot_Thread(0,self)
        
        tree.Expand(root)
        return tree
    
    def OnItemActivate(self, event):
        item = event.GetItem()
        if self.TreeControl.GetItemText(item) == "Ch1":
          print "clicou ch1"
          if self.plot_thread.IsRunning():
            self.plot_thread.stop()
          else:
            self.plot_thread.start()
                                    
    def OnSelChanged(self, event):
        item = event.GetItem()
        print self.TreeControl.GetItemText(item) 
        event.Skip()    

    def CreateTextCtrl(self):

        text = ("Aplicativo iniciado: %d")%(wxID_FRM)

        return wx.TextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)
             
    def OnSize(self, event):
        self.VtkSpace1.UpdateSize()
        event.Skip()         
        

class ScopeApp(wx.App):
    def __init__(self, parent):
        wx.App.__init__(self,0)
        self.parent = parent
        self.main = ScopeFrm(self.parent)
        self.main.Show()
        self.SetTopWindow(self.main)
        
class ScopeNoShell:
    def __init__(self):
      LogOut = Text(font=('courier', 9, 'normal'))
      Log = CLogger(LogOut, TRUE)           
      self.USBXpress = USBXpress(Log)
      if self.USBXpress.GetDevNumber() > 0:
        if self.USBXpress.IsConnected():
          self.USBXpress.CloseDevice()
        retorno = self.USBXpress.ConnectaDev(0)
        print retorno
        if self.USBXpress.IsConnected():
          application = ScopeApp(self)
          application.MainLoop()            
        
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
    

