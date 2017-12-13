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
GOAL_POINT = Vector2D(-3000,-2000)
point_to = Vector2D(0,0)
BScall = None
theta = None
FLAG_move = True
FLAG_turn = True
totalAngle = 0
init_angle = 0

FIRST_CALL = True

def init(_kub,_point_to):
    global kub,point_to
    kub = _kub
    start_time = None
    point_to = _point_to
    # while True:
    #     print totalAngle
    #     pass



def reset():
    global start_time
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)

def BS_callback(state):
    global GOAL_POINT, start_time,FLAG_move,FLAG_turn,totalAngle,init_angle,FIRST_CALL,start_time_w

    if FIRST_CALL:
        init_angle = state.homePos[kub.kubs_id].theta*0
        FIRST_CALL = False

    totalAngle = angle_diff(state.ballPos,point_to)

    # print totalAngle,angle_diff(state.ballPos,point_to)
    # return

    BSstate = state
    GOAL_POINT = state.ballPos
    kub.state.ballPos = GOAL_POINT
    # GOAL_POINT = getPointBehindTheBall(GOAL_POINT,totalAngle)

        
    t = rospy.Time.now()
    t = t.secs + 1.0*t.nsecs/pow(10,9)
    # if(move_flag =1  and )
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
    ##print dist(kub.get_pos(), GOAL_POINT),t
    #if BScall is not None:
    if dist(kub.get_pos(), GOAL_POINT) < 210.0 :
        FLAG_move = False

    # print
    # print "curr: ",state.homePos[kub.kubs_id].theta,",tot : ",totalAngle,\
    # ",init : ",init_angle,",thresh : ",BOT_ANGLE_THRESH
    # print "diff ",abs((state.homePos[kub.kubs_id].theta-init_angle)  - (totalAngle)),vw
    # print


    if abs((state.homePos[kub.kubs_id].theta-init_angle)  - (totalAngle)) < BOT_ANGLE_THRESH:
        FLAG_turn = False

   # print "Turn : ",FLAG_turn,", Move : ",FLAG_move
    if not FLAG_move and not FLAG_turn:
        kub.move(0,0)
        kub.turn(0)
        kub.kick(7)
        kub.execute(state)
       # print "Final showdown in Move"
       # print init_angle,state.homePos[kub.kubs_id].theta,state.homePos[kub.kubs_id].theta-init_angle
        rospy.signal_shutdown('node_new'+ str(kub.kubs_id))
    # # print(" t - start = ",t-start_time,GOAL_POINT.x,GOAL_POINT.y)
    # [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, kub.kubs_id, GOAL_POINT, state.homePos, state.awayPos)   #vx, vy, vw, replanned
    # #print("-------------------REPLANNED = ",REPLANNED)
    # if(REPLANNED):
    #   reset()
    # kub.move(vx, vy)
    # kub.turn(vw)
    # kub.execute(state)
    # #print "kub-goal",dist(kub.get_pos(), GOAL_POINT)
    # #print dist(kub.state.ballPos,GOAL_POINT)
    # # print ((state.ballPos.x,state.ballPos.y),(kub.state.ballPos.x,kub.state.ballPos.y),(GOAL_POINT.x,GOAL_POINT.y))
    # #if BScall is not None:
    # if dist(kub.get_pos(), GOAL_POINT) < 210.0:
    #   FLAG_run = False
    #   kub.move(0,0)
    #   kub.turn(0)
    #   kub.execute(state)
 #      rospy.signal_shutdown('node_new'+ str(kub.kubs_id))

def run():
    global start_time,start_time_w
    #print str(kub.kubs_id) + str('***********')
    rospy.init_node('node_new'+str(kub.kubs_id),anonymous=False)
    start_time = rospy.Time.now()
    start_time_w = start_time

    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)   
    start_time_w = 1.0*start_time_w.secs + 1.0*start_time_w.nsecs/pow(10,9)

    rospy.Subscriber('/belief_state', BeliefState, BS_callback, queue_size=1000)
    rospy.spin()
    return FLAG_move

# from kubs import kubs, cmd_node
# from pid.run import *
# import rospy,sys
# from krssg_ssl_msgs.msg import point_2d
# from krssg_ssl_msgs.msg import BeliefState
# from krssg_ssl_msgs.msg import gr_Commands
# from krssg_ssl_msgs.msg import gr_Robot_Command
# from utils.geometry import Vector2D
# from utils.config import *
# from utils.math_functions import *
# from math import atan2

# kub = None
# GOAL_POINT = None
# start_time = None
# theta = None

# BSstate = None
# def init(_kub,_theta):
#   global kub,theta
#   kub = _kub
#   theta = _theta


# def reset():
#   global start_time
#   start_time = rospy.Time.now()
#   start_time = 1.0 * start_time.secs + 1.0 * start_time.nsecs / pow(10,9)

# def BS_callback(state):
#   BSstate = state
#   global  start_time,GOAL_POINT
#   GOAL_POINT = state.ballPos
#   theta = atan2(state.ballPos.y,state.ballPos.x-3000)
#   GOAL_POINT = getPointBehindTheBall(GOAL_POINT,theta)

#   kub.state.ballPos = GOAL_POINT
        
#   t = rospy.Time.now()
#   t = t.secs + 1.0 * t.nsecs / pow(10,9)
#   #print(" t - start = ",t-start_time,GOAL_POINT.x,GOAL_POINT.y)
#   [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, kub.kubs_id, GOAL_POINT, state.homePos, state.awayPos) #vx, vy, vw, replanned
#   if(REPLANNED):
#       reset() 
#   kub.move(vx, vy)
#   kub.turn(vw)
#   kub.execute(state)

# def run():
#   global start_time
#   print kub.kubs_id + str('***********')
#   rospy.init_node('node_new'+ str(kub.kubs_id),anonymous=False)
#   rospy.Rate(1)
#   start_time = rospy.Time.now()
#   start_time = 1.0 * start_time.secs + 1.0 * start_time.nsecs / pow(10,9) 
#   rospy.Subscriber('/belief_state', BeliefState, BS_callback, queue_size=1000)
#   rospy.spin()