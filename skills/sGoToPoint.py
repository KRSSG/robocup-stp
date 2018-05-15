import skill_node
import math
import sys,os



from utils.config import *
from utils.geometry import Vector2D
from math import pi
from velocity.run import *
import rospy,sys
from krssg_ssl_msgs.msg import point_2d
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from krssg_ssl_msgs.msg import gr_Robot_Command
from krssg_ssl_msgs.msg import point_SF

from utils.config import *

POINTPREDICTIONFACTOR = 2

# def reset(bot_id):
#     start_time = rospy.Time.now()
#     start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)
#     os.environ['bot'+str(bot_id)]=str(start_time)




def reset(bot_id):
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)
    os.environ['bot'+str(bot_id)]=str(start_time)

def debug(param, state, bot_id):
	botPos = Vector2D(state.homePos[bot_id].x, state.homePos[bot_id].y)
	destination = Vector2D(param.GoToPointP.x, param.GoToPointP.y)
	align = param.GoToPointP.align
	finalSlope = param.GoToPointP.finalSlope
	dist = botPos.dist(destination)
	print '#'*50
	print 'In sGoToPoint'
	print 'Current bot pos: {}, {}'.format(state.homePos[bot_id].x, state.homePos[bot_id].y)
	print 'Target pos: {}, {}'.format(destination.x, destination.y)
	print 'Align: {}'.format(align)
	if align:
		print 'Finalslope: {}'.format(finalSlope)
		print 'Bot Orientation {}'.format(state.homePos[bot_id].theta)
	print 'Distance: {}'.format(dist)
	print '#'*50

def execute(param, state, bot_id, pub, dribller=False):
    # debug(param,state, bot_id)
    pointPos = Vector2D()
    pointPos.x = int(param.GoToPointP.x)
    pointPos.y = int(param.GoToPointP.y)
    t = rospy.Time.now()
    t = t.secs + 1.0*t.nsecs/pow(10,9)
    start_time = float(os.environ.get('bot'+str(bot_id)))
    [vx, vy, vw, REPLANNED, maxDisToTurn] = Get_Vel(start_time, t, bot_id, pointPos, state.homePos, state.awayPos)    #vx, vy, vw, replanned
    if(REPLANNED):
        print("REPLANNED {}".format(bot_id))
        reset(bot_id)
    botPos = Vector2D(int(state.homePos[bot_id].x), int(state.homePos[bot_id].y))
    v = Vector2D()
    distan = botPos.dist(pointPos)
    ballPos = Vector2D(state.ballPos)
    # maxDisToTurn = distan 

    if param.GoToPointP.align == True:
      angleToTurn = pointPos.normalizeAngle(param.GoToPointP.finalSlope - state.homePos[bot_id].theta)
    else:
      angleToTurn = pointPos.normalizeAngle(botPos.angle(ballPos) - state.homePos[bot_id].theta)
  
    # angleToTurn = v.normalizeAngle((param.GoToPointP.finalSlope)-(state.homePos[bot_id].theta))

    minReachTime = maxDisToTurn / MAX_BOT_OMEGA
    maxReachTime = maxDisToTurn / MIN_BOT_OMEGA

    minTurnTime = angleToTurn / MAX_BOT_OMEGA
    maxTurnTime = angleToTurn / MIN_BOT_OMEGA

    omega = 2*angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)                 

    if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
        if omega < 0:
            omega = -MIN_BOT_OMEGA
        else:
            omega = MIN_BOT_OMEGA

    if angleToTurn==0:
        omega=0

    print("bot id{} vx: {}, vy:{}".format(bot_id,vx,vy))

    if param.GoToPointP.align == False:
        if distan < DRIBBLER_BALL_THRESH:
            if distan < BOT_BALL_THRESH:
                skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,dribller)
              
            else:
                skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
        else:
            skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
    else:
        if distan > BOT_BALL_THRESH:
            skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
        else:
            skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,dribller)





# def execute(param, state, bot_id, pub,dribller = False):
#     t = rospy.Time.now()
#     t = t.secs + 1.0*t.nsecs/pow(10,9)
#     start_time = float(os.environ.get('bot'+str(bot_id)))
#     print(" t - start = ",t-start_time)
#     [vx, vy, vw, REPLANNED] = Get_Vel(start_time, t, bot_id, state.ballPos, state.homePos, state.awayPos)    #vx, vy, vw, replanned
#     print("-------------------REPLANNED = ",REPLANNED)
#     if(REPLANNED):
#         reset(bot_id)
#     print("vx = ",vx)
#     print("vy = ",vy)
#     # print("kubs_id = ",kub.kubs_id)
#     # try:    
#     #     skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, vw, 0,0)
#     # except Exception as e:
#     #     print("In except",e)
#     #     pass

#     # obs = Vector_Obstacle()
#     # for i in range(0,len(state.homeDetected)):
#     #     if state.homeDetected[i] and i != bot_id:
#     #         o = Obstacle()     
#     #         o.x=state.homePos[i].x
#     #         o.y=state.homePos[i].y
#     #         o.radius=3.3*BOT_RADIUS
#     #         obs.push_back(o)

#     # for j in range(0,len(state.awayDetected)):
#     #     if state.awayDetected[j]:
#     #         o = Obstacle()
#     #         o.x=state.awayPos[j].x
#     #         o.y=state.awayPos[j].y
#     #         o.radius=3.3*BOT_RADIUS
#     #         obs.push_back(o)


#     pointPos = Vector2D()
#     pointPos.x = int(param.GoToPointP.x)
#     pointPos.y = int(param.GoToPointP.y)
#     # point = Vector2D()
#     # nextWP = Vector2D()
#     # nextNWP = Vector2D()

#     # pathplanner = MergeSCurve()

# #     pathplanner.plan(botPos,pointPos,nextWP,nextNWP,obs,len(obs),bot_id, True)
# #     v = Vector2D()
# #     distan = botPos.dist(pointPos)
# #     maxDisToTurn = distan 
# #     angleToTurn = v.normalizeAngle((param.GoToPointP.finalSlope)-(state.homePos[bot_id].theta))

# #     minReachTime = maxDisToTurn / MAX_BOT_OMEGA
# #     maxReachTime = maxDisToTurn / MIN_BOT_OMEGA

# #     minTurnTime = angleToTurn / MAX_BOT_OMEGA
# #     maxTurnTime = angleToTurn / MIN_BOT_OMEGA

# #     speed = 0.0
# #     omega = 2*angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)                 

# #     if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
# #         if omega < 0:
# #             omega = -MIN_BOT_OMEGA
# #         else:
# #             omega = MIN_BOT_OMEGA

# #     from math import exp

# #     speed= 2*maxDisToTurn*MAX_BOT_SPEED/(HALF_FIELD_MAXX)
# #     if (speed)< 2*MIN_BOT_SPEED:
# #         speed=2*MIN_BOT_SPEED
# #     if  (speed > MAX_BOT_SPEED):
# #         speed=MAX_BOT_SPEED    
  
# #     vec = Vector2D()


# #     motionAngle = nextWP.angle(botPos)
# #     theta  = motionAngle - state.homePos[bot_id].theta
# #     if param.GoToPointP.align == False:
# #         if distan < DRIBBLER_BALL_THRESH:
# #             if distan < BOT_BALL_THRESH:
# #                 skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,dribller)
              
# #             else:
# #                 skill_node.send_command(pub, state.isteamyellow, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, 0, dribller)
# #         else:
# #             skill_node.send_command(pub, state.isteamyellow, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, 0, dribller)
# #     else:
# #         if distan > BOT_BALL_THRESH:
# #             skill_node.send_command(pub, state.isteamyellow, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, 0, dribller)
# #         else:
# #             skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,dribller)

#     # pathplanner.plan(botPos,pointPos,nextWP,nextNWP,obs,len(obs),bot_id, True)
#     v = Vector2D()
#     distan = botPos.dist(pointPos)
#     maxDisToTurn = distan 
#     angleToTurn = v.normalizeAngle((param.GoToPointP.finalSlope)-(state.homePos[bot_id].theta))

#     minReachTime = maxDisToTurn / MAX_BOT_OMEGA
#     maxReachTime = maxDisToTurn / MIN_BOT_OMEGA

#     minTurnTime = angleToTurn / MAX_BOT_OMEGA
#     maxTurnTime = angleToTurn / MIN_BOT_OMEGA

#     # speed = 0.0
#     omega = 2*angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)                 

#     if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
#         if omega < 0:
#             omega = -MIN_BOT_OMEGA
#         else:
#             omega = MIN_BOT_OMEGA

#     # from math import exp

#     # speed= 2*maxDisToTurn*MAX_BOT_SPEED/(HALF_FIELD_MAXX)
#     # if (speed)< 2*MIN_BOT_SPEED:
#     #     speed=2*MIN_BOT_SPEED
#     # if  (speed > MAX_BOT_SPEED):
#     #     speed=MAX_BOT_SPEED    
  
#     # vec = Vector2D()


#     # motionAngle = nextWP.angle(botPos)
#     # theta  = motionAngle - state.homePos[bot_id].theta
#     if param.GoToPointP.align == False:
#         if distan < DRIBBLER_BALL_THRESH:
#             if distan < BOT_BALL_THRESH:
#                 skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,dribller)
              
#             else:
#                 skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
#         else:
#             skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
#     else:
#         if distan > BOT_BALL_THRESH:
#             skill_node.send_command(pub, state.isteamyellow, bot_id, vx, vy, omega, 0, dribller)
#         else:
#             skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0,dribller)


