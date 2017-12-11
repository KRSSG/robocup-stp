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
GOAL_POINT = None
BScall = None

FLAG_run = True
def init(_kub,target):
	global kub,GOAL_POINT
	kub = _kub
	start_time = None
	GOAL_POINT = point_2d()
	print target.x,target.y
	# while(1):
	# 	pass
	GOAL_POINT.x = target.x
	GOAL_POINT.y = target.y


def reset():
	global start_time
	start_time = rospy.Time.now()
	start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)

def BS_callback(state):
	global GOAL_POINT, start_time,FLAG_run
		
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
	print dist(kub.get_pos(), GOAL_POINT),t
	#if BScall is not None:
	if dist(kub.get_pos(), GOAL_POINT) < 210.0:
		FLAG_run = False
 		rospy.signal_shutdown('node_new'+ str(kub.kubs_id))

def run():
	global start_time
	print str(kub.kubs_id) + str('***********')
	rospy.init_node('node_new'+str(kub.kubs_id),anonymous=False)
	start_time = rospy.Time.now()
	start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)	
	rospy.Subscriber('/belief_state', BeliefState, BS_callback, queue_size=1000)
	rospy.spin()
	return FLAG_run