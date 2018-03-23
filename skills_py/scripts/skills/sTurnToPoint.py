import skill_node
import math
import sys

sys.path.insert(0, '../../../navigation_py/scripts/navigation')
sys.path.insert(0, '../../../navigation_py/scripts/navigation/src')
sys.path.insert(0, '../../../plays_py/scripts/utils')

from config import *
from wrapperpy import *
from geometry import *

def execute(param, state, bot_id, pub):
    point = Vector2D(int(param.TurnToPointP.x), int(param.TurnToPointP.y))
    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
    ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))

    vec = Vector2D()
    finalslope = point.angle(botPos)
    turnAngleLeft = vec.normalizeAngle(finalslope - state.homePos[bot_id].theta)  #Angle left to turn
    omega = 2.8 * turnAngleLeft * param.TurnToPointP.max_omega / (2 * math.pi)  #Speedup turn

    omega = min(omega,MAX_BOT_OMEGA)


    v_x = omega * BOT_BALL_THRESH * 1.5
    dist = ballPos.dist(botPos)

    if dist < DRIBBLER_BALL_THRESH :
        skill_node.send_command(pub, state.isteamyellow, bot_id, v_x, 0, omega, 0, True)
    else:
        skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0, False)
