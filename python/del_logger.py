# Delete maximum temprature logging periodically

import os
import time
from datetime import datetime
from time import strftime
import requests
from pytz import timezone, utc
deletion_hr  = 0.5 # Periodic time for deletion (in hrs)
deletion_sec =  deletion_hr *3600

#----------------------------------------Customtime--------------------------------------

def custom_time():
    """CUSTOM TIME"""
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("Asia/Kolkata")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()

#-------------------------------------Logfileremoving-------------------------------------

prev = 0
while(True):
    date  = datetime.utcnow()
    if(int(date.strftime("%s")) - int(prev) > deletion_sec):
        print("----------Log file removed----------")
        path = "/home/pi/Desktop/logger/logger.txt"
        if os.path.exists(path):
            os.remove(path)
        else:
            print("x----x-----x-----The file does not exist------x------x----x")
        prev = date.strftime("%s")
    time.sleep(1)

#------------------------------------------End-------------------------------------------
