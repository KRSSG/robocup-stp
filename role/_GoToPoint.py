from kubs import kubs, cmd_node
from pid.run import *
from pid.run_w import *
import rospy,sys
from krssg_ssl_msgs.msg import point_2d
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from krssg_ssl_msgs.msg import gr_Robot_Command
from utils.geometry import Vector2D
from utils.config import *
from utils.math_functions import *

kub = None
start_time = None
GOAL_POINT = None
FLAG_move = True
FLAG_turn = True
rotate = 0
init_angle = 0

FIRST_CALL = True


def init(_kub,target,theta):
    global kub,GOAL_POINT,rotate
    kub = _kub
    GOAL_POINT = point_2d()
    rotate = theta
    GOAL_POINT.x = target.x
    GOAL_POINT.y = target.y


def reset():
    global start_time
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)
    
def execute(startTime):
    global GOAL_POINT, start_time,FIRST_CALL
    if FIRST_CALL:
        start_time = startTime
        FIRST_CALL = False

    t = rospy.Time.now()
    t = t.secs + 1.0*t.nsecs/pow(10,9)

    [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, kub.kubs_id, GOAL_POINT, kub.state.homePos, kub.state.awayPos)
    vw = Get_Omega(kub.kubs_id,rotate,kub.state.homePos)
    if not vw:
        vw = 0

    if(REPLANNED):
        reset()
    kub.move(vx, vy)
    kub.turn(vw)
    kub.execute()

    if dist(kub.state.homePos[kub.kubs_id], GOAL_POINT) < 210.0 :
        kub.move(0,0)
        kub.turn(0)
        kub.execute()
