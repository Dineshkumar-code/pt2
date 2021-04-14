import ftplib
import os
import glob
i = 0
file_list = []

HOSTNAME = "ftpupload.net"
USERNAME = "epiz_28362902"
PASSWORD = "Y6OlM622SK8StqT"

ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

ftp_server.encoding = "utf-8"

# Enter File Name with Extension
count1 = len(glob.glob('/home/pi/Desktop/tempfolder/*.txt'))
print(count1)
os.chdir('/home/pi/Desktop/tempfolder/')
for filename in glob.glob('*.txt'):
     print(filename)
     file_list.append(filename)
     file_list.sort()
for i in range(count1 - 1):
     filename = file_list[i]
     print("uploading file list : ",filename)
     with open(filename, "rb") as file:
         ftp_server.cwd('/htdocs')
         print("inside loop",file)
         ftp_server.storbinary(f"STOR {filename}", file)


ftp_server.dir()
#ftp_server.delete("How to Use a PureThermal 2 on Mac OS.mp4") 
ftp_server.quit()
