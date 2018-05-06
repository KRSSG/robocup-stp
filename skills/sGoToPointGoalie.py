import skill_node
import math
import sys


from utils.config import *
from utils.geometry import *
from navigation_py.wrapperpy import *
from navigation_py.obstacle import Obstacle

POINTPREDICTIONFACTOR = 2


def debug(param, state, bot_pos, target_pos, nextWP, nextNWP, speed, theta, omega, obs):
    print '#'*50
    print 'Current bot pos: {}, {}'.format(bot_pos.x, bot_pos.y)
    print 'Target  bot pos: {}, {}'.format(param.GoToPointP.x, param.GoToPointP.y)
    print 'NextWP  bot pos: {}, {}'.format(nextWP.x, nextWP.y)
    print 'NextNWP bot pos: {}, {}'.format(nextNWP.x, nextNWP.y)
    print 'speed: {}\ttheta: {}\tomega: {}'.format(speed, theta, omega)
    print 'len(obs): {}'.format(len(obs))
    print 'frame : {}'.format(state.frame_number)
    print '#'*50


def execute(param,state,bot_id, pub, kicking=False):
    obs = Vector_Obstacle()
    for i in range(0,len(state.homeDetected)):
        if state.homeDetected[i] and i != bot_id:
            o = Obstacle()     
            o.x=state.homePos[i].x
            o.y=state.homePos[i].y
            o.radius=3.3*BOT_RADIUS
            obs.push_back(o)

    for j in range(0,len(state.awayDetected)):
        if state.awayDetected[j]:
            o = Obstacle()
            o.x=state.awayPos[j].x
            o.y=state.awayPos[j].y
            o.radius=3.3*BOT_RADIUS
            obs.push_back(o)


    pointPos = Vector2D()
    pointPos.x = int(param.GoToPointP.x)
    pointPos.y = int(param.GoToPointP.y)
    point = Vector2D()
    nextWP = Vector2D()
    nextNWP = Vector2D()

    pathplanner = MergeSCurve()

    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))

    pathplanner.plan(botPos,pointPos,nextWP,nextNWP,obs,len(obs),bot_id, True)
    v = Vector2D()
    distan = botPos.dist(pointPos)
    maxDisToTurn = distan - 5.0 * BOT_BALL_THRESH /4
    angleToTurn = v.normalizeAngle((param.GoToPointP.finalslope)-(state.homePos[bot_id].theta))

    minReachTime = maxDisToTurn / MAX_BOT_OMEGA
    maxReachTime = maxDisToTurn / MIN_BOT_OMEGA

    minTurnTime = angleToTurn / MAX_BOT_OMEGA
    maxTurnTime = angleToTurn / MIN_BOT_OMEGA

    speed = 0.0
    omega = angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)

    if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
        if omega < 0:
            omega = -MIN_BOT_OMEGA
        else:
            omega = MIN_BOT_OMEGA

    if maxDisToTurn > 0:
        if minTurnTime > maxReachTime:
            speed = MIN_BOT_SPEED
        elif minReachTime > maxTurnTime:
            speed = MAX_BOT_SPEED
        elif minReachTime < minTurnTime:
            speed =  maxDisToTurn / minTurnTime
        elif minTurnTime < minReachTime:
            speed = MAX_BOT_SPEED
    else:
        speed = distan / MAX_FIELD_DIST * MAX_BOT_SPEED


    vec = Vector2D()
    motionAngle = nextWP.angle(botPos)
    theta  = motionAngle - state.homePos[bot_id].theta

    if math.fabs(speed) < 64*MIN_BOT_SPEED:
        speed = 64*MIN_BOT_SPEED
    if kicking==True:
        force=7
    else: force=0
    # debug(param, state, botPos, pointPos, nextWP, nextNWP, speed, theta, omega, obs)
    # print "Motion angle : {}".format(motionAngle)
    speed = MAX_BOT_SPEED/1.2
    # omega = 0
    if param.GoToPointP.align == False:
        if distan < DRIBBLER_BALL_THRESH:
            print "here"
            if distan < 0.9*BOT_BALL_THRESH:
                
                skill_node.send_command(pub, state, bot_id, 0, 0, 0, 0, False)
            else:
                skill_node.send_command(pub, state, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, force, False)
        else:
            skill_node.send_command(pub, state, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, force, False)
    else:
        if distan > BOT_BALL_THRESH/4:
            skill_node.send_command(pub, state, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), 0, force, False)
        else:
            skill_node.send_command(pub, state, bot_id, 0, 0, 0, force,False)

