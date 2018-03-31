import skill_node
import math
import sys


from navigation_py.wrapperpy import MergeSCurve, Vector_Obstacle
from navigation_py.obstacle import Obstacle
from utils.config import *
from utils.geometry import Vector2D
from math import pi

POINTPREDICTIONFACTOR = 2


def debug(param, state, bot_pos, nextWP, nextNWP, speed, theta, omega, obs):
    print '#'*50
    print 'Current bot pos: {}, {}'.format(bot_pos.x, bot_pos.y)
    print 'Target  bot pos: {}, {}'.format(param.GoToPointP.x, param.GoToPointP.y)
    print 'NextWP  bot pos: {}, {}'.format(nextWP.x, nextWP.y)
    print 'NextNWP bot pos: {}, {}'.format(nextNWP.x, nextNWP.y)
    print 'speed: {}\ttheta: {}\tomega: {}'.format(speed, theta, omega)
    print 'len(obs): {}'.format(len(obs))
    print 'frame : {}'.format(state.frame_number)
    print '#'*50


def execute(param,state,bot_id, pub,dribbler = False):
    obs = Vector_Obstacle()
    for i in range(0,len(state.homeDetected)):
        if state.homeDetected[i] and i != bot_id:
            o = Obstacle()
            o.x=state.homePos[i].x
            o.y=state.homePos[i].y
            o.radius=2.5*BOT_RADIUS
            obs.push_back(o)

    for j in range(0,len(state.awayDetected)):
        if state.awayDetected[j]:
            o = Obstacle()
            o.x=state.awayPos[j].x
            o.y=state.awayPos[j].y
            o.radius=2.5*BOT_RADIUS
            obs.push_back(o)


    pointPos = Vector2D()
    pointPos.x = int(param.GoToPointP.x)
    pointPos.y = int(param.GoToPointP.y)
    point = Vector2D()
    nextWP = Vector2D()
    nextNWP = Vector2D()

    pathplanner = MergeSCurve()

    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))

    pathplanner.plan(botPos,pointPos,nextWP,nextNWP,obs,len(obs),bot_id,not state.isteamyellow)

    # Komega = 1.5
    # Kvel = 1.7

    # netDist = pointPos.dist(state.homePos[bot_id])
    # curDist = nextWP.dist(state.homePos[bot_id])
    # theta_cov = nextWP.normalizeAngle(nextWP.normalizeAngle(param.GoToPointP.finalSlope) - nextWP.normalizeAngle(state.homePos[bot_id].theta))
    # theta_cur = theta_cov * curDist/netDist

    # v_x = -25*Kvel*curDist*math.sin(theta_cur)/HALF_FIELD_MAXX
    # v_y = 25*Kvel*curDist*math.cos(theta_cur)/HALF_FIELD_MAXX
    # omega = Komega*theta_cur
    # print v_x,",",v_y
    # skill_node.send_command(pub, state.isteamyellow, bot_id, v_x, v_y, omega, 0, dribbler)


   
    dist = pointPos.dist(botPos)
    maxDisToTurn = dist -  DRIBBLER_BALL_THRESH
    angleToTurn = pointPos.normalizeAngle((pointPos.angle(botPos))-(state.homePos[bot_id].theta))

    minReachTime = maxDisToTurn / MAX_BOT_SPEED
    maxReachTime = maxDisToTurn / MIN_BOT_SPEED

    minTurnTime = angleToTurn / MAX_BOT_OMEGA
    maxTurnTime = angleToTurn / MIN_BOT_OMEGA

    speed = 0.0
    omega = angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)

    if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
        if omega < 0:
            omega = -MIN_BOT_OMEGA
        else:
            omega = MIN_BOT_OMEGA

   
    speed= 2*maxDisToTurn*MAX_BOT_SPEED/(HALF_FIELD_MAXX)
    if (speed)< 2*MIN_BOT_SPEED:
        speed=2*MIN_BOT_SPEED
    if  (speed > MAX_BOT_SPEED):
        speed=MAX_BOT_SPEED    

    vec = Vector2D()
    motionAngle = nextWP.angle(botPos)
    theta  = motionAngle - state.homePos[bot_id].theta
    theta  = vec.normalizeAngle(theta)
    if dist < DRIBBLER_BALL_THRESH:
        if dist < 1*BOT_BALL_THRESH:
            skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0, True)
        else:
            skill_node.send_command(pub, state.isteamyellow, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, 0, True)

    else:
        skill_node.send_command(pub, state.isteamyellow, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, 0, False)
