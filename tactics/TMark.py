from tactic import Tactic
import time
import sys
from math import *

from utils.config import *

from utils.geometry import * 
from math import *
from skills import *

ANGLE_FACTOR=0.8   #close to the bot to mark orientation
DISTANCE_FACTOR=0.1


class TMark(Tactic):
    def __init__(self, bot_id, state,  param=None):
        super(TMark, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()


    def execute(self, state, pub, bot_to_mark = -1):
        self.bot_to_mark = bot_to_mark
        ballPos=Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        mark_bot_pos=Vector2D(int(state.awayPos[self.bot_to_mark].x), int(state.awayPos[self.bot_to_mark].y))
        mark_bot_angle=mark_bot_pos.normalizeAngle(state.awayPos[self.bot_to_mark].theta-ballPos.angle(mark_bot_pos))
        
        best_angle=ANGLE_FACTOR*mark_bot_angle+ballPos.angle(mark_bot_pos)

        DISTANCE_ORIENTATION=DISTANCE_FACTOR*mark_bot_pos.dist(ballPos)

        if(DISTANCE_ORIENTATION<200):
            DISTANCE_ORIENTATION=200

        x=int(mark_bot_pos.x+ DISTANCE_ORIENTATION*cos(best_angle))
        y=int(mark_bot_pos.y+ DISTANCE_ORIENTATION*sin(best_angle))
        
        self.sParam.GoToPointP.x=x
        self.sParam.GoToPointP.y=y
        self.sParam.GoToPointP.finalslope = ballPos.normalizeAngle(best_angle + pi)

        sGoToPoint.execute(self.sParam, state, self.bot_id, pub) 
      
    def isComplete(self, state):
        # TO DO use threshold distance instead of actual co ordinates
        if self.destination.dist(state.homePos[self.bot_id]) < self.threshold:
            return True
        elif time.time()-self.begin_time > self.time_out:
            return True
        else:
            return False

    def updateParams(self, state):
        # No parameter to update here
        pass    