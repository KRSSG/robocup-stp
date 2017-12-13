##
## @brief      Omega Profiling.
## 
## Return Omega at current time according to Omega profiler
## on calling getOmega
## @see getOmega()
##
import sys

from math import *
from utils.geometry import Vector2D
from utils.config import *

class Omega():
    # TODO
    # Start Omega, final Omega, maxacc
    
    ##
    ## @brief      Constructor of Omega Profiling.
    ##
    ## @param      path       Path Points
    ## @param      startTime  Starting time of profiling
    ## @param[in]   currAngle   Current Angle of Kub
    ## 
    ##
    def __init__(self, totalAngle, startTime, currAngle):
        # while(1):
        #     print "inside pw"
        self.startTime = startTime
        self.currAngle = currAngle
        self.angle_traversed = 0
        self.Omega = 0.0
        self.totalAngle = totalAngle
        self.maxOmega = MAX_BOT_OMEGA*1.0
        # while True:
        #     print self.maxOmega
        #     pass
        self.maxAcc = MAX_BOT_ACCELERATION = 10.0 #######################
        self.startOmega = 0
        self.finalOmega = 0

    ##
    ## @brief      Sends a stop (Omega).
    ##
    def sendStop(self):
        return 0.0

    def getTotalAngle(Self):
        return self.totalAngle
    ##
    ## @brief      Time to travel "totalAngle"
    ##
    ## @param      totalAngle  Path length traversed
    ##
    ##
    ## Cases:-
    ## 1> Triangle --> Maximum possible Omega is not achieved
    ## 
    ## 2> Trapezoidal ---> Maximum possible Omega attained for plateau
    ##  time
    # def getTime(self,t):
        # return t
    def getTime(self,totalAngle):

        self.startOmega = min(self.startOmega, self.maxOmega)
        self.finalOmega = min(self.finalOmega, self.maxOmega)
        self.rampUpTime = (self.maxOmega - self.startOmega) / self.maxAcc
        # To be modified in function
        self.plateauTime = 0
        self.rampDownTime = -(self.finalOmega - self.maxOmega) / self.maxAcc
        self.rampUpTheta = self.rampUpTime*(self.startOmega + self.maxOmega) / 2.0
        # To be modified in function
        self.plateauTheta = 0
        self.rampDownTheta = self.rampDownTime*(self.maxOmega + self.finalOmega) / 2.0
        if self.rampUpTheta + self.rampDownTheta > self.totalAngle:
            # Triangle case :- Will Not attain maximum possible Omega
            self.maxOmega = sqrt((pow(self.finalOmega,2) + pow(self.startOmega,2) + 2 * self.maxAcc * totalAngle) / 2.0)
            # while True:
            #     print self.maxAcc , totalAngle
            #     pass
            self.rampUpTime = (self.maxOmega - self.startOmega) / self.maxAcc
            self.rampDownTime = -(self.finalOmega - self.maxOmega) / self.maxAcc
            self.rampUpTheta = self.rampUpTime*(self.startOmega + self.maxOmega) / 2.0
            self.rampDownTheta = self.rampDownTime*(self.finalOmega + self.maxOmega) / 2.0
            self.plateauTime = 0
            self.plateauTheta = 0
            # while True:
            #     # print "chelss0",self.rampUpTime , self.rampDownTime,self.maxOmega, self.startOmega, self.maxAcc
            #     print "chelss0",self.maxOmega, self.startOmega, self.maxAcc
            #     pass

            return self.rampUpTime + self.rampDownTime 
        else:
            # Trapezoidal case
            # Attain Maximum Possible Omega for plateau Time
            self.plateauTheta = self.totalAngle - (self.rampUpTheta + self.rampDownTheta)
            self.plateauTime = self.plateauTheta / self.maxOmega
            # while True:
            #     print "chelss1"
            #     pass
            return self.rampUpTime + self.plateauTime + self.rampDownTime

        if totalAngle <= 0:
            # while True:
            #     print "chelss2"
            #     pass
            return 0

        # # Covered whole path
        # if abs(totalAngle - (self.rampUpTheta + self.plateauTheta + self.rampUpTheta)) < 0.0001:
        #     return self.rampUpTime + self.plateauTime + self.rampDownTime

        # if totalAngle <= self.rampUpTheta:
        #     # Time Calculations
        #     # 1/2*a*t^2 + t*vi -d = 0
        #     # t = -b + sqrt*(b^2 -4ac)/(2a)
        #     b = self.startOmega
        #     a = self.maxAcc/2.0
        #     c = -totalAngle
        #     root = sqrt(b*b - 4*a*c)
        #     try:
        #         alpha = (-b + root)/(2*a)
        #         beta = (-b - root)/(2*a)
        #     except Exception as e:
        #         print(e)
        #         return 
        #     if alpha > 0 and alpha <= self.rampUpTime:
        #         return alpha
        #     else:
        #         return beta

        # elif (totalAngle <= self.rampUpTheta + self.plateauTheta ):
        #     Angle = totalAngle - self.rampUpTheta
        #     return self.rampUpTime + Angle/self.maxOmega

        # elif (totalAngle < self.rampUpTheta + self.plateauTheta + self.rampDownTheta):
        #     # Again Time Calculations
        #     Angle = totalAngle - self.rampUpTheta - self.plateauTheta
        #     b = self.maxOmega
        #     a = -self.maxAcc/2.0
        #     c = -Angle
        #     try:
        #         root = sqrt(b*b - 4*a*c)
        #     except Exception as e:
        #         print(e)
        #         return
        #     alpha = (-b + root)/(2*a)
        #     beta = (-b - root)/(2*a)
        #     if alpha > 0 and alpha < self.rampDownTime:
        #         return self.rampUpTime + self.plateauTime + alpha
        #     else:
        #         return self.rampUpTime + self.plateauTime + beta
        # else:
        #     return self.rampUpTime + self.plateauTime + self.rampDownTime

    ##
    ## @brief      Check if Trapezoidal motion is possible
    ##
    ## @param      totalAngle   total angle to turn
    ## @param      maxOmega     Maximum possible Omega
    ## @param      maxAcc       maximum possible accelaration
    ## @param      timeIntoLap  currTime - startTime
    ## @param      self.startOmega   Starting Omega
    ## @param      self.finalOmega   Final Omega
    ##
    def trapezoidalMotion(self, totalAngle, maxOmega, maxAcc, timeIntoLap,
                          startOmega, finalOmega):
        startOmega = min(startOmega, maxOmega)
        finalOmega = min(finalOmega, maxOmega)

        # while True:
        print self.rampUpTime
            # pass

        if (timeIntoLap < 0):
            print("Not started to move")
            self.angle_traversed = 0
            self.Omega = startOmega
            return False
        elif (timeIntoLap < self.rampUpTime):
            
            #
            # Accelerating at @maxAcc
            #
            self.angle_traversed = startOmega * timeIntoLap + 0.5 * maxAcc * timeIntoLap * timeIntoLap
            self.Omega = startOmega + maxAcc * timeIntoLap
            return True
        elif (timeIntoLap < self.rampUpTime + self.plateauTime):
            #
            # Going at @maxOmega
            #
            self.angle_traversed = self.rampUpTheta + (timeIntoLap - self.rampUpTime) * maxOmega
            self.Omega = maxOmega
            return True
        elif (timeIntoLap < self.rampUpTime + self.plateauTime + self.rampDownTime):
            #
            timeIntoRampDown = timeIntoLap - (self.rampUpTime + self.plateauTime)
            self.angle_traversed = 0.5*(-maxAcc) *timeIntoRampDown*timeIntoRampDown
            self.angle_traversed += maxOmega*timeIntoRampDown + (self.rampUpTheta + self.plateauTheta)
            self.Omega = maxOmega - maxAcc*timeIntoRampDown
            return True
        else:
            #
            # At the end of path
            #
            print("At the end of path")
            print(timeIntoLap,self.rampUpTime + self.plateauTime + self.rampDownTime)
            self.angle_traversed = totalAngle
            self.Omega = finalOmega
            return False

    ##
    ## @brief      Gets the Omega.
    ##
    def getOmega(self):
        if(self.totalAngle < 0):
            self.Omega = -self.Omega
        return self.Omega

    ##
    ## @brief      Check if trapezoidal motion is possible
    ##
    ## @param      timeIntoLap  Currtime - startTime
    ##
    def trapezoid(self, timeIntoLap, pos):
        self.currAngle = pos
        valid = self.trapezoidalMotion(self.totalAngle, self.maxOmega, self.maxAcc, timeIntoLap, self.startOmega, self.finalOmega)
        return valid
