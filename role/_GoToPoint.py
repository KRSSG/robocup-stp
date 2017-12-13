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
start_time_w = None
GOAL_POINT = None
FLAG_move = True
FLAG_turn = True
totalAngle = 0
init_angle = 0

FIRST_CALL = True


def init(_kub,target,theta):
    global kub,GOAL_POINT,totalAngle
    kub = _kub
    start_time = None
    GOAL_POINT = point_2d()
    totalAngle = theta*1.1
    # while True:
    #     print kub.state.homePos
    #     pass
    # init_angle = kub.state.homePos[kub.kubs_id].theta
    # print theta,totalAngle
    #print target.x,target.y
    # while(1):
    #   pass
    GOAL_POINT.x = target.x
    GOAL_POINT.y = target.y


def reset():
    global start_time
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)
    
def BS_callback(state):
    global GOAL_POINT, start_time,FLAG_move,FLAG_turn,totalAngle,init_angle,FIRST_CALL

    if FIRST_CALL:
        init_angle = state.homePos[kub.kubs_id].theta
        FIRST_CALL = False
    # while True:
    #     print "bs ",totalAngle
    #     pass
        
    t = rospy.Time.now()
    t = t.secs + 1.0*t.nsecs/pow(10,9)

    # print(" t - start = ",t-start_time,GOAL_POINT.x,GOAL_POINT.y)

    if(FLAG_move is  True and FLAG_turn is  True ):
        [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, kub.kubs_id, GOAL_POINT, state.homePos, state.awayPos) 
        vw = Get_Omega(start_time_w, t, kub.kubs_id, totalAngle, state.homePos)
    
    elif (FLAG_move is  True and FLAG_turn is  False ):
        [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, kub.kubs_id, GOAL_POINT, state.homePos, state.awayPos)
    
    elif (FLAG_move is  False and FLAG_turn is  True ):
        vx = vy = vw = REPLANNED = 0
        vw = Get_Omega(start_time_w, t, kub.kubs_id, totalAngle, state.homePos )
    
    else:
        vx = vy = vw = REPLANNED = 0

    # [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, kub.kubs_id, GOAL_POINT, state.homePos, state.awayPos)   #vx, vy, vw, replanned
    # omega = Get_Omega(start_time, t, kub.kubs_id, totalAngle, state.homePos)
    if not vw:
        vw = 0
    # print("omega  "+str(vw)+"   omega")
    #print("-------------------REPLANNED = ",REPLANNED)
    if(REPLANNED):
        reset()
    kub.move(vx, vy)
    kub.turn(vw)
    kub.execute(state)
    print dist(kub.get_pos(), GOAL_POINT),t
    #if BScall is not None:
    if dist(kub.get_pos(), GOAL_POINT) < 210.0 :
        FLAG_move = False

    print state.homePos[kub.kubs_id].theta,totalAngle,init_angle,BOT_ANGLE_THRESH
    print abs(abs(state.homePos[kub.kubs_id].theta-init_angle)  - abs(totalAngle))

    if abs(abs(state.homePos[kub.kubs_id].theta-init_angle)  - abs(totalAngle)) < BOT_ANGLE_THRESH:
        FLAG_turn = False

    print FLAG_turn,FLAG_move
    if not FLAG_move and not FLAG_turn:
        kub.move(0,0)
        kub.turn(0)
        kub.execute(state)
        print "Final showdown"
        print init_angle,state.homePos[kub.kubs_id].theta,state.homePos[kub.kubs_id].theta-init_angle
        rospy.signal_shutdown('node_new'+ str(kub.kubs_id))


def run():
    global start_time,start_time_w, FLAG_move,FLAG_turn
    #print str(kub.kubs_id) + str('***********')
    rospy.init_node('node_new'+str(kub.kubs_id),anonymous=False)
    start_time = rospy.Time.now()
    start_time_w = start_time


    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)   
    start_time_w = 1.0*start_time_w.secs + 1.0*start_time_w.nsecs/pow(10,9)

    rospy.Subscriber('/belief_state', BeliefState, BS_callback, queue_size=1000)
    rospy.spin()
    return FLAG_move and FLAG_turn