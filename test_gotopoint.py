import rospy,sys
from utils.geometry import Vector2D
from utils.math_functions import *
from krssg_ssl_msgs.msg import point_2d
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from krssg_ssl_msgs.msg import gr_Robot_Command
from krssg_ssl_msgs.msg import BeliefState
from role import  GoToBall, GoToPoint
from multiprocessing import Process
from kubs import kubs
pub = rospy.Publisher('/grsim_data',gr_Commands,queue_size=1000)

def g(id_):
	kub = kubs.kubs(id_,pub)
	print(kub.kubs_id)
	m = -1 if id_%2 == 0 else 1
	g_fsm = GoToPoint.GoToPoint(kub,Vector2D(400*m*id_*0,800*id_*m),1.57)
	# g_fsm.as_graphviz()
	# g_fsm.write_diagram_png()
	g_fsm.spin()
	# print
	# print kub.state.homePos[kub.kubs_id].theta,t

g(0)

for i in xrange(0):
	p = Process(target=g,args=(i,))
	p.start()

#g_fsm1 = GoToBall.GoToBall(kub,deg_2_radian(45))


#kub1 = kubs.kubs(0,pub)
# g1_fsm = GoToPoint.GoToPoint(kub1,Vector2D(100,263))
# g1_fsm.as_graphviz()
# g1_fsm.write_diagram_png()

#g_fsm1.spin()
# g1_fsm.spin()
#t = threading.Thread(target=g_fsm.spin())
#t1 = threading.Thread(target=g1_fsm.spin())


#t.start()
#t1.start()*
