import sys, os
import rospy
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
import threading
import time
from std_msgs.msg import Int8
from utils.geometry import Vector2D
from utils.config import *
from tactics import TGoalie
from tactics import TestTac
from tactics import TPosition
from tactics import TPrimaryDefender
from tactics import TLDefender
from tactics import TRDefender
from tactics import TDTP,TAttacker
from tactics import TTestIt
from skills import sGoToPoint
from skills import sGoToBall
from plays import pStall
from plays import DTP_Play
from plays import pCordinatedPass
from skills import skills_union
import math
ref_play_id = 0
cur_play = None
start_time = 0
goalie_tac = None
LDefender_tac = None
RDefender_tac = None
cur_goalie = 0

def skills_GoToPoint(state,bot_id,point):
    sParams = skills_union.SParam()
    ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
    ballVel = Vector2D(int(state.ballVel.x) , int(state.ballVel.y))
    distance = botPos.dist(ballPos)
    sParams.GoToPointP.x = point.x
    sParams.GoToPointP.y = point.y

    sGoToPoint.execute(sParams, state, bot_id, pub)

def skills_GoToBall(state,bot_id,slope = None):
    sParams = skills_union.SParam()
    ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
    ballVel = Vector2D(int(state.ballVel.x) , int(state.ballVel.y))
    distance = botPos.dist(ballPos)
    sParams.GoToPointP.x = ballPos.x
    sParams.GoToPointP.y = ballPos.y
    if slope:
        sParams.GoToBallP.align = True
        sParams.GoToBallP.finalslope = slope
    else:
        sParams.GoToBallP.align = False

    sGoToBall.execute(sParams, state, bot_id, pub)

def skill_callback(state):
    global pub
    bot_id = 0
    skills_GoToBall(state,bot_id,math.pi)

def main():
    global pub
    print "Initializing the node "
    rospy.init_node('play_py_node',anonymous=False)
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)

    for i in xrange(6):
        os.environ['bot'+str(i)]=str(start_time)
    for i in xrange(6):
        print os.environ.get('bot'+str(i))

    pub = rospy.Publisher('/grsim_data', gr_Commands, queue_size=1000)
    rospy.Subscriber('/belief_state', BeliefState, skill_callback, queue_size=1000)

    rospy.spin()

if __name__=='__main__':
    # rospy.init_node('skill_py_node',anonymous=False)
    main()