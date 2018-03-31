import skill_node
import math
import sys

sys.path.append('../../../plays_py/scripts/utils/')
sys.path.insert(0, '../../../navigation_py/scripts/navigation/src')
sys.path.insert(0, '../../../navigation_py/scripts/navigation')

from utils.geometry import *
from utils.config import *
def execute(param, state, bot_id,pub, dribbler=False):
    finalSlope = param.TurnToAngleP.finalslope # Yet to be defined
    ballPos = Vector2D(int(state.ballPos.x),int(state.ballPos.y))
    botPos = Vector2D(int(state.homePos[bot_id].x),int(state.homePos[bot_id].y))
    obj=Vector2D()
    
    turnAngleLeft = obj.normalizeAngle(finalSlope - state.homePos[bot_id].theta); # Angle left to turn
    
    omega = 3*turnAngleLeft * MAX_BOT_OMEGA/(2*math.pi); # Speedup turn 
    if(omega < 1.43*MIN_BOT_OMEGA and omega > -1.43*MIN_BOT_OMEGA): # This is a rare used skill so believe in Accuracy more than speed. Hence reducing minimum Omega
      if(omega < 0): omega = -1.43*MIN_BOT_OMEGA
      else: omega = 1.43*MIN_BOT_OMEGA
 
    dist = ballPos.dist(botPos)
    if(dist < DRIBBLER_BALL_THRESH):
		  skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,True)
    else:
      skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,False)
