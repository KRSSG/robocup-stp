import skill_node
import math
import sys


from navigation_py.wrapperpy import MergeSCurve, Vector_Obstacle
from navigation_py.obstacle import Obstacle
from utils.config import *
from utils.geometry import Vector2D
from math import pi

POINTPREDICTIONFACTOR = 2

vx = 0
vy = 0
vw = 0
bot_id = 0
start_time = None
start_time_w = None
GOAL_POINT = None
FLAG_move = True
FLAG_turn = True
totalAngle = 0
init_angle = 0

FIRST_CALL = True


def reset():
    global start_time
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)

def path_planner(state,bot_id,pub,GOAL_POINT):
	global GOAL_POINT, start_time,FLAG_move,FLAG_turn,totalAngle,init_angle,FIRST_CALL

    if FIRST_CALL:
        init_angle = state.homePos[bot_id].theta
        FIRST_CALL = False

    t = rospy.Time.now()
    t = t.secs + 1.0*t.nsecs/pow(10,9)

    if(FLAG_move is  True and FLAG_turn is  True ):
        [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, bot_id, GOAL_POINT, state.homePos, state.awayPos) 
        vw = Get_Omega(start_time_w, t, bot_id, totalAngle, state.homePos)
    
    elif (FLAG_move is  True and FLAG_turn is  False ):
        [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, bot_id, GOAL_POINT, state.homePos, state.awayPos)
    
    elif (FLAG_move is  False and FLAG_turn is  True ):
        vx = vy = vw = REPLANNED = 0
        vw = Get_Omega(start_time_w, t, bot_id, totalAngle, state.homePos )
    
    else:
        vx = vy = vw = REPLANNED = 0

    if not vw:
        vw = 0
    if(REPLANNED):
        reset()
    # kub.move(vx, vy)
    # kub.turn(vw)
    # kub.execute(state)
    skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, vw, 0,dribller)
    print dist(kub.get_pos(), GOAL_POINT),t
    #if BScall is not None:
    if dist(kub.get_pos(), GOAL_POINT) < 210.0 :
        FLAG_move = False

    print state.homePos[bot_id].theta,totalAngle,init_angle,BOT_ANGLE_THRESH
    print abs(abs(state.homePos[bot_id].theta-init_angle)  - abs(totalAngle))

    if abs(abs(state.homePos[bot_id].theta-init_angle)  - abs(totalAngle)) < BOT_ANGLE_THRESH:
        FLAG_turn = False

    print FLAG_turn,FLAG_move
    if not FLAG_move and not FLAG_turn:
        # kub.move(0,0)
        # kub.turn(0)
        # kub.execute(state)
        skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, 0, 0,dribller)
        print "Final showdown"
        print init_angle,state.homePos[bot_id].theta,state.homePos[bot_id].theta-init_angle

def execute(param,state,bot_id, pub,dribller = False):
	path_planner(state, bot_id, pub,Vector2D(100,100))
