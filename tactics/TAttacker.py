from tactic import Tactic
import time
import sys
from math import *

import enum

#####################
#change opp_goalie##
####################

from utils.config import *
from utils.geometry import *
from skills import skills_union
from skills import sKick
from skills import sKickToPoint
from skills import sGoToPoint
from skills import sGoalie
from skills import sStop
from tactic import Tactic
from skills import sGoToBall
from skills import sTurnToPoint
from evo_fuzz import *


import numpy as np
from numpy import array,inf
from isPossible import isPossible

k1 = True
k2 = True

class TAttacker(Tactic):
	def __init__(self, bot_id, state, params=None):
		super(TAttacker, self).__init__( bot_id, state, params)
		self.sParams = skills_union.SParam()
		self.bot_id = bot_id
		self.receive_bot_id = -1
		self.passer_bot_id = -1 
		self.UPPER_HALF = Vector2D(-HALF_FIELD_MAXX,OUR_GOAL_MAXY)
		self.LOWER_HALF = Vector2D(-HALF_FIELD_MAXX,OUR_GOAL_MINY)

		self.GOAL_UPPER = Vector2D(HALF_FIELD_MAXX,OUR_GOAL_MAXY*3)
		self.GOAL_LOWER = Vector2D(HALF_FIELD_MAXX,OUR_GOAL_MINY*3)

	class State(enum.Enum):
		#shoot towards goal 
		shoot = 1
		#cross pass
		cross_pass = 2
		#cross receive
		cross_receive = 3

	def getState(self,state):
		botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
		ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
		ballVel = Vector2D(int(state.ballVel.x) , int(state.ballVel.y))
		goal_angle_upper = atan2((self.GOAL_UPPER.y-botPos.y)*1.0, (self.GOAL_UPPER.x-botPos.x))
		goal_angle_lower = atan2((self.GOAL_LOWER.y-botPos.y)*1.0, (self.GOAL_LOWER.x-botPos.x))
		goal_angle_mid   = 0.5*(goal_angle_lower+goal_angle_upper)
		global k1
		global k2
		for away_bot in xrange(len(state.awayPos)):
			
			if state.awayPos[away_bot].x > state.homePos[self.bot_id].x:
				if away_bot == 4:
					continue
				###print (state.awayPos[away_bot].x, state.homePos[self.bot_id].x, "chutiya.....")
				away_BOT = Vector2D (int(state.awayPos[away_bot].x), int(state.awayPos[away_bot].y))
				try:
					bot_angle = atan2((away_BOT.y - botPos.y)*1.0, (away_BOT.x - botPos.x))
				except:
					bot_angle = fabs((away_BOT.y - botPos.y))

				###print("bhosdiwala angles ",bot_angle, goal_angle_lower, goal_angle_mid, goal_angle_upper, away_bot)
				if bot_angle > goal_angle_lower and bot_angle < goal_angle_mid:
					k1=False
					break
					 
				if bot_angle > goal_angle_mid and bot_angle < goal_angle_upper:
					k2=False
					break
				##print(k1,k2)
		for home_bot in xrange(len(state.homePos)):
			if home_bot == state.our_goalie:
				continue
			
			if state.homePos[home_bot].x > state.homePos[self.bot_id].x:
				###print (state.homePos[home_bot].x, state.homePos[self.bot_id].x, "chutiya.....")
				home_BOT = Vector2D (int(state.homePos[home_bot].x), int(state.homePos[home_bot].y))
				try:
					bot_angle = atan2((home_BOT.y - botPos.y)*1.0, (home_BOT.x - botPos.x))
				except:
					bot_angle = fabs((home_BOT.y - botPos.y))

				###print("bhosdiwala angles ",bot_angle, goal_angle_lower, goal_angle_mid, goal_angle_upper, home_bot)
				if bot_angle > goal_angle_lower and bot_angle < goal_angle_mid:
					k1=False
					break
				if bot_angle > goal_angle_mid and bot_angle < goal_angle_upper:
					k2=False
					break

		if k1 or k2 or ballPos.x > HALF_FIELD_MAXX - DBOX_HEIGHT:
			print "shoot_State"
			return TAttacker.State.shoot

		if fabs(atan2(ballVel.y,ballVel.x) - atan2((botPos.y-ballPos.y),(botPos.x-ballPos.x))) < 0.01 :
			print 'cross_receive'
			return TAttacker.State.cross_receive
		print 'cross_pass'
		return TAttacker.State.cross_pass


	def execute(self,state,pub):
		ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
		botPos = Vector2D(int(state.homePos[self.bot_id].x), int(state.homePos[self.bot_id].y))
		ballVel = Vector2D(int(state.ballVel.x) , int(state.ballVel.y))
		gameState = self.getState(state)
		global k1,k2

		if gameState == TAttacker.State.shoot :
			# if fabs(ballPos.dist(botPos)>BOT_BALL_THRESH/400):
			#     sGoToBall.execute(self.sParams, state, self.bot_id, pub)
			# #fuzzy logic to find best angle
			# #print "shoot_State"
			if k1 and not k2:
				self.sParams.KickToPointP.x = HALF_FIELD_MAXX
				self.sParams.KickToPointP.y = 0.8*OUR_GOAL_MINY
				self.sParams.KickToPointP.power = 7
				sKickToPoint.execute(self.sParams, state, self.bot_id, pub)
				#print "shot"
			elif k2 and not k1:
				self.sParams.KickToPointP.x = HALF_FIELD_MAXX
				self.sParams.KickToPointP.y = 0.8*OUR_GOAL_MAXY
				self.sParams.KickToPointP.power = 7
				sKickToPoint.execute(self.sParams, state, self.bot_id, pub)
				#print "shot"
			else:
				if state.awayPos[4].y < 0 :
					self.sParams.KickToPointP.x = HALF_FIELD_MAXX      
					self.sParams.KickToPointP.y = 0.8*OUR_GOAL_MAXY
					self.sParams.KickToPointP.power = 7
					sKickToPoint.execute(self.sParams, state, self.bot_id, pub)
					#print "shot"
				if state.awayPos[4].y > 0:
					self.sParams.KickToPointP.x = HALF_FIELD_MAXX      
					self.sParams.KickToPointP.y = 0.8*OUR_GOAL_MINY
					self.sParams.KickToPointP.power = 7
					sKickToPoint.execute(self.sParams, state, self.bot_id, pub)
					#print "shot"



		if gameState == TAttacker.State.cross_pass :
			# if fabs(ballPos.dist(botPos)>BOT_BALL_THRESH/4):
			# 	sGoToBall.execute(self.sParams, state, self.bot_id, pub)
			print "pass_state"
			p = get_all(state,self.bot_id)
			self.receive_bot_id = p[0]
			print "receiver =" , p[0]
			self.sParams.KickToPointP.x = state.homePos[self.receive_bot_id].x
			self.sParams.KickToPointP.y = state.homePos[self.receive_bot_id].y
			self.sParams.KickToPointP.power = 7
			sKickToPoint.execute(self.sParams,state,self.bot_id,pub)

		if gameState == TAttacker.State.cross_receive :
			mindist = 9999999
			print "recieve_state"
			for our_bot in xrange(len(state.homePos)):
				if state.homePos[our_bot].x > state.homePos[bots].x:
					curr_home_bot = Vector2D(int(state.homePos[our_bot].x),int(state.homePos[our_bot].y))
					# #print'Bot id: {}, Pos {},{}'.format(our_bot,curr_opp_bot.x, curr_opp_bot.y)
					dist_bot = ballPos.dist(curr_home_bot)
					# #print our_bot , " " ,mindist , " " , dist_bot
					# #print int(state.homePos[our_bot].x)," " ,int(state.homePos[our_bot].y)
					if dist_bot < mindist:
						
						mindist = dist_bot
						closest_home_bot = our_bot
			passer_bot_id = closest_home_bot
			self.SParams.sTurnToPoint.x = state.homePos[self.passer_bot_id].x
			self.SParams.sTurnToPoint.y = state.homePos[self.passer_bot_id].y
			self.SParams.sTurnToPoint.max_omega = MAX_BOT_OMEGA

	def isComplete(self, state):
		return False

	def updateParams(self, state):
		pass
