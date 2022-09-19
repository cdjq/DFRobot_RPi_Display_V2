# -*- coding: utf-8 -*
""" 
  @file DFRobot_Epaper.py
  @brief Define the basic structure of class DFRobot_Epaper 
  @details 该类提供初始化墨水屏的代码和发送指令的函数
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @License     The MIT License (MIT)
  @author [fengli](li.feng@dfrobot.com)
  @version  V1.0
  @date  2022-6-09
  @url https://github.com/DFRobot/DFRobot_RPi_Display_V2
"""
import time

import sys
sys.path.append("..")
import RPi.GPIO as RPIGPIO
from DFRobot_display.DFRobot_display import DFRobot_Display
from display_extension import fonts_8_16 as fonts_ABC

try:
  from DFRobot_interface.raspberry.spi import SPI
  from DFRobot_interface.raspberry.gpio import GPIO
except:
  print("unknow platform")
  exit()

CONFIG_IL0376F = {

}

CONFIG_IL3895 = {
  
}


class DFRobot_Epaper(DFRobot_Display):

  XDOT = 128
  YDOT = 250
  GDEH0213B72  = 3
  GDEH0213B1   = 2
  FULL = True
  PART = False
  VERSION = GDEH0213B72

  def __init__(self, width = 250, height = 122):
    '''!
      @fn __init__
      @brief init function
      @param width 屏幕的宽度
      @param height 屏幕的高度
    '''
    DFRobot_Display.__init__(self, width, height)
    # length = width * height // 8
    length = 4000
    self._displayBuffer = bytearray(length)
    i = 0
    while i < length:
      self._displayBuffer[i] = 0xff
      i = i + 1

    self._isBusy = False
    self._busyExitEdge = GPIO.RISING
    
    self._fonts.setFontsABC(fonts_ABC)
    self.setExFontsFmt(16, 16)

  def _busyCB(self, channel):
    self._isBusy = False

  def setBusyExitEdge(self, edge):
    if edge != GPIO.HIGH and edge != GPIO.LOW:
      return
    self._busyEdge = edge

  def begin(self):
    '''!
      @fn begin
      @brief 获取树莓派墨水屏的ID
    '''
    version = self.readID()
    if(version[0] == 0x01):
       self.VERSION = self.GDEH0213B1
    else:
       self.VERSION = self.GDEH0213B72
    #self._init()
    #self._powerOn()
    #self.setBusyCB(self._busyCB)
    #self._powerOn()


  def pixel(self, x, y, color):
    '''!
      @fn pixel
      @brief 在屏幕的(x,y)坐标画一个点
      @param x x轴坐标
      @param y y轴坐标
    '''
    if x < 0 or x >= self._width:
      return
    if y < 0 or y >= self._height:
      return
    x = int(x)
    y = int(y)
    m = int(x * 16 + (y + 1) / 8)
    sy = int((y + 1) % 8)
    if color == self.WHITE:
      if sy != 0:
        self._displayBuffer[m] = self._displayBuffer[m] | int(pow(2, 8 - sy))
      else:
        self._displayBuffer[m - 1] = self._displayBuffer[m - 1] | 1
    elif color == self.BLACK:
      if sy != 0:
        self._displayBuffer[m] = self._displayBuffer[m] & (0xff - int(pow(2, 8 - sy)))
      else:
        self._displayBuffer[m - 1] = self._displayBuffer[m - 1] & 0xfe

  def _initLut(self, mode):
    if self.VERSION == self.GDEH0213B72:
      if mode == self.FULL:
        
        self.writeCmdAndData(0x32, [  0x80,0x60,0x40,0x00,0x00,0x00,0x00,           
                                      0x10,0x60,0x20,0x00,0x00,0x00,0x00,             
                                      0x80,0x60,0x40,0x00,0x00,0x00,0x00,            
                                      0x10,0x60,0x20,0x00,0x00,0x00,0x00,           
                                      0x00,0x00,0x00,0x00,0x00,0x00,0x00,            
      
                                             0x03,0x03,0x00,0x00,0x02,                       
                                             0x09,0x09,0x00,0x00,0x02,                       
                                             0x03,0x03,0x00,0x00,0x02,                     
                                             0x00,0x00,0x00,0x00,0x00,                       
                                             0x00,0x00,0x00,0x00,0x00,                     
                                             0x00,0x00,0x00,0x00,0x00,                       
                                             0x00,0x00,0x00,0x00,0x00,                       
                 
                                    ])
      elif mode == self.PART:
        self.writeCmdAndData(0x32, [0x00,0x00,0x00,0x00,0x00,0x00,0x00,             
                                    0x80,0x00,0x00,0x00,0x00,0x00,0x00,             
                                    0x40,0x00,0x00,0x00,0x00,0x00,0x00,             
                                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,             
                                    0x00,0x00,0x00,0x00,0x00,0x00,0x00,             
      
                                        0x0A,0x00,0x00,0x00,0x00,                      
                                        0x00,0x00,0x00,0x00,0x00,                       
                                        0x00,0x00,0x00,0x00,0x00,                      
                                        0x00,0x00,0x00,0x00,0x00,                       
                                        0x00,0x00,0x00,0x00,0x00,                       
                                        0x00,0x00,0x00,0x00,0x00,                      
                                        0x00,0x00,0x00,0x00,0x00,     
	  									              ])
    elif self.VERSION == self.GDEH0213B1:
      if mode == self.FULL:
        self.writeCmdAndData(0x32, [  0xA0,	0x90,	0x50,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
                                      0x50,	0x90,	0xA0,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
                                      0xA0,	0x90,	0x50,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
                                      0x50,	0x90,	0xA0,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
                                      0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,
	  
                                      0x0F,	0x0F,	0x00,	0x00,	0x00,		
                                      0x0F,	0x0F,	0x00,	0x00,	0x03,		
                                      0x0F,	0x0F,	0x00,	0x00,	0x00,		
                                      0x00,	0x00,	0x00,	0x00,	0x00,	
                                      0x00,	0x00,	0x00,	0x00,	0x00,
                                      0x00,	0x00,	0x00,	0x00,	0x00,
                                      0x00,	0x00,	0x00,	0x00,	0x00,	 
                                      0x00,	0x00,	0x00,	0x00,	0x00,		
                                      0x00,	0x00,	0x00,	0x00,	0x00,		
                                      0x00,	0x00,	0x00,	0x00,	0x00,		
                                    ])
      elif mode == self.PART:
        self.writeCmdAndData(0x32, [0xA0,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00, 0x00,	0x00,	0x00,	
                                    0x50,	0x00,	0x00,	0x00,	0x00,	0x00, 0x00,	0x00,	0x00,	0x00,	
                                    0xA0,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	
                                    0x50,	0x00, 0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	
                                    0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00,	0x00, 0x00,	0x00,	
	  
                                      0x0f,	0x00,	0x00,	0x00,	0x00,		
                                      0x0,	0x00,	0x00,	0x00,	0x00,		
                                      0x0,	0x00,	0x00,	0x00,	0x00,		
                                      0x00,	0x00,	0x00,	0x00,	0x00,	
                                      0x00,	0x00,	0x00,	0x00,	0x00,
                                      0x00,	0x00,	0x00,	0x00,	0x00,
                                      0x00,	0x00,	0x00,	0x00,	0x00,	 
                                      0x00,	0x00,	0x00,	0x00,	0x00,		
                                      0x00,	0x00,	0x00,	0x00,	0x00,		
                                      0x00,	0x00,	0x00,	0x00,	0x00,		
	  									              ])

  def _setRamData(self, xStart, xEnd, yStart, yStart1, yEnd, yEnd1):
    self.writeCmdAndData(0x44, [xStart, xEnd])
    self.writeCmdAndData(0x45, [yStart, yStart1, yEnd, yEnd1])

  def _setRamPointer(self, x, y, y1):
    self.writeCmdAndData(0x4e, [x])
    self.writeCmdAndData(0x4f, [y, y1])

  def _init(self,mode):
    if self.VERSION == self.GDEH0213B72:
      if mode == self.FULL:
        time.sleep(0.1)
        self.writeCmdAndData(0x12, [])
        time.sleep(0.1)
        self.writeCmdAndData(0x74, [0x54])
        self.writeCmdAndData(0x7e, [0x3b])
        self.writeCmdAndData(0x01, [0xf9, 0x00, 0x00])
        self.writeCmdAndData(0x11, [0x01])
      
        self._setRamData(0x00, 0x0f, 0xf9,0x00, 0x00, 0x00)
        
        self.writeCmdAndData(0x3c, [0x03])   
         
        #self.writeCmdAndData(0x21, [0x08])
        self.writeCmdAndData(0x2c, [0x55])
        self.writeCmdAndData(0x03, [0x15])
        self.writeCmdAndData(0x04, [0x41,0xa8,0x32])
        self.writeCmdAndData(0x3a, [0x30])
        self.writeCmdAndData(0x3b, [0x0a])
        self._initLut(self.FULL)
        #self.writeCmdAndData(0x0c, [0x8b,0x9c,0x96,0x0f])
        self._setRamPointer(0x00, 0xF9, 0x00) 
        time.sleep(0.1)
      elif mode == self.PART:
      
        self.writeCmdAndData(0x2C, [0x26])
        self._initLut(self.PART)
        self.writeCmdAndData(0x37, [0x00,0x00,0x00,0x00,0x40,0x00,0x00])
        self.writeCmdAndData(0x22, [0xC0])
        self.writeCmdAndData(0x20, [])
        self.writeCmdAndData(0x3C, [0x01])
        time.sleep(0.1)
    elif self.VERSION == self.GDEH0213B1:
        self.writeCmdAndData(0x12, [])
        self.writeCmdAndData(0x01, [0xf9, 0x00, 0x00])
        self.writeCmdAndData(0x74, [0x54])
        self.writeCmdAndData(0x7e, [0x3b])
        self.writeCmdAndData(0x11, [0x01])
        self._setRamData(0x00, 0x0f, 0xf9,0x00, 0x00, 0x00)
        self.writeCmdAndData(0x3c, [0x03])   
        self._setRamPointer(0x00, 0xf9, 0x00)  
        self.writeCmdAndData(0x21, [0x08])
        self.writeCmdAndData(0x2c, [0x50])
        self.writeCmdAndData(0x03, [0x15])
        self.writeCmdAndData(0x04, [0x41,0xa8,0x32])
        self.writeCmdAndData(0x3a, [0x2c])
        self.writeCmdAndData(0x3b, [0x0b])
        self.writeCmdAndData(0x0c, [0x8b,0x9c,0x96,0x0f])
        self._initLut(mode)
  def _writeDisRam(self, sizeX, sizeY):
    if sizeX % 8 != 0:
      sizeX = sizeX + (8 - sizeX % 8)
    sizeX = sizeX // 8
    
    self.writeCmdAndData(0x24, self._displayBuffer[0: sizeX * sizeY])



  def _updateDis(self, mode):
    if mode == self.FULL:
    
     self.writeCmdAndData(0x22, [0xc7])
    elif mode == self.PART:
          if self.VERSION == self.GDEH0213B72:
             self.writeCmdAndData(0x22, [0x0C])
          elif self.VERSION == self.GDEH0213B1:
             self.writeCmdAndData(0x22, [0xc7])
    else:
      return
    self.writeCmdAndData(0x20, [])
  

  def _waitBusyExit(self):
    temp = 0
    while self.readBusy() != False:
      time.sleep(0.01)
      temp = temp + 1
      if (temp % 200) == 0:
        print("waitBusyExit")

  def _powerOn(self):
    self.writeCmdAndData(0x22, [0xC0])
    self.writeCmdAndData(0x20, [])

  def _powerOff(self):
    self.writeCmdAndData(0x10, [0x01])
    time.sleep(0.1)

  def _disPart(self, xStart, xEnd, yStart, yEnd):
    self._setRamData(xStart // 8, xEnd // 8, yEnd % 256, yEnd // 256, yStart % 256, yStart // 256)
    self._setRamPointer(xStart // 8, yEnd % 256, yEnd // 256)
    self._writeDisRam(xEnd - xStart, yEnd - yStart + 1)
    self._updateDis(self.PART)

  def flush(self, mode):
    '''!
      @fn flush
      @brief 把已经准备好的屏幕图像buffer发送出去,显示到墨水屏
      @param mode 显示的模式FULL:全屏刷新,PART:局部刷新
    '''
    if mode != self.FULL and mode != self.PART:
      return
    self._init(mode)
    #self._powerOn()
    if mode == self.PART:
      self._disPart(0, self.XDOT - 1, 0, self.YDOT - 1)
    else:
      #self._setRamPointer(0x00, (self.YDOT - 1) % 256, (self.YDOT - 1) // 256)
      self._writeDisRam(self.XDOT, self.YDOT)
      self._updateDis(self.FULL)
   
  def startDrawBitmapFile(self, x, y):
    '''!
      @fn startDrawBitmapFile
      @brief 绘制位图
      @param x 位图起始x坐标
      @param y 位图起始y坐标
    '''
    self._bitmapFileStartX = x
    self._bitmapFileStartY = y

  def bitmapFileHelper(self, buf):
    '''!
      @fn bitmapFileHelper
      @brief 将位图数据buffer按规则移到到屏幕图像buffer
      @param buf 待发送位图数据buffer
    '''
    for i in range(len(buf) // 3):
      addr = i * 3
      if buf[addr] == 0x00 and buf[addr + 1] == 0x00 and buf[addr + 2] == 0x00:
        self.pixel(self._bitmapFileStartX, self._bitmapFileStartY, self.BLACK)
      else:
        self.pixel(self._bitmapFileStartX, self._bitmapFileStartY, self.WHITE)
      self._bitmapFileStartX += 1
  
  def endDrawBitmapFile(self):
    '''!
      @fn endDrawBitmapFile
      @brief 把已经准备好的屏幕图像buffer发送出去,显示位图到墨水屏
    '''
    self.flush(self.PART)
    
  def clearScreen(self):
    '''!
      @fn clearScreen
      @brief 清除墨水屏上显示的东西
    '''
    self.clear(self.WHITE)
  
    self.flush(self.FULL)
    if self.VERSION == self.GDEH0213B72:
         self.flush(self.PART)
         time.sleep(0.1)
    elif self.VERSION == self.GDEH0213B1:
         time.sleep(0.1)
    
    
  def setVersion(self,version):
    '''!
      @fn setVersion
      @brief 手动设置屏幕的版本号
    '''
    self.VERSION = version
  def readID(self):
    '''!
      @fn clearScreen
      @brief 读取墨水屏的ID
    '''
    self.writeCmdAndData(0x2f, [])
    return self.readData(1)

class DFRobot_Epaper_SPI(DFRobot_Epaper):
  
  def __init__(self, bus, dev, cs, cd, busy):
    DFRobot_Epaper.__init__(self)
    self._busy = GPIO(busy, GPIO.IN)
    self._spi = SPI(bus, dev)
    self._cs = GPIO(cs, GPIO.OUT)
    self._cd = GPIO(cd, GPIO.OUT)
    
  
  def writeCmdAndData(self, cmd, data = []):
    self._waitBusyExit()
    self._cs.setOut(GPIO.LOW)
    self._cd.setOut(GPIO.LOW)
    self._spi.transfer([cmd])
    if len(data):
      self._cd.setOut(GPIO.HIGH)
      self._spi.transfer(data)
    self._cs.setOut(GPIO.HIGH)

  def readBusy(self):
    return self._busy.read()
    #time.sleep(0.1)
  def readData(self,n):
    self._cs.setOut(GPIO.LOW)
    self._cd.setOut(GPIO.HIGH)
    data = self._spi.readData(n)
    self._cs.setOut(GPIO.HIGH)
    return data

  def setBusyCB(self, cb):
    self._busy.setInterrupt(self._busyExitEdge, cb)
  def __del__(self):
    RPIGPIO.cleanup()