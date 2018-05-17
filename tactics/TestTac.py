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
from skills import sGoToBall
from tactic import Tactic
from skills import sTurnToPoint
from skills import sGoalie


import enum
from tactic import Tactic
from math import *
from numpy import inf,array,linalg
from utils.config import *

class TestTac(Tactic):
    def __init__(self,bot_id,state,params=None):
        # print("int TestTac constru")
        super(TestTac, self).__init__(bot_id, state, params)
        self.sParams = skills_union.SParam()

    def execute(self, state , pub):
        # print("int TestTac execute")
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
        ballVel = Vector2D(int(state.ballVel.x) , int(state.ballVel.y))
        distance = botPos.dist(ballPos)
        
        self.sParams.GoToPointP.x = ballPos.x
        self.sParams.GoToPointP.y = ballPos.y
        # self.sParams.GoToBallP.finalslope = 3*pi/4.0
        # self.sParams.GoToBallP.align = 3*pi/4.0
        sGoToPoint.execute(self.sParams, state, self.bot_id, pub)

       


    def isComplete(self, state):
        return False

    def updateParams(self, state):
        pass
