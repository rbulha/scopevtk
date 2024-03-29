# This file was automatically generated by pywxrc.
# -*- coding: UTF-8 -*-

import wx
import wx.xrc as xrc

__res = None

def get_resources():
    """ This function provides access to the XML resources in this module."""
    global __res
    if __res == None:
        __init_resources()
    return __res




class xrcAnalog(wx.Panel):
#!XRCED:begin-block:xrcAnalog.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcAnalog.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PrePanel()
        self.PreCreate(pre)
        get_resources().LoadOnPanel(pre, parent, "Analog")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.Button_onoff_analog = xrc.XRCCTRL(self, "Button_onoff_analog")
        self.Slider_zoom = xrc.XRCCTRL(self, "Slider_zoom")
        self.Slider_position = xrc.XRCCTRL(self, "Slider_position")
        self.Check_trigger = xrc.XRCCTRL(self, "Check_trigger")



class xrcConfiguracao(wx.Panel):
#!XRCED:begin-block:xrcConfiguracao.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcConfiguracao.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PrePanel()
        self.PreCreate(pre)
        get_resources().LoadOnPanel(pre, parent, "Configuracao")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.Combo_devices = xrc.XRCCTRL(self, "Combo_devices")
        self.Button_conect = xrc.XRCCTRL(self, "Button_conect")
        self.Button_disconnect = xrc.XRCCTRL(self, "Button_disconnect")
        self.Button_refresh_devices = xrc.XRCCTRL(self, "Button_refresh_devices")
        self.wx_combo_serial_list = xrc.XRCCTRL(self, "wx_combo_serial_list")
        self.wxConnectSerial = xrc.XRCCTRL(self, "wxConnectSerial")
        self.wxDisconnectSerial = xrc.XRCCTRL(self, "wxDisconnectSerial")
        self.wxButtonRefreshSerial = xrc.XRCCTRL(self, "wxButtonRefreshSerial")
        self.wxInitiateView = xrc.XRCCTRL(self, "wxInitiateView")

        self.Bind(wx.EVT_COMBOBOX, self.OnCombobox_Combo_devices, self.Combo_devices)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText_enter_Combo_devices, self.Combo_devices)
        self.Bind(wx.EVT_BUTTON, self.OnButton_wxConnectSerial, self.wxConnectSerial)
        self.Bind(wx.EVT_BUTTON, self.OnButton_wxDisconnectSerial, self.wxDisconnectSerial)
        self.Bind(wx.EVT_BUTTON, self.OnButton_wxButtonRefreshSerial, self.wxButtonRefreshSerial)
        self.Bind(wx.EVT_BUTTON, self.OnButton_wxInitiateView, self.wxInitiateView)

#!XRCED:begin-block:xrcConfiguracao.OnCombobox_Combo_devices
    def OnCombobox_Combo_devices(self, evt):
        # Replace with event handler code
        print "OnCombobox_Combo_devices()"
#!XRCED:end-block:xrcConfiguracao.OnCombobox_Combo_devices        

#!XRCED:begin-block:xrcConfiguracao.OnText_enter_Combo_devices
    def OnText_enter_Combo_devices(self, evt):
        # Replace with event handler code
        print "OnText_enter_Combo_devices()"
#!XRCED:end-block:xrcConfiguracao.OnText_enter_Combo_devices        

#!XRCED:begin-block:xrcConfiguracao.OnButton_wxConnectSerial
    def OnButton_wxConnectSerial(self, evt):
        # Replace with event handler code
        print "OnButton_wxConnectSerial()"
#!XRCED:end-block:xrcConfiguracao.OnButton_wxConnectSerial        

#!XRCED:begin-block:xrcConfiguracao.OnButton_wxDisconnectSerial
    def OnButton_wxDisconnectSerial(self, evt):
        # Replace with event handler code
        print "OnButton_wxDisconnectSerial()"
#!XRCED:end-block:xrcConfiguracao.OnButton_wxDisconnectSerial        

#!XRCED:begin-block:xrcConfiguracao.OnButton_wxButtonRefreshSerial
    def OnButton_wxButtonRefreshSerial(self, evt):
        # Replace with event handler code
        print "OnButton_wxButtonRefreshSerial()"
#!XRCED:end-block:xrcConfiguracao.OnButton_wxButtonRefreshSerial        

#!XRCED:begin-block:xrcConfiguracao.OnButton_wxInitiateView
    def OnButton_wxInitiateView(self, evt):
        # Replace with event handler code
        print "OnButton_wxInitiateView()"
#!XRCED:end-block:xrcConfiguracao.OnButton_wxInitiateView        


class xrcSonarRanging(wx.Panel):
#!XRCED:begin-block:xrcSonarRanging.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcSonarRanging.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PrePanel()
        self.PreCreate(pre)
        get_resources().LoadOnPanel(pre, parent, "SonarRanging")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.Spin_cycles = xrc.XRCCTRL(self, "Spin_cycles")
        self.Button_send_pulse = xrc.XRCCTRL(self, "Button_send_pulse")
        self.Slider_zoom = xrc.XRCCTRL(self, "Slider_zoom")



class xrcTSW1250Panel(wx.Panel):
#!XRCED:begin-block:xrcTSW1250Panel.PreCreate
    def PreCreate(self, pre):
        """ This function is called during the class's initialization.
        
        Override it for custom setup before the window is created usually to
        set additional window styles using SetWindowStyle() and SetExtraStyle().
        """
        pass
        
#!XRCED:end-block:xrcTSW1250Panel.PreCreate

    def __init__(self, parent):
        # Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
        pre = wx.PrePanel()
        self.PreCreate(pre)
        get_resources().LoadOnPanel(pre, parent, "TSW1250Panel")
        self.PostCreate(pre)

        # Define variables for the controls, bind event handlers
        self.wxChannelSelector = xrc.XRCCTRL(self, "wxChannelSelector")
        self.wxChCaptureButton = xrc.XRCCTRL(self, "wxChCaptureButton")
        self.wxCheckChSimulation = xrc.XRCCTRL(self, "wxCheckChSimulation")
        self.wxXRangeSlider = xrc.XRCCTRL(self, "wxXRangeSlider")

        self.Bind(wx.EVT_BUTTON, self.OnButton_wxChCaptureButton, self.wxChCaptureButton)
        self.Bind(wx.EVT_SCROLL, self.OnScroll_wxXRangeSlider, self.wxXRangeSlider)

#!XRCED:begin-block:xrcTSW1250Panel.OnButton_wxChCaptureButton
    def OnButton_wxChCaptureButton(self, evt):
        # Replace with event handler code
        print "OnButton_wxChCaptureButton()"
#!XRCED:end-block:xrcTSW1250Panel.OnButton_wxChCaptureButton        

#!XRCED:begin-block:xrcTSW1250Panel.OnScroll_wxXRangeSlider
    def OnScroll_wxXRangeSlider(self, evt):
        # Replace with event handler code
        print "OnScroll_wxXRangeSlider()"
#!XRCED:end-block:xrcTSW1250Panel.OnScroll_wxXRangeSlider        




# ------------------------ Resource data ----------------------

def __init_resources():
    global __res
    __res = xrc.EmptyXmlResource()

    __res.Load('FrameLateral.xrc')
