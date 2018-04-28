import sys
sys.path.append('/opt/ros/jade/lib/python2.7/dist-packages/')
import rospy
import serial, os
from pylab import *
import math
import time 
sys.path.append('../../')
frame = 1
ti = time.time()            
# # sys.path.append('/home/aif/ROBOCUP_SSL_WS/devel/lib/python2.7/dist-packages/krssg_ssl_msgs/msg/')
# from krssg_ssl_msgs.msg import gr_Commands
ser = None

# # ser = serial.Serial('/dev/ttyUSB1',bytesize=32)
# ser = serial.Serial('/dev/ttyUSB1')
file = ''
try :
    try:
        # global ser, file
        ser = serial.Serial('/dev/ttyUSB0',115200)
        file = '/dev/ttyUSB0'
    except:
        # global ser
        ser = serial.Serial('/dev/ttyUSB1',115200)
        file = '/dev/ttyUSB1'
    # ser = serial.Serial('/dev/ttyUSB1',bytesize=32)
    print(ser)

except :
    print("Couldn't open the port\n")


Team_ID = 127  # Team Blue
theta = [30.0,150.0,225.0,315.0] # Bot angles
bot_radius = 0.087
bot_wheel_radius = 0.025
max_vel_wheel = 5000.0 # in rpm
# global buf
buf = [None]*32
for i in range(32):
    buf[i] = 0
buf[0] = Team_ID
FACTOR_T = 40
FACTOR_N = 40
FACTOR_W = 90
v_4_wheel = [None, None, None, None]
ch_buff = ''
from os import stat


def vel_convert(vel_3_wheel):
    vx = vel_3_wheel[0]
    vy = vel_3_wheel[1]
    vw = -vel_3_wheel[2]

    print("vx",vx,"vy",vy,"vw",vw)
    for i in range(4):
        v_4_wheel[i] = ((bot_radius*vw) - (vx*math.sin(theta[i]*math.pi/180.0)) + (vy*math.cos(theta[i]*math.pi/180.0)))/(bot_wheel_radius * math.pi)
    for i in range(4):
        if v_4_wheel[i] > 0 :
            v_4_wheel[i] = 126 + ((v_4_wheel[i]-max_vel_wheel)*126) / max_vel_wheel
        else :
            v_4_wheel[i] = 255 + (v_4_wheel[i]*129) / max_vel_wheel
    return v_4_wheel

def gr_Commands_CB(bot_id, velnormal, veltangent, velangular, spinner=False,kickspeedx=0):
    global buf,ser
    buff = ''
    # for i in xrange(1,32):
    #     buf[i] = 20
    # for i in xrange(4):
    #     buf[i+start] = vel_convert([veltangent,velnormal,velangular])
    # buf[11],   buf[12],  buf[13],  buf[14] = vel_convert([veltangent,velnormal,velangular])

    v_4_wheel = vel_convert([veltangent,velnormal,velangular])
    start = 1 + bot_id*5
    for i in xrange(4):
        buf[i+start] = int(v_4_wheel[i])
    # buf[1],   buf[2],  buf[3],  buf[4] = vel_convert([0,-50,0])
    for i in xrange(11,15):
        buf[i] = int(buf[i])

    for i in xrange(1,5):
        buf[i] = int(buf[i])
    for i in xrange(32):
        buff += chr(int(buf[i])%256)

    print(buf)
    ser.write(buff)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument('--id','-i', default=0)
    parser.add_argument('--vx','-x', default=0)
    parser.add_argument('--vy','-y', default=-40)
    parser.add_argument('--vw','-w', default=0)
    parser.add_argument('--range','-r',type=str,default = "none")
    
    args = parser.parse_args()

    while True:
        if "none" in args.range:
            gr_Commands_CB(bot_id=args.id, velnormal=args.vy, veltangent=args.vx, velangular=args.vw)
        else:
            bots = map(int,args.range.split('-'))
            for i in range(bots[0],bots[1]):
                gr_Commands_CB(bot_id=i, velnormal=args.vy, veltangent=args.vx, velangular=args.vw)
