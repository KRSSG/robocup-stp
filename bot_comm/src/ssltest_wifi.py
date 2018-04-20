import socket
import sys 
import thread          

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
UDP_IP = ['127.0.0.1']*6 # bot_ip

print("UDP target port:", UDP_PORT)

def vel_convert(vel_3_wheel):
    global max_vel_wheel
    vx = vel_3_wheel[0]
    vy = vel_3_wheel[1]
    vw = -vel_3_wheel[2]
    for i in range(4):
        if v_4_wheel[i] > 0 :
            v_4_wheel[i] = 126 + ((v_4_wheel[i]-max_vel_wheel)*126) / max_vel_wheel
        else :
            v_4_wheel[i] = 255 + (v_4_wheel[i]*129) / max_vel_wheel
    return v_4_wheel

def send(bot_index,buf):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(buf, (UDP_IP[bot_index], UDP_PORT))

def gr_Commands_CB(bot_id, velnormal, veltangent, velangular, spinner=False,kickspeedx=0):
    global buf
    print(bot_id,velnormal, veltangent, velangular)
    vel_xyw = [0]*3
    vel_xyw[0] = int(velnormal * FACTOR_T)
    vel_xyw[1] = -1*int(veltangent * FACTOR_N)
    vel_xyw[2] = int(velangular * FACTOR_W)
    v_4_wheel = vel_convert(vel_xyw)
    start = 1 + bot_id*5
    for i in xrange(4):
        buf[i+start] = int(v_4_wheel[i])

    if spinner and kickspeedx :
        buf[start+4] = 3
    elif spinner :
        buf[start+4] = 2
    elif kickspeedx :
        buf[start+4] = 1
    else:
        buf[start+4] = 0
    buff = ''   
    for i in xrange(len(buf)):
        if buf[i] > 255:
            buf[i] = 0
        buff += chr(int(buf[i])%256)
    # buff = ' '.join(map(str,buf))

    # send(0,buff)
    try:
        for i in xrange(1):
            thread.start_new_thread(send,(i,buff,))
    except:
       print ("Error: unable to start thread")



    
if __name__ == '__main__':
    while True:
        gr_Commands_CB(bot_id=0, velnormal=0, veltangent=-40, velangular=0)
