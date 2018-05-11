import rospy
from krssg_ssl_msgs.msg import BeliefState
import memcache
shared = memcache.Client(['127.0.0.1:11211'],debug=False)


def BS_callback(state):
	shared.set('state',state)
	print state

rospy.init_node('BSnode',anonymous=False)
rospy.Subscriber('/belief_state', BeliefState, BS_callback, queue_size=1000)
rospy.spin()