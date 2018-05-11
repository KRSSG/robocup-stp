import sys
import rospy
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
import threading
import time
from math import *
from utils.math_functions import *
from utils.geometry import *
from utils.config import *

def attacker_selector(state):
	#debug(state)
	weights = [20*0.15847, 0.0008888*8 , 1500000]
	min_strength = 99999999
	for bots in range(len(state.homePos)):
		print "id = ",bots
		closest_opp_bot = -1
		second_closest_opp_bot = -1
		curr_bot_pos = Vector2D(int(state.homePos[bots].x), int(state.homePos[bots].y))
		ball_pos = Vector2D(int(state.ballPos.x),int(state.ballPos.y))
		bot_ball_dist = ball_pos.dist(curr_bot_pos)
		temp = Vector2D()
		angle1 = curr_bot_pos.angle(ball_pos)
		angle = fabs(temp.normalizeAngle(angle1-state.homePos[bots].theta))
		# print "angle = ", angle
		#if angle < 0 and ball_pos.y > curr_bot_pos.y :
			#angle = 3.141592654 + angle
		#print "anglen = ", angle
		#angle = temp.normalizeAngle(angle)
		#print "anglen = ", angle
		mindist = 9999999
		for opponents in xrange(len(state.awayPos)):
			if state.awayPos[opponents].x > state.homePos[bots].x:
				curr_opp_bot = Vector2D(int(state.awayPos[opponents].x),int(state.awayPos[opponents].y))
				# print'Bot id: {}, Pos {},{}'.format(opponents,curr_opp_bot.x, curr_opp_bot.y)
				dist_bot = curr_bot_pos.dist(curr_opp_bot)
				# print opponents , " " ,mindist , " " , dist_bot
				# print int(state.awayPos[opponents].x)," " ,int(state.awayPos[opponents].y)
				if dist_bot < mindist:
					
					mindist = dist_bot
					closest_opp_bot = opponents
		mindist = 9999999
		for opponents in xrange(len(state.awayPos)):
			if state.awayPos[opponents].x > state.homePos[bots].x:
				if not opponents == closest_opp_bot:			
					curr_opp_bot = Vector2D(int(state.awayPos[opponents].x),int(state.awayPos[opponents].y))
					dist_bot = curr_bot_pos.dist(curr_opp_bot)
					if dist_bot < mindist:
						mindist = dist_bot
						second_closest_opp_bot = opponents

		opp_bot_1 = Vector2D(int(state.awayPos[closest_opp_bot].x), int(state.awayPos[closest_opp_bot].y))
		opp_bot_2 = Vector2D(int(state.awayPos[second_closest_opp_bot].x),int(state.awayPos[second_closest_opp_bot].y))
		free_space = area_of_triangle(curr_bot_pos, opp_bot_1,opp_bot_2)
		try:
			strength = angle*weights[0] + bot_ball_dist*weights[1] + weights[2]/free_space
		except:
			strength = angle*weights[0] + bot_ball_dist*weights[1] + weights[2]/50000
		print "angle_strength = " , angle*weights[0]
		print "dist_strength = ", bot_ball_dist*weights[1]
		print "closest bots =" , closest_opp_bot , " " , second_closest_opp_bot
		print "free_space_sternth =" , weights[2]/free_space
		print "strength = ",strength
		if strength < min_strength:
			min_strength = strength
			attacker_bot_id = bots

	print attacker_bot_id
	return attacker_bot_id