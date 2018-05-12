import skill_node
import math
import sys,os

from utils.config import *
from utils.geometry import *
from navigation_py.wrapperpy import *
from navigation_py.obstacle import Obstacle
from math import pi
from velocity.run import *
import rospy,sys
from krssg_ssl_msgs.msg import point_2d
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from krssg_ssl_msgs.msg import gr_Robot_Command
from krssg_ssl_msgs.msg import point_SF
from utils.config import *
from math import pi

POINTPREDICTIONFACTOR = 2

def reset(bot_id):
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)
    os.environ['bot'+str(bot_id)]=str(start_time)


def debug(param, state, bot_pos, target_pos, nextWP, nextNWP, speed, theta, omega, obs):
    print '#'*50
    print 'Current bot pos: {}, {}'.format(bot_pos.x, bot_pos.y)
    print 'Target  bot pos: {}, {}'.format(param.GoToPointP.x, param.GoToPointP.y)
    print 'NextWP  bot pos: {}, {}'.format(nextWP.x, nextWP.y)
    print 'NextNWP bot pos: {}, {}'.format(nextNWP.x, nextNWP.y)
    print 'speed: {}\ttheta: {}\tomega: {}'.format(speed, theta, omega)
    print 'len(obs): {}'.format(len(obs))
    print 'frame : {}'.format(state.frame_number)
    print '#'*50


def execute(param, state, bot_id, pub,dribbler = False):
    t = rospy.Time.now()
    t = t.secs + 1.0*t.nsecs/pow(10,9)
    start_time = float(os.environ.get('bot'+str(bot_id)))

    [vx, vy, vw, REPLANNED, remainingPath] = Get_Vel(start_time, t, bot_id, state.ballPos, state.homePos, state.awayPos)    #vx, vy, vw, replanned, remainingPath
    if(REPLANNED):
        reset(bot_id)
    print("vx = ",vx)
    print("vy = ",vy)
    # print("kubs_id = ",kub.kubs_id)

    try:    
        skill_node.send_command(pub, False, bot_id, vx, vy, vw, 0,0)
    except Exception as e:
        print("In except",e)
        pass
