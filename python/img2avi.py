#Image to video conversion (.avi format)
import cv2
import numpy as np
import glob
import os
import datetime

#-----------------------------------------------------------------

max_limit = 800 # Maximum Limit of images converted during conversion
file_list = []
img_array = []
count1 = 0
count2 = 0

#-----------------------------------------------------------------------

video_name = '/home/pi/Desktop/pt2_vid/'
pass_directory1 = '/home/pi/Desktop/img_sample1/*.jpg'
pass_directory2 = '/home/pi/Desktop/img_sample2/*.jpg'

#-------------------------------------------Imageconversion------------------------------------------

def img_conversion(directory):
    """Imageconversion"""
    for filename in glob.glob(directory):
        file_list.append(filename)
        file_list.sort()
    for i in file_list:
        frame = cv2.imread(i)
        img_array.append(frame)
    video = cv2.VideoWriter(video_name + str(datetime.datetime.now()) + str('.avi'), cv2.VideoWriter_fourcc(*'DIVX'), 8, (640,480))
    for i in range(len(img_array)):
        img_trs = i
        video.write(img_array[i])
    print("Image Transfered : ",img_trs + 1)
    cv2.destroyAllWindows()
    video.release()
    del file_list [:]
    del img_array [:]
    for filename in glob.glob(directory):
         os.remove(filename)

#------------------------------------------main----------------------------------------
         
def main():
    """main"""
    while (True):
        try:
            count1 = len(glob.glob('/home/pi/Desktop/img_sample1/*.jpg'))
            if(count1 >= max_limit):
                img_conversion(pass_directory1)
                print("--------------pass_directory-(1)---------------")
                count1 = 0
            count2 = len(glob.glob('/home/pi/Desktop/img_sample2/*.jpg'))
            if(count2 >= max_limit):
                img_conversion(pass_directory2)
                print("-------------pass_directory-(2)----------------")
                count2 = 0
        except Exception as error:
            print("exception reason {}",error)
        
        
#---------------------------------------MAIN---------------------------------
    
if __name__ == '__main__':
  main()

#-------------------------------------End------------------------------------
