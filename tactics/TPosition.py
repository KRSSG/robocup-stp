from tactic import Tactic
import time
import sys
from math import *


from utils.config import *
from utils.geometry import *

from skills import skills_union
from skills import sKickToPoint
from skills import sGoToPoint
from skills import sDribbleTurn
import numpy as np


KICK_RANGE_THRESH = MAX_DRIBBLE_R   #ASK
THRES  = 0.8
THETA_THRESH = 0.005
TURNING_THRESH = 10
# k=k2=50000 no threshold
THRESH=15*pi/180
BOT_OPP_DIST_THRESH =  500
from time import time

ROWS                                    =  33
COLS                                    =  22
OPTIMAL_DISTANCE                        =  3.0*HALF_FIELD_MAXX/5
BISECTOR_CONST                          =  70
OUR_BOT_APPROACHABILITY_CONST           =  35
OPTIMAL_DISTANCE_CONST                  =  10
AWAY_BOT_APP_GWT                        =  30

k=k2=20*pi/180

class TPosition(Tactic):
    def __init__(self, bot_id, state, param=None):
        super(TPosition, self).__init__( bot_id, state, param)
        self.sParam = skills_union.SParam()
        self.bot_id = bot_id
        self.sParam.GoToPointP.x = param.PositionP.x
        self.sParam.GoToPointP.y = param.PositionP.y
        self.sParam.GoToPointP.finalSlope = param.PositionP.finalSlope
        self.sParam.GoToPointP.finalVelocity = param.PositionP.finalVelocity
        self.UPPER_HALF = Vector2D(-HALF_FIELD_MAXX,OUR_GOAL_MAXY)
        self.LOWER_HALF = Vector2D(-HALF_FIELD_MAXX, OUR_GOAL_MINY)

    def execute(self, state, pub):
        self.sParam.GoToPointP.x = self.param.PositionP.x
        self.sParam.GoToPointP.y = self.param.PositionP.y
        self.sParam.GoToPointP.finalSlope = self.param.PositionP.finalSlope
        self.sParam.GoToPointP.finalVelocity = self.param.PositionP.finalVelocity
        sGoToPoint.execute(self.sParam, state, self.bot_id, pub)


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
