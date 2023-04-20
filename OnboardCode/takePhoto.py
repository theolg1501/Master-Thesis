import os
import datetime
import time


dir_img = '/home/ubuntu/theo/images/'
#   definition of parameters, more at https://www.raspberrypi.org/app/uploads/2013/07/RaspiCam-Documentation.pdf
# rotation
rot = '180'
# saturation，-100 - 100
sa = '30'
# width
width = '1920'
# height
height = '1080'
# timeout
timeout = '1'
# ISO
iso = '1600'
# shutter speed in microseconds
ss = str(10000000 / int(iso))
# set exposure mode
mode = 'sports'

save_str = datetime.datetime.strftime(datetime.datetime.now(),
                                      '%Y-%m-%d-%H-%M-%S')
print('shot time:', save_str)
os.system('raspistill -o ' + dir_img + save_str + '.jpg ' +
          ' -rot ' + rot +
          ' -sa ' + sa +
          ' -w ' + width +
          ' -h ' + height +
          ' -t ' + timeout +
          ' -ex ' + mode)