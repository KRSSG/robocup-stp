import rospy,sys
from utils.geometry import Vector2D
from utils.math_functions import *
from krssg_ssl_msgs.msg import point_2d
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from krssg_ssl_msgs.msg import gr_Robot_Command
from krssg_ssl_msgs.msg import BeliefState
from role import  GoToBall, GoToPoint
import threading
from kubs import kubs
pub = rospy.Publisher('/grsim_data',gr_Commands,queue_size=1000)

#kub = kubs.kubs(0,pub)
kub = kubs.kubs(int(sys.argv[1]),pub)
print(kub.kubs_id)

g_fsm = GoToBall.GoToBall(kub,deg_2_radian(45))
g_fsm.as_graphviz()
g_fsm.write_diagram_png()


# g1_fsm = GoToPoint.GoToPoint(kub1,Vector2D(100,263))
# g1_fsm.as_graphviz()
# g1_fsm.write_diagram_png()

g_fsm.spin()
# g1_fsm.spin()

# t = threading.Thread(target=g_fsm.spin())
# t1 = threading.Thread(target=g1_fsm.spin())


# t.start()
# t1.start()
