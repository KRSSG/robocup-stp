import skill_node
import math
import sys


from utils.config import *
from utils.geometry import *
from navigation_py.wrapperpy import *
from navigation_py.obstacle import Obstacle

def debug(param, state, bot_id):
    botPos = Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
    destination = Vector2D(param.TurnToPointP.x, param.TurnToPointP.y)
    print '#'*50
    print 'In sTurnToPoint'
    print 'Current bot pos: {}, {}'.format(state.homePos[bot_id].x, state.homePos[bot_id].y)
    print 'Target alignment: {}'.format(botPos.angle(destination))
    print 'Bot Orientation: {}'.format(state.homePos[bot_id].theta)
    print '#'*50

def execute(param, state, bot_id, pub):
    debug(param, state, bot_id)

    point = Vector2D(int(param.TurnToPointP.x), int(param.TurnToPointP.y))
    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
    ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))

    vec = Vector2D()
    finalslope = botPos.angle(point)
    turnAngleLeft = vec.normalizeAngle(finalslope - state.homePos[bot_id].theta)  #Angle left to turn
    omega = 2.8 * turnAngleLeft * param.TurnToPointP.max_omega / (2 * math.pi)  #Speedup turn

    omega = min(omega,MAX_BOT_OMEGA)


    v_x = omega * BOT_BALL_THRESH * 1.5
    dist = ballPos.dist(botPos)

    if dist < DRIBBLER_BALL_THRESH :
        skill_node.send_command(pub, state.isteamyellow, bot_id, v_x, 0, omega, 0, True)
    else:
        skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0, False)
