import skill_node
import math
from utils.config import *
from utils.geometry import *
from navigation_py.wrapperpy import *
from navigation_py.obstacle import Obstacle

def debug(param, state, bot_id):
		botPos = Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
		ballPos = Vector2D(state.ballPos.x, state.ballPos.y)
		print '#'*50
		print 'In sTurnToAngle'
		print 'Current bot pos: {}, {}'.format(state.homePos[bot_id].x, state.homePos[bot_id].y)
		print 'Target alignment: {}'.format(param.TurnToAngleP.finalSlope)
		print 'Bot Orientation: {}'.format(state.homePos[bot_id].theta)
		print '#'*50

def execute(param, state, bot_id,pub, dribbler=False):
		debug(param,state,bot_id)
		finalSlope = param.TurnToAngleP.finalSlope # Yet to be defined
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
