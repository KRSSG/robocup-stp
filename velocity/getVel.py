import sys
import os
import rospy

from utils.geometry import Vector2D
from utils.config import *
from krssg_ssl_msgs.srv import path_plan
from krssg_ssl_msgs.msg import point_2d

from profiler import *
from pid import pid
from pso import PSO
from error import Error

DESTINATION_THRESH = 2*BOT_BALL_THRESH

def distance_(a, b):
    dx = a.x-b.x
    dy = a.y-b.y
    return sqrt(dx*dx+dy*dy)
    
class GetVelocity(object):
    """docstring for GetVelocity"""
    def __init__(self, start_time, kubs_id):
        super(GetVelocity, self).__init__()
        self.start_time = start_time
        self.kubid = kubs_id
        self.expectedTraverseTime = None
        self.pso = None
        # self.# self.pso = self.PSO(5,20,1000,2,1,0.5)
        self.errorInfo = Error()
        self.REPLAN = 0
        self.homePos = None
        self.awayPos = None
        self.prev_target = None
        self.FIRST_CALL = 1


    def execute(self, t, kub_id, target, homePos_, awayPos_,avoid_ball=False):

        # Return vx,vy,vw,self.replan,remainingDistance
        self.target = target

        self.REPLAN = 0
        self.homePos = homePos_
        self.awayPos = awayPos_
        self.kubid = kub_id
        #self.FIRST_CALL = int(os.environ.get('fc'+str(self.kubid)))
        print(self.FIRST_CALL)
        # if not self.prev_target==None:
        if isinstance(self.prev_target, Vector2D):
            dist = distance_(self.target, self.prev_target)
            if(dist>DESTINATION_THRESH):
                self.REPLAN = 1
        self.prev_target = self.target        
        # print("in getVelocity, self.FIRST_CALL = ",self.FIRST_CALL)
        curPos = Vector2D(int(self.homePos[self.kubid].x),int(self.homePos[self.kubid].y))
        distance = sqrt(pow(self.target.x - self.homePos[self.kubid].x,2) + pow(self.target.y - self.homePos[self.kubid].y,2))
        if(self.FIRST_CALL):
            print("BOT id:{}, in first call, timeIntoLap: {}".format(self.kubid, t-self.start_time))
            startPt = point_2d()
            startPt.x = self.homePos[self.kubid].x
            startPt.y = self.homePos[self.kubid].y
            self.findPath(startPt, self.target, avoid_ball)
            #os.environ['fc'+str(self.kubid)]='0'
            self.FIRST_CALL = 0

        else:
            print("Bot id:{}, not first call, timeIntoLap: {}".format(self.kubid,t-self.start_time))
        if distance < 1.5*BOT_BALL_THRESH:
            return [0,0,0,0,0]
        # print("ex = ",self.expectedTraverseTime) 
        # print("t = ",t," start = ",start)
        remainingDistance = 0
        # print("ex = ",self.expectedTraverseTime) 
        # print("t = ",t," start = ",start)
        if (t-self.start_time< self.expectedTraverseTime):
            if self.v.trapezoid(t-self.start_time,curPos):
                index = self.v.GetExpectedPositionIndex()
                if index == -1:
                    vX,vY,eX,eY = self.v.sendVelocity(self.v.getVelocity(),self.v.motionAngle[index],index)
                    vX,vY = 0,0

                else:
                    remainingDistance = self.v.GetPathLength(startIndex=index)
                    vX,vY,eX,eY = self.v.sendVelocity(self.v.getVelocity(),self.v.motionAngle[index],index)

            else:
                # print(t-self.start_time, self.expectedTraverseTime)
                if self.expectedTraverseTime == 'self.REPLAN':
                    self.REPLAN = 1
                # print("Motion Not Possible")
                vX,vY,eX,eY = 0,0,0,0
                flag = 1
        else:
            # print("TimeOUT, self.REPLANNING")
            vX,vY,eX,eY = 0,0,0,0
            self.errorInfo.errorIX = 0.0
            self.errorInfo.errorIY = 0.0
            self.errorInfo.lastErrorX = 0.0
            self.errorInfo.lastErrorY = 0.0
            startPt = point_2d()
            startPt.x = self.homePos[self.kubid].x
            startPt.y = self.homePos[self.kubid].y
            self.findPath(startPt,self.target, avoid_ball)

        errorMag = sqrt(pow(eX,2) + pow(eY,2))

        should_replan = self.shouldReplan()
        if(should_replan == True):
            self.v.velocity = 0
            # print("self.v.velocity now = ",self.v.velocity)
        # print("entering if, should_replan = ", should_replan)
        if  should_replan or \
            (errorMag > 350 and distance > 1.5* BOT_BALL_THRESH) or \
            self.REPLAN == 1:
                # print("______________here____________________")
                # print("condition 1",should_replan)
                # print("error magnitude", errorMag)
                # print("distance threshold",distance > 1.5* BOT_BALL_THRESH)
                # print("condition 2",errorMag > 350 and distance > 1.5* BOT_BALL_THRESH)
                # print("condition 3",self.REPLAN)
                # print("Should self.Replan",should_replan)
                # print("ErrorMag",errorMag > 350 and distance > 2*BOT_BALL_THRESH)
                self.REPLAN = 1
                startPt = point_2d()
                startPt.x = self.homePos[self.kubid].x
                startPt.y = self.homePos[self.kubid].y
                self.findPath(startPt,self.target, avoid_ball)
                return [0,0,0, self.REPLAN,0]  

        else:
            self.errorInfo.errorX = eX
            self.errorInfo.errorY = eY
            vX,vY = pid(vX,vY,self.errorInfo,self.pso)
            botAngle = self.homePos[self.kubid].theta
            vXBot = vX*cos(botAngle) + vY*sin(botAngle)
            vYBot = -vX*sin(botAngle) + vY*cos(botAngle)

            return [vXBot, vYBot, 0, self.REPLAN,remainingDistance]            

            return [vXBot, vYBot, 0, self.REPLAN]            

        # print("end getVelocity")    
        
    def shouldReplan(self):
        # print("velocity = ",self.v.velocity)
        if self.v.velocity < 10:
            return False

        myPos = Vector2D(int(self.homePos[self.kubid].x),int(self.homePos[self.kubid].y))
        obsPos = Vector2D()
        index = self.v.GetExpectedPositionIndex()
        for i in xrange(len(self.homePos)):
            if i == self.kubid:
                pass
            else:
                obsPos.x = int(self.homePos[i].x)
                obsPos.y = int(self.homePos[i].y)
                if self.v.ellipse(myPos,obsPos,self.v.motionAngle[index]):
                    return True
        for i in xrange(len(self.awayPos)):
            obsPos.x = int(self.awayPos[i].x)
            obsPos.y = int(self.awayPos[i].y)
            if self.v.ellipse(myPos,obsPos,self.v.motionAngle[index]):
                return True

        return False

    def findPath(self,startPoint,end,avoid_ball=False):
        print("Bot id: {}, calculating path".format(self.kubid))
        # global FLAG_PATH_RECEIVED, self.REPLAN
        # self.FLAG_PATH_RECEIVED = 1
        self.REPLAN = 1
        startPt = point_2d()
        self.target = point_2d()
        startPt.x = startPoint.x
        startPt.y = startPoint.y
        self.target.x = end.x
        self.target.y = end.y
        # print("Start Point ",startPt.x,startPt.y)
        # print("self.Target Point",self.target.x,self.target.y)
        # print("Waiting for service")
        rospy.wait_for_service('planner')

        planner = rospy.ServiceProxy('planner', path_plan)

        message = planner(self.kubid,startPt,self.target,avoid_ball)
        path = []
        for i in xrange(len(message.path)):
            path = path + [Vector2D(int(message.path[i].x),int(message.path[i].y))]
        # start = rospy.Time.now()
        # start = 1.0*start.secs + 1.0*start.nsecs/pow(10,9)
        self.start_time = rospy.Time.now()
        self.start_time = 1.0*self.start_time.secs + 1.0*self.start_time.nsecs/pow(10,9)
        os.environ['bot'+str(self.kubid)]=str(self.start_time)

        self.v = Velocity(path,self.start_time,startPt)
        self.v.updateAngle()
        self.expectedTraverseTime = self.v.getTime(self.v.GetPathLength())
        time_cal = self.expectedTraverseTime
        # self.pso = self.PSO(5,20,1000,1,1,0.5)
        self.errorInfo = Error()
        # print("Path Planned")
