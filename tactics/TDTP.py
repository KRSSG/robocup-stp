from tactic import Tactic
import time
import sys
from utils.config import *
from utils.geometry import *
from skills import skills_union
from skills import sKick
from skills import sKickToPoint
from skills import sGoToPoint
from skills import sGoalie
from skills import sStop
from tactic import Tactic


class TDTP(Tactic):
    def __init__(self, bot_id, state, param = None):
        super(TDTP, self).__init__(bot_id, state, param)

    def execute(self, state, pub):
        point = Vector2D(int(self.param.DribbleTurnP.x), int(self.param.DribbleTurnP.y));
        ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
        botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
        dist = botPos.dist(ballPos)
        angleToTurn = point.normalizeAngle(state.homePos[self.bot_id].theta - point.angle(ballPos))
        pointDis = botPos.dist(point)
        goalBotAngle = point.angle(botPos)
        ballBotAngle = ballPos.angle(botPos)
        angle = point.angle(ballPos)
        delta = 0.085 if pointDis != 0 else 3.0/4
        angleUp = angle + delta
        angleDown = angle - delta

        if dist >= 2.0: # DRIBBLER_BALL_THRESH:
            sParams = skills_union.SParam()
            sParams.GoToPointP.x = state.ballPos.x
            sParams.GoToPointP.y = state.ballPos.y
            sParams.GoToPointP.finalslope = ballPos.angle(botPos)
            sParams.GoToPointP.finalVelocity = 0
            sGoToPoint.execute(sParams, state, self.bot_id, pub)

    def updateParams(self, state):
		# No parameter to update here
		pass

    def isComplete(self, state):
        pass
