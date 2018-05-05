import skill_node
import math
import sys

from utils.config import *
from utils.geometry import *
from navigation_py.wrapperpy import *
from navigation_py.obstacle import Obstacle
from math import pi, fabs

def debug(param, state, bot_id):
    botPos = Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
    ballPos = Vector2D(state.ballPos.x, state.ballPos.y)
    print '#'*50
    print 'In sFaceToBall'
    print 'Current bot pos: {}, {}'.format(state.homePos[bot_id].x, state.homePos[bot_id].y)
    print 'Current ball pos: {}, {}'.format(state.ballPos.x, state.ballPos.y)
    print 'Target alignment: {}'.format(botPos.angle(ballPos))
    print '#'*50

def execute(param, state, bot_id, pub):
    
    debug(param,state,bot_id)

    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
    ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
    vec = Vector2D()
    finalslope = botPos.angle(ballPos)
    turnAngleLeft = vec.normalizeAngle(finalslope - state.homePos[bot_id].theta)  #Angle left to turn
    omega =  1*(math.pi)*turnAngleLeft *MAX_BOT_OMEGA / (2 * math.pi)  #Speedup turn
    if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
        if omega < 0:
            omega = -MIN_BOT_OMEGA
        else:
            omega = MIN_BOT_OMEGA


    v_x = omega * BOT_BALL_THRESH * 1.5
    dist = ballPos.dist(botPos)

    if(fabs(turnAngleLeft)<SATISFIABLE_THETA/2.0):
        omega=0
    
    if dist < DRIBBLER_BALL_THRESH * 2:
        skill_node.send_command(pub, state.isteamyellow, bot_id, v_x, 0, omega, 0, True)
    else:
        skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0, False)
