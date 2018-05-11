print "In test GOToPoint"
from skills import skill_node
from velocity.run import *
import rospy,sys
from krssg_ssl_msgs.msg import point_2d
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from krssg_ssl_msgs.msg import gr_Robot_Command
from krssg_ssl_msgs.msg import point_SF
from utils.config import *
import sys

bot_id = int(sys.argv[1])
print "bot_id received",bot_id
pub = rospy.Publisher('/grsim_data', gr_Commands, queue_size=1000)

GOAL_POINT = point_2d()
GOAL_POINT.x = 1000
GOAL_POINT.y = 1200
REPLANNED = 0
homePos = None
awayPos = None

def reset():
	global start_time
	start_time = rospy.Time.now()
	start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)

def GUI_Callback(data):
	global bot_id, kub, BState, pub
	bot_id = data.bot_id
	print bot_id, "_____________________________"

def BS_callback(data):
	global homePos, REPLANNED
	global awayPos, start_time, BState, kub
	BState = data
	homePos = data.homePos
	awayPos = data.awayPos
	t = rospy.Time.now()
	t = t.secs + 1.0*t.nsecs/pow(10,9)
	print(" t - start = ",t-start_time)
	[vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, bot_id, data.ballPos, homePos, awayPos)	#vx, vy, vw, replanned
	print("-------------------REPLANNED = ",REPLANNED)
	if(REPLANNED):
		reset()
	print("vx = ",vx)
	print("vy = ",vy)
	# print("kubs_id = ",kub.kubs_id)
	try:	
		skill_node.send_command(pub, False, bot_id, vx, vy, vw, 0,0)
	except Exception as e:
		print("In except",e)
		pass	

if __name__ == "__main__":
	global start_time
	rospy.init_node('node_new',anonymous=False)
	start_time = rospy.Time.now()
	start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)
	pub = rospy.Publisher('/grsim_data', gr_Commands, queue_size=1000)	
	rospy.Subscriber('/belief_state', BeliefState, BS_callback, queue_size=1000)
	rospy.Subscriber('/gui_params', point_SF, GUI_Callback, queue_size = 1000)
	rospy.spin()


