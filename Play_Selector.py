import sys
import rospy
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
import threading
import time
from std_msgs.msg import Int8
from utils.geometry import Vector2D
from utils.config import *
from tactics import TGoalie
from tactics import TPosition
from tactics import TPrimaryDefender
from tactics import TLDefender
from tactics import TRDefender
from tactics import TDTP,TAttacker
from tactics import TTestIt

from plays import pStall
from plays import DTP_Play
from plays import pCordinatedPass
from skills import skills_union
ref_play_id = 0
cur_play = None
start_time = 0
goalie_tac = None
LDefender_tac = None
RDefender_tac = None
cur_goalie = 0

def select_play(state):
	global start_time,pub
	# TO DO Proper play selection
	# play_testplay=pTestPlay.pTestPlay()
	# play_cordinatedpass=pCordinatedPass.pCordinatedPass()
	play=DTP_Play.DTP_Play(pub)
	# start_time = time.clock()
	# play_testplay.execute()
	play.execute(state)
	return play
	# play_Defence = pDefence.pDefence()
	# play_Defence.execute()

def ref_callback(play_id):
	global ref_play_id
	ref_play_id = play_id

def goalKeeper_callback(state):
	global pub,goalie_tac,cur_goalie
	state.our_goalie = 0
	cur_goalie = state.our_goalie
	if goalie_tac == None :
		cur_goalie = state.our_goalie
		goalie_tac = TGoalie.TGoalie(cur_goalie,state)
	goalie_tac.execute(state,pub)
	print ("goalie : ",cur_goalie)

# def attacker_callback(state):
# 	global pub
# 	attacker_id = 5
# 	param = skills_union.SParam()
# 	param.DribbleTurnP.x = 0
# 	param.DribbleTurnP.y = 0
# 	param.DribbleTurnP.max_velocity = 500
# 	param.DribbleTurnP.turn_radius = 300
# 	cur_tactic = TDTP.TDTP(attacker_id,state,param)
# 	cur_tactic.execute(state,pub)
# 	print ("attacker : ",attacker_id)

def attacker_callback(state):
	global pub
	attacker_id = 5
	param = skills_union.SParam()
	cur_tactic = TAttacker.TAttacker(attacker_id,state,param)
	cur_tactic.execute(state,pub)
	print ("attacker : ",attacker_id)

def LDefender_callback(state):
	global pub,LDefender_tac
	# LDefender_id = 0
	LDefender_id = 1
	ballPos = Vector2D(state.ballPos.x,state.ballPos.y)
	botpos = Vector2D(state.homePos[0].x,state.homePos[0].y)
	print("dist ",ballPos.dist(botpos))
	return
	if LDefender_tac == None :
		LDefender_tac = TLDefender.TLDefender(LDefender_id,state)
	LDefender_tac.execute(state,pub)

def RDefender_callback(state):
	global pub,RDefender_tac
	# RDefender_id = 1
	RDefender_id = 2
	ballPos = Vector2D(state.ballPos.x,state.ballPos.y)
	if RDefender_tac == None :
		RDefender_tac = TRDefender.TRDefender(RDefender_id,state)
	RDefender_tac.execute(state,pub)

def bs_callback(state):
	global cur_play,start_time
	state.our_goalie = 0
	if ref_play_id == 0 :  # 0 signifies normal game play
		if(cur_play == None):
			cur_play = select_play(state)
		cur_time = time.clock()
		if(cur_time - start_time >=60): # TIME OUT IS 60 seconds for now
			cur_play = select_play(state)
		cur_play.execute(state)
	else :
		cur_play = None
		start_time = 0
		# TO DO call corresponding refree plays here
		# Basically corresponding TPosition except goalie

def debug_subscriber(state):
	global pub
	attacker_id = 0
	cur_tactic = TTestIt.TTestIt(attacker_id,state)
	cur_tactic.execute(state,pub)

if __name__=='__main__':
    global pub
    print "Initializing the node "
    rospy.init_node('play_py_node',anonymous=False)
    pub = rospy.Publisher('/grsim_data', gr_Commands, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, bs_callback, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, goalKeeper_callback, queue_size=1000)
    rospy.Subscriber('/belief_state', BeliefState, debug_subscriber, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, LDefender_callback, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, RDefender_callback, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, attacker_callback, queue_size=1000)
    #rospy.Subscriber('/ref_play', Int8, ref_callback, queue_size=1000)
    rospy.spin()
