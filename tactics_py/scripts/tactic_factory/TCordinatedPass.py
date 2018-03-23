from tactic import Tactic
import time
import sys
from math import *

sys.path.append('../../../skills_py/scripts/skills')
sys.path.append('../../../plays_py/scripts/utils/')
sys.path.insert(0, '../../../navigation_py/scripts/navigation/src')
sys.path.insert(0, '../../../navigation_py/scripts/navigation')

from geometry import * 
import skills_union
from config import *
import obstacle


import sGoToBall
import sGoToPointGoalie
import sFaceToBall
import sKickToPoint
import sGoToPoint
import numpy as np


class TCordinatedPass(Tactic):
    def __init__(self, bot_id, state, param=None):
        super(TCordinatedPass, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()
        self.bot_id=bot_id
        self.UPPER_HALF = Vector2D(-HALF_FIELD_MAXX,OUR_GOAL_MAXY)
        self.LOWER_HALF = Vector2D(-HALF_FIELD_MAXX, OUR_GOAL_MINY)

    def execute(self, state, pub):


        GOAL_LOWER_HALF_Y = 1000
        GOAL_UPPER_HALF_Y = 1420
        GOAL_LOWER_X=110
        GOAL_UPPER_X=530

        LOWER_HALF_Y = 336
        UPPER_HALF_Y = 2580

        ORIGIN_Y = (GOAL_LOWER_HALF_Y+GOAL_UPPER_HALF_Y)*0.5
        ORIGIN_X = (GOAL_LOWER_X+GOAL_UPPER_X)/2.0

        att_id = 0
        rec_id = 1
        pos = {}
        for i in xrange(6):
            pos[i]=Vector2D(int(state.homePos[i].x), int(state.homePos[i].y))
        
        ballPos=Vector2D(int(state.ballPos.x), int(state.ballPos.y))


        # Attacker
        import sKickToPoint
        import sKick
        self.sParam.KickToPointP.x = pos[rec_id].x
        self.sParam.KickToPointP.y = pos[rec_id].y
        self.sParam.KickToPointP.power = 7
        self.sParam.KickP.power=7
        sKickToPoint.execute(self.sParam, state, att_id, pub)
   
        #Receiver
        sFaceToBall.execute(self.sParam, state, rec_id, pub)
        return 
  

        for i in range(10):
            print("dist", pos[att_id].dist(ballPos))



        GOALIE_THRESH = 350
        print("\n\n\n\n\n\ndistance b/w bot and ball",fabs(Vector2D(int(state.homePos[att_id].x),int(state.homePos[att_id].y)).dist(ballPos)))
        print "ball x="+str(ballPos.x)+" ball y="+str(ballPos.y)
        if ballPos.dist(pos[goalie_id])<BOT_BALL_THRESH:
            kicking=True
        else: kicking=False
        if(GOAL_LOWER_X-200<ballPos.x<GOAL_UPPER_X+200 and GOAL_LOWER_HALF_Y-200<ballPos.y<GOAL_UPPER_HALF_Y+200 and state.ballVel.x==0):
            print "kick to point"
            import sKickToPoint
            self.sParam.KickToPointP.x=GOAL_UPPER_X+800
            self.sParam.KickToPointP.y=ORIGIN_Y
            self.sParam.KickToPointP.power=7
            sKickToPoint.execute(self.sParam, state, goalie_id, pub)    
        elif 30+BOT_BALL_THRESH <pos[goalie_id].dist(ballPos) < GOALIE_THRESH or state.ballVel.x<0:
            self.sParam.GoToPointP.x = ORIGIN_X
            self.sParam.GoToPointP.y = ballPos.y + state.ballVel.y*(state.ballPos.x- ORIGIN_X)/fabs(state.ballVel.x)
            if(not GOAL_LOWER_HALF_Y<pos[goalie_id].y<GOAL_UPPER_HALF_Y):
                self.sParam.GoToPointP.y=ORIGIN_Y
            self.sParam.GoToPointP.finalslope=ballPos.angle(Vector2D(int(self.sParam.GoToPointP.x), int(self.sParam.GoToPointP.y)))
            print "gotopoint goalie"
            sGoToPointGoalie.execute(self.sParam, state, goalie_id, pub,kicking)
            print("GAL GTP")
            "I am just aligning"
        else:   
            print "_____in else_____"
            if GOAL_LOWER_HALF_Y<=ballPos.y<=GOAL_UPPER_HALF_Y:
                self.sParam.GoToPointP.y = ballPos.y 
            elif ballPos.y>GOAL_UPPER_HALF_Y:
                self.sParam.GoToPointP.y = GOAL_UPPER_HALF_Y
            elif GOAL_LOWER_HALF_Y>ballPos.y:
                self.sParam.GoToPointP.y = GOAL_LOWER_HALF_Y

            self.sParam.GoToPointP.x = ORIGIN_X
            # ballPos.angle(pos[goalie_id])
            self.sParam.GoToPointP.finalslope =  ballPos.angle(pos[goalie_id])
            sGoToPoint.execute(self.sParam, state, goalie_id, pub)



        # Defender

        if GOAL_LOWER_HALF_Y<=ballPos.y<=GOAL_UPPER_HALF_Y:
            self.sParam.GoToPointP.y = -1*(ballPos.y - ORIGIN_Y) + ORIGIN_Y
        elif ballPos.y>GOAL_UPPER_HALF_Y:
            self.sParam.GoToPointP.y = GOAL_LOWER_HALF_Y
        elif GOAL_LOWER_HALF_Y>ballPos.y:
            self.sParam.GoToPointP.y = GOAL_UPPER_HALF_Y

        self.sParam.GoToPointP.x = 500 + ORIGIN_X
        self.sParam.GoToPointP.finalslope =  ballPos.angle(pos[def_id])
        sGoToPoint.execute(self.sParam, state, def_id, pub)
        print("DEF GTP")

        import sKick

        if pos[def_id].dist(ballPos) < BOT_BALL_THRESH+30:
            print("DEF K")
            sKick.execute(self.sParam, state, def_id, pub)








       

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
