from kubs import kubs, cmd_node
from pid.run import *
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
GOAL_POINT = Vector2D(-3000,-2000)
BScall = None
theta = None
FLAG_run = True

def init(_kub,_theta):
	global kub,theta
	kub = _kub
	start_time = None
	theta = _theta



def reset():
	global start_time
	start_time = rospy.Time.now()
	start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)

def BS_callback(state):
	global GOAL_POINT, start_time,FLAG_run,theta
	BSstate = state
	GOAL_POINT = state.ballPos
	kub.state.ballPos = GOAL_POINT

	theta = atan2(state.ballPos.y,state.ballPos.x-3000)
	GOAL_POINT = getPointBehindTheBall(GOAL_POINT,theta)

		
	t = rospy.Time.now()
	t = t.secs + 1.0*t.nsecs/pow(10,9)
	# print(" t - start = ",t-start_time,GOAL_POINT.x,GOAL_POINT.y)
	[vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, kub.kubs_id, GOAL_POINT, state.homePos, state.awayPos)	#vx, vy, vw, replanned
	#print("-------------------REPLANNED = ",REPLANNED)
	if(REPLANNED):
		reset()
	kub.move(vx, vy)
	kub.turn(vw)
	kub.execute(state)
	#print "kub-goal",dist(kub.get_pos(), GOAL_POINT)
	#print dist(kub.state.ballPos,GOAL_POINT)
	# print ((state.ballPos.x,state.ballPos.y),(kub.state.ballPos.x,kub.state.ballPos.y),(GOAL_POINT.x,GOAL_POINT.y))
	#if BScall is not None:
	if dist(kub.get_pos(), GOAL_POINT) < 210.0:
		FLAG_run = False
 		rospy.signal_shutdown('node_new'+ str(kub.kubs_id))

def run():
	global start_time
	#print str(kub.kubs_id) + str('***********')
	rospy.init_node('node_new'+str(kub.kubs_id),anonymous=False)
	start_time = rospy.Time.now()
	start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)	
	rospy.Subscriber('/belief_state', BeliefState, BS_callback, queue_size=1000)
	rospy.spin()
	return FLAG_run

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
# 	global kub,theta
# 	kub = _kub
# 	theta = _theta


# def reset():
# 	global start_time
# 	start_time = rospy.Time.now()
# 	start_time = 1.0 * start_time.secs + 1.0 * start_time.nsecs / pow(10,9)

# def BS_callback(state):
# 	BSstate = state
# 	global  start_time,GOAL_POINT
# 	GOAL_POINT = state.ballPos
# 	theta = atan2(state.ballPos.y,state.ballPos.x-3000)
# 	GOAL_POINT = getPointBehindTheBall(GOAL_POINT,theta)

# 	kub.state.ballPos = GOAL_POINT
		
# 	t = rospy.Time.now()
# 	t = t.secs + 1.0 * t.nsecs / pow(10,9)
# 	#print(" t - start = ",t-start_time,GOAL_POINT.x,GOAL_POINT.y)
# 	[vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, kub.kubs_id, GOAL_POINT, state.homePos, state.awayPos)	#vx, vy, vw, replanned
# 	if(REPLANNED):
# 		reset()	
# 	kub.move(vx, vy)
# 	kub.turn(vw)
# 	kub.execute(state)

# def run():
# 	global start_time
# 	print kub.kubs_id + str('***********')
# 	rospy.init_node('node_new'+ str(kub.kubs_id),anonymous=False)
# 	rospy.Rate(1)
# 	start_time = rospy.Time.now()
# 	start_time = 1.0 * start_time.secs + 1.0 * start_time.nsecs / pow(10,9)	
# 	rospy.Subscriber('/belief_state', BeliefState, BS_callback, queue_size=1000)
# 	rospy.spin()