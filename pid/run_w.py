import sys
import os
import rospy

from utils.geometry import Vector2D
from utils.config import *
from krssg_ssl_msgs.srv import path_plan
from krssg_ssl_msgs.msg import point_2d
from profiler_w import *
from pid import pid
from pso import PSO
from error import Error

v = None
kubid = None
expectedTraverseTime = None
pso = None
errorInfo = Error()
REPLAN = 0
FIRST_CALL = 1
homePos = None
expectedTraverseTime = None 

def Get_Omega(start, t, kub_id, totalAngle, homePos_):
    global FIRST_CALL,expectedTraverseTime,v,homePos,kubid
    REPLAN = 0
    homePos = homePos_
    kubid = kub_id
    currAngle = homePos[kub_id].theta
    kubid = kub_id

    if FIRST_CALL:
        v = Omega(totalAngle, start, currAngle)
        expectedTraverseTime = v.getTime(totalAngle)
        FIRST_CALL = 0


    
    if (t - start < expectedTraverseTime):
        if v.trapezoid(t - start, currAngle):
            print v.getOmega(),'get omega '*3
            return v.getOmega()
