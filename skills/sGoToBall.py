import skill_node
import math
import sys,os


from navigation_py.wrapperpy import MergeSCurve, Vector_Obstacle
from navigation_py.obstacle import Obstacle
from utils.config import *
from utils.geometry import Vector2D
from math import pi,sin,cos
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

    pointPos = Vector2D()
    pointPos.x = int(state.ballPos.x)
    pointPos.y = int(state.ballPos.y)
 

    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
    ballPos = Vector2D(state.ballPos)
    oppGoal = Vector2D(HALF_FIELD_MAXX, 0)
    v = Vector2D()
    targetPoint = Vector2D()
    # maxDisToTurn = distan
    if param.GoToBallP.align:
        angle = param.GoToBallP.finalslope
        angleToTurn = v.normalizeAngle(param.GoToBallP.finalslope - state.homePos[bot_id].theta)
    else:
        angle = ballPos.angle(oppGoal)
        angleToTurn = v.normalizeAngle(ballPos.angle(oppGoal) - state.homePos[bot_id].theta)
    # angleToTurn = v.normalizeAngle((param.GoToPointP.finalSlope)-(state.homePos[bot_id].theta))

    targetPoint.x = ballPos.x - 2*DRIBBLER_BALL_THRESH*cos(angle)
    targetPoint.y = ballPos.y - 2*DRIBBLER_BALL_THRESH*sin(angle)
    distan = botPos.dist(targetPoint)

    t = rospy.Time.now()
    t = t.secs + 1.0*t.nsecs/pow(10,9)
    start_time = float(os.environ.get('bot'+str(bot_id)))

    if distan <= DRIBBLER_BALL_THRESH :
        print("in DRIBBLER_BALL_THRESH")
        [vx, vy, vw, REPLANNED,maxDisToTurn] = Get_Vel(start_time, t, bot_id, state.ballPos, state.homePos, state.awayPos,avoid_ball=False)    #vx, vy, vw, replanned
        omega = 2*angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)                 
        if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
            if omega < 0:
                omega = -MIN_BOT_OMEGA
            else:
                omega = MIN_BOT_OMEGA
        if fabs(angleToTurn) < SATISFIABLE_THETA_SHARP:
            omega = 0
        if distan < BOT_BALL_THRESH:
            skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,dribller)
        else:
            skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
    else:
        [vx, vy, vw, REPLANNED,maxDisToTurn] = Get_Vel(start_time, t, bot_id, targetPoint, state.homePos, state.awayPos,avoid_ball=True)    #vx, vy, vw, replanned
        omega = 2*angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)                 
        if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
            if omega < 0:
                omega = -MIN_BOT_OMEGA
            else:
                omega = MIN_BOT_OMEGA
        if fabs(angleToTurn) < SATISFIABLE_THETA_SHARP:
            omega = 0
        skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)

    if(REPLANNED):
        reset(bot_id)

