import skill_node
import math
import sys

sys.path.insert(0, '../../../navigation_py/scripts/navigation')
sys.path.insert(0, '../../../navigation_py/scripts/navigation/src')
sys.path.insert(0, '/../../../plays_py/scripts/utils')

from config import *
from wrapperpy import *
from geometry import *

FRICTION_COEFF = 0.05
ACCN_GRAVITY = 9.80665
ANGLE_THRES =30.0
TURN_ANGLE_THRESH = 5 * math.pi/180

def execute(param, state, bot_id, pub):
    R = param.DribbleTurnP.turn_radius
    v = param.DribbleTurnP.max_velocity
    K = 1000

    fp = Vector2D(param.DribbleTurnP.x,param.DribbleTurnP.y)
    botpointangle = fp.normalizeAngle(fp.angle(state.homePos[bot_id]))

    print "Bot Pos: {} {}".format(state.homePos[bot_id].x,state.homePos[bot_id].y)
    print "Bot Point angle: {}".format(fp.angle(state.homePos[bot_id])*180/math.pi)
    sign = -1 if fp.normalizeAngle(fp.normalizeAngle(state.homePos[bot_id].theta)-fp.normalizeAngle(fp.angle(state.homePos[bot_id]))) >= 0 else 1
    print "Sign: {}".format(sign)

    ta = (v*v)/(K*R)
    a = sign*abs(math.atan(ta))
    print "tananlpha: {} alpha: {}".format(ta,a*180/math.pi)
    v_y = v*math.cos(a)
    v_x = v*math.sin(a)
    w = sign*v/R
    print "w: {}".format(w)

    skill_node.send_command(pub, state.isteamyellow, bot_id, v_x, v_y, w, 0, 1)