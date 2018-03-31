from tactic import Tactic
import time
import sys
from math import *
from utils.geometry import *
import skills.skills_union
from utils.config import *
from skills import sGoToBall
from skills import sGoToPoint
from skills import sFaceToBall
from skills import sKickToPoint
import numpy as np

class TTestIt(Tactic):
    def __init__(self, bot_id, state, param=None):
        super(TTestIt, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()
        self.bot_id=bot_id
        self.UPPER_HALF = Vector2D(-HALF_FIELD_MAXX,OUR_GOAL_MAXY)
        self.LOWER_HALF = Vector2D(-HALF_FIELD_MAXX, OUR_GOAL_MINY)

    def execute(self, state, pub):

        #GO_TO_BALL

        #sGoToBall.execute(self.sParam, state, self.bot_id, pub)

        #FACE_TO_BALL
        #sFaceToBall.execute(self.sParam, state, self.bot_id, pub)


        import sTurnToPoint
        self.sParam.TurnToPointP.x = state.ballPos.x
        self.sParam.TurnToPointP.y = state.ballPos.y
        self.sParam.TurnToPointP.max_omega = MAX_BOT_OMEGA
        sTurnToPoint.execute(self.sParam, state, self.bot_id, pub)
        #Turn_To_Angle
        # import sTurnToAngle
        # self.sParam.TurnToAngleP.finalslope=0
        # print(state.homePos[self.bot_id].theta)
        # sTurnToAngle.execute(self.sParam, state, self.bot_id, pub)

        #GO_TO_POINT
        ballPos=Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        # dest_bot_id=0
        # destination=Vector2D()
        # destination.x=int(state.homePos[dest_bot_id].x)
        # destination.y=int(state.homePos[dest_bot_id].y)
        # self.sParam.GoToPointP.x= 490
        # self.sParam.GoToPointP.y= -1010
        # self.sParam.GoToPointP.finalslope=pi
        # self.sParam.GoToPointP.align = True
        # sGoToPoint.execute(self.sParam, state, self.bot_id, pub)


        #KICK_TO_POINT
        # dest_bot_id=1
        # destination=Vector2D()
        # destination.x=int(state.homePos[dest_bot_id].x)
        # destination.y=int(state.homePos[dest_bot_id].y)
        # self.sParam.KickToPointP.x=destination.x
        # self.sParam.KickToPointP.y=destination.y
        # self.sParam.KickToPointP.power=7
        # sKickToPoint.execute(self.sParam, state, self.bot_id, pub)


        #GO_TO_POINT
        # ballPos=Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        # destination=Vector2D(0,0)
        # self.sParam.GoToPointP.x=destination.x
        # self.sParam.GoToPointP.y=destination.y
        # self.sParam.GoToPointP.finalslope=ballPos.angle(destination)
        # sGoToPoint.execute(self.sParam, state, self.bot_id, pub)

        #GOALIE
        # GOAL_LOWER_X=110
        # GOAL_LOWER_Y=890
        # GOAL_UPPER_X=415
        # GOAL_UPPER_Y=1680
        # origin=Vector2D(int((GOAL_LOWER_X+GOAL_UPPER_X)/2.0), int((GOAL_LOWER_Y+GOAL_UPPER_Y)/2.0))

        # ballVel=Vector2D(int(state.ballVel.x), int(state.ballVel.y))
        # ballPos=Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        # my_pos=Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))

        # print "ball is at "+str(ballPos.x)+","+str(ballPos.y)
        # if (GOAL_LOWER_X<ballPos.x<GOAL_UPPER_X+500 and GOAL_LOWER_Y<ballPos.y<GOAL_UPPER_Y):
        #     print "HEE_1"
        #     self.sParam.KickToPointP.x=600
        #     self.sParam.KickToPointP.y=origin.y
        #     self.sParam.KickToPointP.power=7
        #     sKickToPoint.execute(self.sParam, state, self.bot_id, pub)
        #     return

        # if (fabs(ballVel.y)>0):
        #     destination=Vector2D()
        #     try:
        #         destination.y=ballPos.y+(ballVel.y)*(ballPos.x-origin.x)/ballVel.x
        #     except:
        #         destination.y=ballPos.y

        #     destination.x=GOAL_UPPER_X

        #     if(not (GOAL_LOWER_Y<destination.y<GOAL_UPPER_Y)):
        #         if(destination.y>GOAL_UPPER_Y):
        #             destination.y=GOAL_UPPER_Y
        #         else:
        #             destination.y=GOAL_LOWER_Y

        #     self.sParam.GoToPointP.x=destination.x
        #     self.sParam.GoToPointP.y=destination.y
        #     self.sParam.GoToPointP.finalslope=ballPos.angle(destination)
        #     print "HEE_2"
        #     sGoToPoint.execute(self.sParam, state, self.bot_id, pub)
        #     return

        # destination=Vector2D()
        # destination.x=GOAL_UPPER_X

        # #destination.y=((my_pos.x-origin.x)/(ballPos.x-origin.x)*(ballPos.y-origin.y))
        # if(not GOAL_LOWER_Y<ballPos.y<GOAL_UPPER_Y):
        #     if(ballPos.y>GOAL_UPPER_Y):
        #         destination.y=GOAL_UPPER_Y
        #     elif(ballPos.y<GOAL_LOWER_Y):
        #         destination.y=GOAL_LOWER_Y
        # else:
        #     destination.y=ballPos.y

        # self.sParam.GoToPointP.x=destination.x
        # self.sParam.GoToPointP.y=destination.y
        # self.sParam.GoToPointP.finalslope=ballPos.angle(destination)

        # sGoToPoint.execute(self.sParam, state, self.bot_id, pub)










    def isComplete(self, state):
        # TO DO use threshold distance instead of actual co ordinates
        if self.destination.dist(state.homePos[i]) < self.threshold:
            return True
        elif time.time()-self.begin_time > self.time_out:
            return True
        else:
            return False

    def updateParams(self, state):
        # No parameter to update here
        pass
