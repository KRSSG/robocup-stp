
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

from skills import skills_union
from skills import sStop
from skills import sGoToPoint
from utils.role_selector import *

from plays import pStall
from plays import DTP_Play
from plays import pCordinatedPass
from skills import skills_union
from utils import tactics_union
from velocity.getVel import GetVelocity

ref_play_id = 0
cur_play = None
start_time = 0
goalie_tac = None
LDefender_tac = None
RDefender_tac = None
cur_goalie = 0

prev_attacker = 3



isteamyellow = False
ref_command = False

gv = None 

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


def attacker_callback(state):
    global pub,prev_attacker
    # print "bef as"
    attacker_id = attacker_selector(state)
    param = skills_union.SParam()
    if prev_attacker != attacker_id :
        sStop.execute(param, state, prev_attacker, pub)
    else:
        cur_tactic = TAttacker.TAttacker(attacker_id,state,param)
        cur_tactic.execute(state,pub)
    prev_attacker = attacker_id
    print ("attacker : ",attacker_id)

def LDefender_callback(state):
    global pub,LDefender_tac
    # LDefender_id = 0
    LDefender_id = 1
    ballPos = Vector2D(state.ballPos.x,state.ballPos.y)
    botpos = Vector2D(state.homePos[0].x,state.homePos[0].y)
    print("dist ",ballPos.dist(botpos))
    # return
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

def planner_callback(state):
    print("incoming planner_callback")
    global pub
    bot_id = 0
    ballPos = Vector2D(state.ballPos.x, state.ballPos.y)
    botpos = Vector2D(state.homePos[bot_id].x,state.homePos[bot_id].y)
    print("dist is ",ballPos.dist(botpos))
    new = TestTac.TestTac(bot_id,state)
    new.execute(state,pub)
    print(" outgoing planner_callback")

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
    # print("New Call Back")
    global pub
    attacker_id = 0
    params = tactics_union.Param()
    params.PositionP.x = state.ballPos.x
    params.PositionP.y = state.ballPos.y
    cur_tactic = TPosition.TPosition(attacker_id+1,state,params)
    cur_tactic.execute(state,gv,pub)

def debug_subscriber2(state):
    # print("New Call Back")
    global pub
    attacker_id = 0
    params = tactics_union.Param()
    params.PositionP.x = state.homePos[1].x -200
    params.PositionP.y = state.homePos[1].y + 200
    cur_tactic = TPosition.TPosition(attacker_id,state,params)
    cur_tactic.execute(state,gv,pub)


    # cur_tactic = TTestIt.TTestIt(attacker_id,state)
    # cur_tactic.execute(state,pub)
def main():
    global pub, gv
    print "Initializing the node "
    # rospy.init_node('play_py_node',anonymous=False)
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)

    gv = []
    for i in xrange(6):
        os.environ['bot'+str(i)]=str(start_time)
        gv.append(GetVelocity(start_time = start_time,kubs_id = i))
        #os.environ['fc'+str(i)]='1'
    for i in xrange(6):
        print os.environ.get('bot'+str(i))

    #for i in xrange(6):
    #    start_time = float(os.environ.get('bot'+str(i)))
     #   gv.append(GetVelocity(start_time = start_time,kubs_id = i))

    pub = rospy.Publisher('/grsim_data', gr_Commands, queue_size=1000)

    # rospy.Subscriber("/ref_data", Referee, referee_callback, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, bs_callback, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, goalKeeper_callback, queue_size=1000)
    rospy.Subscriber('/belief_state', BeliefState, debug_subscriber2, queue_size=1000)
    rospy.Subscriber('/belief_state', BeliefState, debug_subscriber, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, LDefender_callback, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, planner_callback, queue_size=1000)
    # rospy.Subscriber('/belief_state', BeliefState, RDefender_callback, queue_size=1000)
    rospy.Subscriber('/belief_state', BeliefState, attacker_callback, queue_size=1000)
    #rospy.Subscriber('/ref_play', Int8, ref_callback, queue_size=1000)
    rospy.spin()

if __name__=='__main__':
    rospy.init_node('play_py_node',anonymous=False)
    main()
