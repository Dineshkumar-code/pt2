#Converting Image file into zip file
import zipfile
import os
import glob
import datetime

directory1 = '/home/pi/Desktop/img_sample1'
directory2 = '/home/pi/Desktop/img_sample2'

flag1 = 0
flag2 = 0

#-----------------------------------DirectoryZipping------------------------------------------------

def zip_directory(folder_path, zip_path):
    print("----------zipping started----------")
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])

#----------------------------------DirectorySwapping------------------------------------------------
def main():
    global flag1
    global flag2
    while(True):
       try:
          if(flag1 == 0):
               count1 = len(glob.glob('/home/pi/Desktop/img_sample1/*.jpg'))
               if(count1 == 800):
                   zip_directory(directory1,str('/home/pi/Desktop/zip_folder/') + str(datetime.datetime.now()) + str('.zip'))
                   print("--------Img_sample (1) zipping completed--------")
                   flag1 = 1
                   flag2 = 0
          if(flag2 == 0):
               count2 = len(glob.glob('/home/pi/Desktop/img_sample2/*.jpg'))
               if(count2 == 800):
                   zip_directory(directory2,str('/home/pi/Desktop/zip_folder/') + str(datetime.datetime.now()) + str('.zip'))
                   print("--------Img_sample (2) zipping completed--------")
                   flag1 = 0
                   flag2 = 1
       except Exception as error:
          print("error reason {}", error)

#---------------------------------------main------------------------------------------------------

if __name__ == '__main__':
   main()

#----------------------------------------End------------------------------------------------------
