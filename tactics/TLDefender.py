from tactic import Tactic
import time
import sys


from utils.geometry import * 
from utils.config import *
from skills import skills_union
from skills import sGoToPoint
from skills import sStop
from skills import sKick
from skills import sKickToPoint
from skills import sGoToPoint
from tactic import Tactic
from skills import sTurnToPoint
from skills import sGoalie


import enum
from tactic import Tactic
from math import *
from numpy import inf,array,linalg
from utils.config import *

class TLDefender(Tactic):
    def __init__(self,bot_id,state,params=None):
        super(TLDefender, self).__init__(bot_id, state, params)
        self.sParams = skills_union.SParam()
        self.ballPrevX_Velocity = 0

    class State(enum.Enum):
        # Opponent has the ball and we need to block his angle
        block = 1
        # The ball is moving towards our goal and we should catch it.
        intercept = 2
        # Goal Keeper has to clear the ball, so block the nearest opponent
        clear_block = 3
        # Ball in our possession
        chill = 4

        # TO DO Add more states for refree plays

    def ball_in_our_dBox(self,state):
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        if ballPos.x > -HALF_FIELD_MAXX+DBOX_WIDTH :
            return False
        dbox_point1 = Vector2D(-HALF_FIELD_MAXX,DBOX_SMALLER_LENGTH/2)
        dbox_point2 = Vector2D(-HALF_FIELD_MAXX,-DBOX_SMALLER_LENGTH/2)
        if ballPos.dist(dbox_point1) < DBOX_RADIUS or ballPos.dist(dbox_point2) < DBOX_RADIUS :
            return True
        elif -DBOX_SMALLER_LENGTH/2 <= ballPos.y and ballPos.y <= DBOX_SMALLER_LENGTH/2 :
            return True
        else :
            return False


    def getState(self,state):
        attacker_id = state.opp_bot_closest_to_ball
        attacker_pos = Vector2D (int(state.awayPos[attacker_id].x),int(state.awayPos[attacker_id].y))
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        attacker_dist = ballPos.dist(attacker_pos)
        self.ballPrevX_Velocity = (self.ballPrevX_Velocity + state.ballVel.x)/2
        if False :  # check for ref_play
            pass
        elif self.ball_in_our_dBox(state) :
            return TLDefender.State.clear_block
        elif state.ball_in_our_possession :
            return TLDefender.State.chill
        elif int(state.ballVel.x) < -1 and int(self.ballPrevX_Velocity) < -7:  # TO DO SIGNS ACCORDING TO FIELD POSITION
            return TLDefender.State.intercept
        elif attacker_dist < DRIBBLER_BALL_THRESH and (state.homePos[self.bot_id].x-state.ballPos.x)*(state.ballPos.x-state.awayPos[state.opp_bot_closest_to_ball].x) > 0 :
            return TLDefender.State.block
        else :
            return TLDefender.State.chill

    def getPoints(self,state):
        ballPos = Vector2D(state.ballPos.x,state.ballPos.y)
        goal_max = Vector2D(-HALF_FIELD_MAXX,OUR_GOAL_MAXY)
        goal_min = Vector2D(-HALF_FIELD_MAXX,OUR_GOAL_MINY)
        xmin = xmax = -HALF_FIELD_MAXX+DBOX_WIDTH
        if abs(state.ballPos.y) <= 2.2*OUR_GOAL_MAXY :
            return Vector2D(-HALF_FIELD_MAXX+DBOX_WIDTH,DBOX_SMALLER_LENGTH/2),Vector2D(-HALF_FIELD_MAXX+DBOX_WIDTH,-DBOX_SMALLER_LENGTH/2)
        if ballPos.x != goal_max.x :
            ymax = ballPos.y + (ballPos.y-goal_max.y)*abs((xmax-ballPos.x)/(ballPos.x-goal_max.x))
            ymin = ballPos.y + (ballPos.y-goal_min.y)*abs((xmin-ballPos.x)/(ballPos.x-goal_min.x))
            if ymin > OUR_GOAL_MAXY :
                ymin = DBOX_SMALLER_LENGTH/2
                angle = atan2(ballPos.y-DBOX_WIDTH/2,ballPos.x-goal_max.x)
                xmax = goal_max.x + abs(1.4*sin(angle)*(DBOX_RADIUS+2*BOT_RADIUS))
                print ("xmax : ",xmax)
                ymax = DBOX_SMALLER_LENGTH/2 + abs(cos(angle)*(DBOX_RADIUS+2*BOT_RADIUS))
            elif ymax < OUR_GOAL_MINY :
                ymax = -DBOX_SMALLER_LENGTH/2
                angle = atan2(ballPos.y+DBOX_WIDTH/2,ballPos.x-goal_min.x)
                xmin = goal_max.x + abs(1.4*sin(angle)*(DBOX_RADIUS+2*BOT_RADIUS))
                print ("xmin : ",xmin)
                ymin = -DBOX_SMALLER_LENGTH/2 - abs(cos(angle)*(DBOX_RADIUS+2*BOT_RADIUS))
        else :
            ymin = -DBOX_SMALLER_LENGTH/2
            ymax = DBOX_SMALLER_LENGTH/2
        if ymax-ymin < 2.5*BOT_RADIUS :
            diff = 2.5*BOT_RADIUS - ymax + ymin
            ymax = ymax + diff/2
            ymin = ymin -diff/2
        pointL = Vector2D(xmax,ymax)
        pointR = Vector2D(xmin,ymin)
        print (" L : ",pointL.x,",",pointL.y)
        print (" R : ",pointR.x,",",pointR.y)
        return pointL,pointR

    def execute(self, state , pub):
        #bot_list = [self.bot_id, self.bot_id]
        print "BALL_POS : ",state.ballPos.x,",",state.ballPos.y
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
        ballVel = Vector2D(int(state.ballVel.x) , int(state.ballVel.y))
        distance = botPos.dist(ballPos)
        attacker_id = state.opp_bot_closest_to_ball
        attacker_pos = Vector2D (int(state.awayPos[attacker_id].x),int(state.awayPos[attacker_id].y))
        gameState = self.getState(state)

        # self.sParams.GoToPointP.x = ballPos.x
        # self.sParams.GoToPointP.y = ballPos.y
        # sGoToPoint.execute(self.sParams, state, self.bot_id, pub)
        # return

        if gameState == TLDefender.State.block:
            print ("ATTACKER_HAS_THE_BALL")
            self.sParams.GoToPointP.x = -HALF_FIELD_MAXX+DBOX_WIDTH+BOT_RADIUS
            if (ballPos.x-attacker_pos.x) != 0 :
                y = ballPos.y + (ballPos.y-attacker_pos.y)*abs((-HALF_FIELD_MAXX+2*BOT_RADIUS-ballPos.x)/(ballPos.x-attacker_pos.x))
            else :
                y = ballPos.y
            y = min(y,OUR_GOAL_MAXY - BOT_RADIUS)
            y = max(y,OUR_GOAL_MINY + BOT_RADIUS)
            if y - OUR_GOAL_MINY <= 2*BOT_RADIUS :
                y = y + 4.4*BOT_RADIUS
            elif OUR_GOAL_MAXY - y <= 2*BOT_RADIUS :
                y = y - 1.7*BOT_RADIUS
            else :
                y = y + 2.4*BOT_RADIUS
            self.sParams.GoToPointP.y = y
            finalPos = Vector2D(self.sParams.GoToPointP.x,self.sParams.GoToPointP.y)
            self.sParams.GoToPointP.finalSlope = ballPos.angle(finalPos)
            if finalPos.dist(state.homePos[self.bot_id]) <= BOT_BALL_THRESH :
                print (" TURN TOWARDS BALL")
                self.sParams.TurnToPointP.x = ballPos.x
                self.sParams.TurnToPointP.y = ballPos.y
                self.sParams.TurnToPointP.max_omega = MAX_BOT_OMEGA
                sTurnToPoint.execute(self.sParams,state,self.bot_id,pub)
            else :
                print (" GET POSITIONED ")
                sGoToPoint.execute(self.sParams, state, self.bot_id, pub)
        elif gameState == TLDefender.State.intercept:
            print ("___BALL_APPROACHING______")
            self.sParams.GoToPointP.x = -HALF_FIELD_MAXX+DBOX_WIDTH+BOT_RADIUS
            y = ballPos.y + ballVel.y*abs((-HALF_FIELD_MAXX+2*BOT_RADIUS-ballPos.x)/ballVel.x)
            y = min(y,OUR_GOAL_MAXY - BOT_RADIUS)
            y = max(y,OUR_GOAL_MINY + BOT_RADIUS)
            if y - OUR_GOAL_MINY <= 2*BOT_RADIUS :
                y = y + 4.4*BOT_RADIUS
            elif OUR_GOAL_MAXY - y <= 2*BOT_RADIUS :
                y = y - 1.7*BOT_RADIUS
            else :
                y = y + 2.4*BOT_RADIUS
            self.sParams.GoToPointP.y = y
            finalPos = Vector2D(self.sParams.GoToPointP.x,self.sParams.GoToPointP.y)
            self.sParams.GoToPointP.finalSlope = ballPos.angle(finalPos)
            if distance <= DRIBBLER_BALL_THRESH and ballPos.y < 0:
                self.sParams.KickToPointP.x = 0  # TO DO decide the point to clear the ball
                self.sParams.KickToPointP.y = 0
                self.sParams.KickToPointP.power = 7
                sKickToPoint.execute(self.sParams,state,self.bot_id,pub, True)
            else :
                sGoToPoint.execute(self.sParams, state, self.bot_id, pub)
        elif gameState == TLDefender.State.chill :
            print ("___BALL_NOT_APPROACHING______")
            pointL,pointR = self.getPoints(state)
            self.sParams.GoToPointP.x = pointL.x
            self.sParams.GoToPointP.y = pointL.y
            finalPos = pointL
            self.sParams.GoToPointP.finalSlope = ballPos.angle(finalPos)
            print(finalPos.x,finalPos.y)
            if distance <= DRIBBLER_BALL_THRESH and ballPos.y > 0:
                print ("KICK TO POINT")
                self.sParams.KickToPointP.x = 0  # TO DO decide the point to clear the ball
                self.sParams.KickToPointP.y = 0
                self.sParams.KickToPointP.power = 7
                sKickToPoint.execute(self.sParams,state,self.bot_id,pub)
            else :
                if finalPos.dist(state.homePos[self.bot_id]) <= BOT_BALL_THRESH :
                    print (" TURN TOWARDS BALL")
                    self.sParams.TurnToPointP.x = ballPos.x
                    self.sParams.TurnToPointP.y = ballPos.y
                    self.sParams.TurnToPointP.max_omega = MAX_BOT_OMEGA
                    sTurnToPoint.execute(self.sParams,state,self.bot_id,pub)
                else :
                    print (" GET POSITIONED ")
                    sGoToPoint.execute(self.sParams, state, self.bot_id, pub)
        elif gameState == TLDefender.State.clear_block:
            print (" ___CLEAR_THE_BALL________")
            sStop.execute(self.sParams,state,self.bot_id,pub)
            # TO DO decide the opponent to block
        else :
            print ("___REFREE_PLAY__________")
            # TO DO add refree conditions here


    def isComplete(self, state):
        return False

    def updateParams(self, state):
        pass
