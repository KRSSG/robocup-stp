from tactic import Tactic
import time
import sys



from utils.geometry import * 
import skills_union
from utils.config import *
import sGoToPoint
from tactic import Tactic
from geometry import Vector2D
import skills_union
from math import *
from utils.config import *

DISTANCE_ORIENTATION = 2.5*BOT_RADIUS

class TPressureCooker(Tactic):
    def __init__(self,bot_id,state,params=None):
        super(TPressureCooker, self).__init__(bot_id, state, params)
        self.bot_id = bot_id

        self.ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        self.botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))

        self.sParams = skills_union.SParam()

    def execute(self, state , pub, opp_bot):

        p_threat = opp_bot
        p_threat_pos = Vector2D(int(state.awayPos[p_threat].x), int(state.awayPos[p_threat].y))

        x = p_threat_pos.x+ DISTANCE_ORIENTATION*cos(state.awayPos[p_threat].theta)
        y = p_threat_pos.y+ DISTANCE_ORIENTATION*sin(state.awayPos[p_threat].theta)

        self.sParams.GoToPointP.x = x
        self.sParams.GoToPointP.y = y
        self.sParams.GoToPointP.finalslope = self.botPos.normalizeAngle(state.awayPos[p_threat].theta+pi)
        sGoToPoint.execute(self.sParams, state, self.bot_id, pub)

    def isComplete(self, state):
        return False

    def updateParams(self, state):
        pass
