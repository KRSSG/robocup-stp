import socket
import rospy 
from krssg_ssl_msgs.msg import gr_Commands
import sys 
import thread          
sys.path.append('/opt/ros/jade/lib/python2.7/dist-packages/')

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
v_4_wheel = [0, 0, 0, 0]

UDP_PORT = 5005
UDP_IP = ['127.0.0.1']*6 #bot_ip

print("UDP target port:", UDP_PORT)

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

def send(bot_index,buf):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
	sock.sendto(buf, (UDP_IP[bot_index], UDP_PORT))

def gr_Commands_CB(msg):
    global buf
    vel_xyw = [0]*3
    vel_xyw[0] = int(msg.robot_commands.velnormal * FACTOR_T)
    vel_xyw[1] = -1*int(msg.robot_commands.veltangent * FACTOR_N)
    vel_xyw[2] =int(msg.robot_commands.velangular * FACTOR_W)
    v_4_wheel = vel_convert(vel_xyw)
    start = 1 + msg.robot_commands.id*5
    for i in range(4):
        buf[i+start] = int(v_4_wheel[i])

    if msg.robot_commands.spinner and msg.robot_commands.kickspeedx :
        buf[start+4] = 3
    elif msg.robot_commands.spinner :
        buf[start+4] = 2
    elif msg.robot_commands.kickspeedx :
        buf[start+4] = 1
    else:
        buf[start+4] = 0
    buff = ''   
    for i in xrange(len(buf)):
        if buf[i] > 255:
            buf[i] = 0
        buff += chr(int(buf[i])%256)

    try:
    	for i in xrange(6):
    		thread.start_new_thread(send,(i,buff,))
    except:
       print ("Error: unable to start thread")


rospy.init_node('bot_comm_wifi',anonymous=False)
rospy.Subscriber('/grsim_data',gr_Commands,gr_Commands_CB)
rospy.spin()
