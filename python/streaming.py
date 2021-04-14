#Image capturing and storing
#Directory - home/pi/Desktop/purethermal1-uvc-capture/python/img_capture.py
"""thermal_image streaming script"""

import datetime
from uvctypes import *
import time
import cv2
import os
import numpy as np
import threading
import glob
import shutil
try:
  from queue import Queue
except ImportError:
  from Queue import Queue
import platform

#------------------------------------------------------------------------

global img_array
global prev_dir
setpoint = 12 # Temprature Setpoint Maximum Limit
max_limit = 800 # Maximum Limit of images captured
count = 0
sample1_count = 0
sample2_count = 0
img_array = []

#------------------------------------------------------------------------

prev_dir = r'/home/pi/Desktop/img_sample1' 
directory1 =  r'/home/pi/Desktop/img_sample1'
os.chdir(directory1)
directory2 = r'/home/pi/Desktop/img_sample2'
capture_directory = r'/home/pi/Desktop/thermal_image'
text_dir = r'/home/pi/Desktop/logger/logger.txt'
BUF_SIZE = 2

#-------------------------------------------------------------------------

for filename in glob.glob(directory1 + str('/*.jpg')):
         os.remove(filename)
for filename in glob.glob(directory2 + str('/*.jpg')):
         os.remove(filename)
q = Queue(BUF_SIZE)

#---------------------------------py_frame_callback--------------------------\

def py_frame_callback(frame, userptr):
  """py_frame_callback"""
  array_pointer = cast(frame.contents.data, POINTER(c_uint16 * (frame.contents.width * frame.contents.height)))
  data = np.frombuffer(array_pointer.contents, dtype=np.dtype(np.uint16)).reshape(frame.contents.height, frame.contents.width)
  if frame.contents.data_bytes != (2 * frame.contents.width * frame.contents.height):
    return
  if not q.full():
    q.put(data)
PTR_PY_FRAME_CALLBACK = CFUNCTYPE(None, POINTER(uvc_frame), c_void_p)(py_frame_callback)

#--------------------------------------------KTOF---------------------------------

def ktof(val):
  """ktof"""
  global temp_f
  temp_f = (1.8 * ktoc(val) + 32.0)
  return temp_f

#----------------------------------------------KTOC-------------------------------

def ktoc(val):
  """ktoc"""
  return (val - 27315) / 100.0

#--------------------------------------------RAW_to_8bit-------------------------

def raw_to_8bit(data):
  """raw_to_8bit"""
  cv2.normalize(data, data, 0, 65535, cv2.NORM_MINMAX)
  np.right_shift(data,8,data)
  return cv2.cvtColor(np.uint8(data), cv2.COLOR_GRAY2RGB)

#-----------------------------------------min_display_temperature---------------

def min_display_temperature(img, val_k, loc, color):
  """min_display_temperature"""
  val = ktof(val_k)
  cv2.putText(img,"{0:.1f} degF".format(val), loc, cv2.FONT_HERSHEY_SIMPLEX, 0.0, color, 2)

#---------------------------------------max_display_temperature-----------------

def max_display_temperature(img, val_k, loc, color):
  """max_display_temperature"""
  val = ktof(val_k)
  cv2.putText(img,"{0:.1f} degF".format(val), loc, cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
  x, y = loc
  cv2.line(img, (x - 2, y), (x + 2, y), color, 1)
  cv2.line(img, (x, y - 2), (x, y + 2), color, 1)

#-------------------------------------videoconversion---------------------------

def videoconversion(imgtype):
  """videoconversion"""
  img_conv = cv2.cvtColor(imgtype,cv2.COLOR_BGR2HSV)
  cv2.imwrite(str(datetime.datetime.now()) + str('.jpg'),img_conv)

#--------------------------------------main-------------------------------------

def main():
  """main"""
  ctx = POINTER(uvc_context)()
  dev = POINTER(uvc_device)()
  devh = POINTER(uvc_device_handle)()
  ctrl = uvc_stream_ctrl()
  res = libuvc.uvc_init(byref(ctx), 0)
  if res < 0:
    print("uvc_init error")
    exit(1)
  try:
    res = libuvc.uvc_find_device(ctx, byref(dev), PT_USB_VID, PT_USB_PID, 0)
    if res < 0:
      print("uvc_device error")
      exit(1)
    try:
      res = libuvc.uvc_open(dev, byref(devh))
      if res < 0:
        print("uvc_open error")
        exit(1)
      print("device opened!")
      print_device_info(devh)
      print_device_formats(devh)
      frame_formats = uvc_get_frame_formats_by_guid(devh, VS_FMT_GUID_Y16)
      if len(frame_formats) == 0:
        print("device does not support Y16")
        exit(1)
      libuvc.uvc_get_stream_ctrl_format_size(devh, byref(ctrl), UVC_FRAME_FORMAT_Y16,
        frame_formats[0].wWidth, frame_formats[0].wHeight, int(1e7 / frame_formats[0].dwDefaultFrameInterval)
      )
      res = libuvc.uvc_start_streaming(devh, byref(ctrl), PTR_PY_FRAME_CALLBACK, None, 0)
      if res < 0:
        print("uvc_start_streaming failed: {0}".format(res))
        exit(1)
      try:
        count = 0
        while True:
          data = q.get(True, 500)
          if data is None:
            break
          data = cv2.resize(data[:,:], (640, 480))
          minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(data)
          img = raw_to_8bit(data)
          min_display_temperature(img, minVal, minLoc, (0, 0, 0))
          minTemp = temp_f
          max_display_temperature(img, maxVal, maxLoc, (0, 0, 255))
          maxTemp = temp_f
          cv2.imshow('Lepton Radiometry', img)
          videoconversion(img)
          count = count +1
          if(count == max_limit):
              global prev_dir
              print("----------Directory moved from (1) to (2)----------")
              os.chdir(directory2)
              prev_dir = directory2
          elif(count == (max_limit*2)):
              count = 0
              global prev_dir
              print("----------Directory moved from (2) to (1)----------")
              os.chdir(directory1)
              prev_dir = directory1
          if maxTemp > (minTemp + setpoint):
              prev_line = "datetime : " +str(datetime.datetime.now()) +" :  "+ "Temp_raised to " +" : " + str(maxTemp) +" in Fahrenheit"
              f = open(text_dir,"a+")
              f.write(prev_line + '\n')
              img2hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
              os.chdir(capture_directory)
              global prev_dir
              cv2.imwrite(str(datetime.datetime.now()) + str('.jpg'),img2hsv)
              os.chdir(prev_dir)
          cv2.waitKey(1)
        out.release()
        cv2.destroyAllWindows()
      finally:
        libuvc.uvc_stop_streaming(devh)
      print("done")
    finally:
      libuvc.uvc_unref_device(dev)
  finally:
    libuvc.uvc_exit(ctx)

#---------------------------------------MAIN---------------------------------
    
if __name__ == '__main__':
  main()

#-------------------------------------------------end------------------------------
