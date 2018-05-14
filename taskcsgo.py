import sys
import PlaySelector
import TestSkills
import rospy
import math
from krssg_ssl_msgs.msg import GUI_call
from krssg_ssl_msgs.msg import BeliefState
statemimic=None
resetValue=0

def gui_callback(msg):
	global statemimic
	TestSkills.main()
	global resetValue
	resetValue=0
	while 1:
		if(resetValue==1):
			TestSkills.skills_Stop(statemimic,bot_id)
			break;
		# print "in cs finally"
		# print(msg.button)
		# print(msg.params)
		if (msg.button  == "skill_test"):
			params = str(msg.params).split(' ')
			skill = params[0]
			params = params[1:]
			if skill in "goToBall":
				bot_id = int(params[0])
				
				TestSkills.skills_GoToBall(statemimic,bot_id,math.pi)
				# print "RETURNED"


def reset_callback(msg):
	global resetValue
	resetValue=1
	print("In reset callback",resetValue)

def skill_callback(state):
	global statemimic 
	statemimic = state

def main():
	rospy.init_node('gui',anonymous=False)
	rospy.Subscriber('/gui_call', GUI_call, gui_callback, queue_size=1000)
	rospy.Subscriber('/belief_state', BeliefState, skill_callback, queue_size=1000)
	rospy.Subscriber('/gui_call_reset', GUI_call, reset_callback, queue_size=1000)
	rospy.spin()

if __name__ == '__main__':
	print "STARTED"
	main()
