import skill_node
import math
import sys

from utils.config import *
from utils.geometry import *
from navigation_py.wrapperpy import *
from navigation_py.obstacle import Obstacle

import skills_union
import sGoToBall
import sGoToPoint
import sTurnToPoint

def execute(param, state, bot_id, pub):
    # print "in kicktopoint"
    botPos=Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
    ballPos=Vector2D(int(state.ballPos.x), int(state.ballPos.y))
    destPoint=Vector2D(int(param.KickToPointP.x), int(param.KickToPointP.y))
    ob = Vector2D()

    finalSlope = destPoint.angle(botPos)
    turnAngleLeft = ob.normalizeAngle(finalSlope - state.homePos[bot_id].theta)  #Angle left to turn
    ballBotAngle  = ob.normalizeAngle(ballPos.angle(botPos)-state.homePos[bot_id].theta)
    dist = ballPos.dist(botPos)

    if dist > BOT_BALL_THRESH :
        print("before kick (GoToBall) dist remaining : ",dist-BOT_BALL_THRESH, " : ", BOT_BALL_THRESH)
        param.GoToPointP.x = state.ballPos.x
        param.GoToPointP.y = state.ballPos.y
        param.GoToPointP.finalSlope = ballPos.angle(state.homePos[bot_id])
        sGoToPoint.execute(param, state, bot_id, pub)
        return 
        # print("After gotoball")

    if ballBotAngle > SATISFIABLE_THETA/2 :
        sParam = skills_union.SParam()
        sParam.TurnToPointP.x = ballPos.x
        sParam.TurnToPointP.y = ballPos.y
        sParam.TurnToPointP.max_omega = MAX_BOT_OMEGA
        print("before kick (TurnToBall) angle remaining : ",ballBotAngle)
        sTurnToPoint.execute(sParam, state, bot_id, pub)
        return
    if math.fabs(turnAngleLeft) > SATISFIABLE_THETA/2 : # SATISFIABLE_THETA in config file
        sParam = skills_union.SParam()
        sParam.TurnToPointP.x = destPoint.x
        sParam.TurnToPointP.y = destPoint.y
        sParam.TurnToPointP.max_omega = MAX_BOT_OMEGA
        print("before kick (Turn) angle remaining : ",turnAngleLeft)
        sTurnToPoint.execute(sParam, state, bot_id, pub)
        return
        # print("after turn")
    print ("____KICK____ DIST :",dist," ANGLE : ",turnAngleLeft)
    skill_node.send_command(pub, state.isteamyellow, bot_id ,0, 0, 0, param.KickToPointP.power, False)


    
      
     
    