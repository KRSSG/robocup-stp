import skill_node
import math
import sys,os


from navigation_py.wrapperpy import MergeSCurve, Vector_Obstacle
from navigation_py.obstacle import Obstacle
from utils.config import *
from utils.geometry import Vector2D
from math import pi
from velocity.run import *
import rospy,sys
from krssg_ssl_msgs.msg import point_2d
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from krssg_ssl_msgs.msg import gr_Robot_Command
from krssg_ssl_msgs.msg import point_SF
from utils.config import *

POINTPREDICTIONFACTOR = 2

def reset(bot_id):
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)
    os.environ['bot'+str(bot_id)]=str(start_time)



# def debug(param, state, bot_pos, nextWP, nextNWP, speed, theta, omega, obs):
# 	print '#'*50
# 	print 'Current bot pos: {}, {}'.format(bot_pos.x, bot_pos.y)
# 	print 'Target  bot pos: {}, {}'.format(param.GoToPointP.x, param.GoToPointP.y)
# 	print 'NextWP  bot pos: {}, {}'.format(nextWP.x, nextWP.y)
# 	print 'NextNWP bot pos: {}, {}'.format(nextNWP.x, nextNWP.y)
# 	print 'speed: {}\ttheta: {}\tomega: {}'.format(speed, theta, omega)
# 	print 'len(obs): {}'.format(len(obs))
# 	print 'frame : {}'.format(state.frame_number)
# 	print '#'*50


def debug(param, state, bot_id):
	botPos = Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
	destination = Vector2D(param.GoToPointP.x, param.GoToPointP.y)
	align = param.GoToPointP.align
	finalSlope = param.GoToPointP.finalSlope
	dist = botPos.dist(destination)
	print '#'*50
	print 'In sGoToPoint'
	print 'Current bot pos: {}, {}'.format(state.homePos[bot_id].x, state.homePos[bot_id].y)
	print 'Target pos: {}, {}'.format(destination.x, destination.y)
	print 'Align: {}'.format(align)
	if align:
		print 'Finalslope: {}'.format(finalSlope)
		print 'Bot Orientation {}'.format(state.homePos[bot_id].theta)
	print 'Distance: {}'.format(dist)
	print '#'*50


def execute(param, state, bot_id, pub,dribller = False):
    t = rospy.Time.now()
    t = t.secs + 1.0*t.nsecs/pow(10,9)
    start_time = float(os.environ.get('bot'+str(bot_id)))
    print(" t - start = ",t-start_time)
    [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, bot_id, state.ballPos, state.homePos, state.awayPos)    #vx, vy, vw, replanned
    print("-------------------REPLANNED = ",REPLANNED)
    if(REPLANNED):
        reset(bot_id)
    print("vx = ",vx)
    print("vy = ",vy)
    # print("kubs_id = ",kub.kubs_id)
    # try:    
    #     skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, vw, 0,0)
    # except Exception as e:
    #     print("In except",e)
    #     pass

    # obs = Vector_Obstacle()
    # for i in range(0,len(state.homeDetected)):
    #     if state.homeDetected[i] and i != bot_id:
    #         o = Obstacle()     
    #         o.x=state.homePos[i].x
    #         o.y=state.homePos[i].y
    #         o.radius=3.3*BOT_RADIUS
    #         obs.push_back(o)

    # for j in range(0,len(state.awayDetected)):
    #     if state.awayDetected[j]:
    #         o = Obstacle()
    #         o.x=state.awayPos[j].x
    #         o.y=state.awayPos[j].y
    #         o.radius=3.3*BOT_RADIUS
    #         obs.push_back(o)


    pointPos = Vector2D()
    pointPos.x = int(param.GoToPointP.x)
    pointPos.y = int(param.GoToPointP.y)
    # point = Vector2D()
    # nextWP = Vector2D()
    # nextNWP = Vector2D()

    # pathplanner = MergeSCurve()

    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
   
    # pathplanner.plan(botPos,pointPos,nextWP,nextNWP,obs,len(obs),bot_id, True)
    v = Vector2D()
    distan = botPos.dist(pointPos)
    maxDisToTurn = distan 
    angleToTurn = v.normalizeAngle((param.GoToPointP.finalSlope)-(state.homePos[bot_id].theta))

    minReachTime = maxDisToTurn / MAX_BOT_OMEGA
    maxReachTime = maxDisToTurn / MIN_BOT_OMEGA

    minTurnTime = angleToTurn / MAX_BOT_OMEGA
    maxTurnTime = angleToTurn / MIN_BOT_OMEGA

    # speed = 0.0
    omega = 2*angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)                 

    if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
        if omega < 0:
            omega = -MIN_BOT_OMEGA
        else:
            omega = MIN_BOT_OMEGA

    # from math import exp

    # speed= 2*maxDisToTurn*MAX_BOT_SPEED/(HALF_FIELD_MAXX)
    # if (speed)< 2*MIN_BOT_SPEED:
    #     speed=2*MIN_BOT_SPEED
    # if  (speed > MAX_BOT_SPEED):
    #     speed=MAX_BOT_SPEED    
  
    # vec = Vector2D()


    # motionAngle = nextWP.angle(botPos)
    # theta  = motionAngle - state.homePos[bot_id].theta
    if param.GoToPointP.align == False:
        if distan < DRIBBLER_BALL_THRESH:
            if distan < BOT_BALL_THRESH:
                skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,dribller)
              
            else:
                skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
        else:
            skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
    else:
        if distan > BOT_BALL_THRESH:
            skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
        else:
            skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,dribller)

