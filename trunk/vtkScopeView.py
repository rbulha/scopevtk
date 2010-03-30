import vtk
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor

class VtkSNRender(vtk.vtkRenderer):
    def __init__(self, nome):
      #vtk.vtkRenderer.__init__(self)
      self.label_t = nome
      self.scree_text_offset = 10
      self.text_label = vtk.vtkTextActor()
      self.ShowLabel()
    def SetMode(self, mode):
      if mode == 'scope':
        self.SetBackground(0.1, 0.2, 0.4)
      elif mode == '8chScope':          
        self.SetBackground(0.1, 0.2, 0.32)
    def SetQuadrant(self, Quadrant):
      if Quadrant == '1_8chScope': #1st Top ch
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.875, 1.0, 1.0)
        self.SetBackground(0.1, 0.2, 0.35)
      elif Quadrant == '2_8chScope': #1st Top ch
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.750, 1.0, 0.875)
        self.SetBackground(0.1, 0.2, 0.35)
      elif Quadrant == '3_8chScope': #1st Top ch
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.625, 1.0, 0.750)
        self.SetBackground(0.1, 0.2, 0.35)
      elif Quadrant == '4_8chScope': #1st Top ch
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.5, 1.0, 0.625)
        self.SetBackground(0.1, 0.2, 0.35)
      elif Quadrant == '5_8chScope': #1st Top ch
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.375, 1.0, 0.5)
        self.SetBackground(0.1, 0.2, 0.35)
      elif Quadrant == '6_8chScope': #1st Top ch
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.25, 1.0, 0.375)
        self.SetBackground(0.1, 0.2, 0.35)
      elif Quadrant == '7_8chScope': #1st Top ch
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.125, 1.0, 0.25)
        self.SetBackground(0.1, 0.2, 0.35)     
      elif Quadrant == '8_8chScope': #1st Top ch
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.0, 1.0, 0.125)
        self.SetBackground(0.1, 0.2, 0.35)                                                        
      elif Quadrant == 'BL': #Botton left
        #(xmin,ymin,xmax,ymax)
        self.SetViewport(0.0, 0.0, 0.5, 0.5)
        self.SetBackground(0.1, 0.2, 0.4)
      elif Quadrant == 'TL': #Top left
        self.SetViewport(0.0, 0.5, 0.5, 1.0)
        self.SetBackground(0.1, 0.2, 0.5)
      elif Quadrant == 'BR': #Botton right          
        self.SetViewport(0.5, 0.0, 1.0, 0.5)
        self.SetBackground(0.1, 0.2, 0.6)
      elif Quadrant == 'TR': #Top right           
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
    def SetLabel(self, nome):
      self.label_t = nome
      self.text_label.SetInput(self.label_t)
    def ShowLabel(self):
      self.tprop = vtk.vtkTextProperty()
      size = self.GetSize()
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
      
class VtkSpace:
    def __init__(self, parent,title,nchannel=1):
      self.Parent = parent
      self.nchannel = nchannel
      self.iren = wxVTKRenderWindowInteractor(self.Parent,-1,size = self.Parent.GetSize())
      self.iren.SetPosition((0,0))
      self.renwin = self.iren.GetRenderWindow()
      self.renwin.StereoCapableWindowOn()
      self.renwin.StereoRenderOff()
      self.renScope = {}
      self.mode = '%dchScope'%nchannel
      for i in range(nchannel):
          name = '%d_%dchScope'%(i+1,nchannel)
          self.renScope[i] = {}
          new_render = VtkSNRender(name)  
          new_render.SetMode(self.mode)
          new_render.SetQuadrant(name)
          self.renwin.AddRenderer(new_render)
          self.renScope[i]['render'] = new_render
          self.renScope[i]['name'] = name
      
      #Constantes de tela
      self.H_MAX = 800
      self.V_MAX = 1030
      
      self.V_MAX_UNIT = 100.0
      self.H_MAX_UNIT = 1.0 
      
      self.V_DIG_MAX_UNIT = 10.0
      self.H_DIG_MAX_UNIT = 4098

      for render in self.renScope:
          self.renScope[render]['points'] = vtk.vtkPoints()
          self.renScope[render]['values'] = vtk.vtkFloatArray()
          
          self.PontosNaTela = 0
          
          self.renScope[render]['values'].SetName("Values")
          toggle = 0.0
          edge = 500
          #For fast render time
          self.renScope[render]['points'].SetNumberOfPoints(self.H_DIG_MAX_UNIT)
          self.renScope[render]['values'].SetNumberOfValues(self.H_DIG_MAX_UNIT)
          for i in range(self.H_DIG_MAX_UNIT):
            #self.renScope[render]['points'].InsertPoint(i,0,0,0)
            #self.renScope[render]['values'].InsertValue(i,toggle)
            #For fast render time in conjuction with SetNumberOfPoints and SetNumberOfValues
            self.renScope[render]['points'].SetPoint(i,0,0,0)
            self.renScope[render]['values'].SetValue(i,toggle)
            if i == edge:
              if toggle:
                toggle = 0.0
              else:  
                toggle = self.V_MAX_UNIT/2
              edge = edge + 500
            self.PontosNaTela += 1 

          self.renScope[render]['polydata'] = vtk.vtkPolyData()
          self.renScope[render]['polydata'].SetPoints(self.renScope[render]['points'])
          self.renScope[render]['polydata'].GetPointData().SetScalars(self.renScope[render]['values'])
          self.renScope[render]['xyplot'] = vtk.vtkXYPlotActor()
          self.renScope[render]['xyplot'].AddInput(self.renScope[render]['polydata'])
          self.renScope[render]['xyplot'].GetProperty().SetColor(0, 1, 0)
          self.renScope[render]['xyplot'].GetProperty().SetLineWidth(1)
          self.renScope[render]['xyplot'].GetProperty().SetPointSize(2)
          
          self.renScope[render]['xyplot'].GetAxisLabelTextProperty().SetFontSize(1)
          self.renScope[render]['xyplot'].GetAxisLabelTextProperty().BoldOff()
          
          self.renScope[render]['xyplot'].PlotPointsOn()
          self.renScope[render]['xyplot'].PlotLinesOn()
          
          self.renScope[render]['xyplot'].SetTitle(title)
          self.renScope[render]['xyplot'].SetXTitle("")
          self.renScope[render]['xyplot'].SetYTitle("")
          self.renScope[render]['xyplot'].GetPositionCoordinate().SetValue(0.02, 0.1, 0)
          self.renScope[render]['xyplot'].GetPosition2Coordinate().SetValue(0.99, 0.9, 0)
          
          #self.renScope[render]['plotwidget'] = vtk.vtkXYPlotWidget()
          #self.renScope[render]['plotwidget'].SetXYPlotActor(self.renScope[render]['xyplot'])
          #self.renScope[render]['plotwidget'].SetInteractor(self.iren)
          self.renScope[render]['render'].AddActor2D(self.renScope[render]['xyplot'])
        
    def SetDigitalPlotRange(self):
      self.h_max = self.H_DIG_MAX_UNIT
      self.h_min = 0
      self.v_min = 0
      self.v_max = self.V_DIG_MAX_UNIT  
      for render in self.renScope: 
          self.renScope[render]['xyplot'].SetPlotRange(0,0,0,0)           
          #self.renScope[render]['xyplot'].SetXRange(0,self.H_DIG_MAX_UNIT)
          #self.renScope[render]['xyplot'].SetYRange(0,self.V_DIG_MAX_UNIT)
      self.renwin.Render()
    def SetXPlotMaxVisible(self,channel,x_max):
        channel = channel - 1
        if channel >= 0:    
            self.renScope[channel]['xyplot'].SetPlotRange(0,0,x_max,0)
            self.renwin.Render()   
    def SetPlotRange(self,h_min, h_max,v_min, v_max):
      self.h_max = h_max
      self.h_min = h_min
      self.v_min = v_min
      self.v_max = v_max
      for render in self.renScope: 
          self.renScope[render]['xyplot'].SetPlotRange(0,0,0,0)
          #self.renScope[render]['xyplot'].SetXRange(h_min,h_max)
          #self.renScope[render]['xyplot'].SetYRange(v_min,v_max) 
      self.renwin.Render()
    def SetDataRange(self,h_max,h_max_unit,v_max,v_max_unit):   
      self.H_MAX = h_max
      self.V_MAX = v_max
      self.V_MAX_UNIT = h_max_unit
      self.H_MAX_UNIT = v_max_unit
      for render in self.renScope:
          self.renScope[render]['xyplot'].SetPlotRange(0,0,0,0) 
          #self.renScope[render]['xyplot'].SetXRange(0,h_max)
          #self.renScope[render]['xyplot'].SetYRange(0,v_max_unit) 
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
      for render in self.renScope: 
        self.renScope[render]['render'].UpdateSize()

    def UpdateLabel(self, nome):
        for render in self.renScope:
            self.renScope[render]['render'].SetLabel(nome)
      
    def GetActiveVolume(self):
      return self.Vol3D
    
    def Points(self, mode):
        for render in self.renScope:
          if self.renScope[render]['xyplot'].GetPlotPoints():
            self.renScope[render]['xyplot'].PlotPointsOff()
            return 0
          else:  
            self.renScope[render]['xyplot'].PlotPointsOn()
            return 1
      
    def Lines(self, mode):
        for render in self.renScope:
          if self.renScope[render]['xyplot'].GetPlotLines():
            self.renScope[render]['xyplot'].PlotLinesOff()
            return 0 
          else:
            self.renScope[render]['xyplot'].PlotLinesOn()
            return 1   
    
    def UpdateDataPlot(self, data, channel):
      channel = channel - 1
      if channel >= 0:
          print '[UpdateDataPlot] ch=%d, render=%s'%(channel,self.renScope[channel]['name'])
          self.renScope[channel]['points'] = vtk.vtkPoints()
          self.renScope[channel]['points'].SetNumberOfPoints(len(data))
            
          self.renScope[channel]['values'] = vtk.vtkFloatArray()
          self.renScope[channel]['values'].SetName("Values")
          self.renScope[channel]['values'].SetNumberOfValues(len(data))
          for i,value in enumerate(data):
            unit_value = (float(value)/self.V_MAX)*self.V_MAX_UNIT
            #self.renScope[channel]['values'].InsertNextValue(unit_value)
            self.renScope[channel]['points'].SetPoint(i,0,0,0)
            self.renScope[channel]['values'].SetValue(i,unit_value)
          self.renScope[channel]['polydata'].SetPoints(self.renScope[channel]['points'])  
          self.renScope[channel]['polydata'].GetPointData().SetScalars(self.renScope[channel]['values'])
          #self.renScope[channel]['xyplot'].SetPlotRange(0,0,0,0)
          self.renwin.Render()
