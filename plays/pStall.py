import sys
import time
import threading

from utils import tactics_union
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from Stall_function import assign_roles
import rospy
from tactics import *
# from tactics import TAttacker
# from tactics import TMark
# from tactics import TMiddleDefender
# from tactics import TPrimaryDefender
# from tactics import TForward
# from tactics import TReceiver

from utils.robot_threads import robot_thread as thread

class pStall(object):
    def __init__(self,pub):
        self.state = BeliefState()
        self.pub = pub
        self.detected = 6
        self.time = time.clock()

        self.role_list = [['' for i in range(2)] for j in range(self.detected+1)]

        params = tactics_union.Param()

        self.role_list[0][0] = "TAttacker"
        self.role_list[0][1] = params

        self.role_list[1][0] = "TPrimaryDefender"
        self.role_list[1][1] = params

        self.role_list[2][0] = "TMiddleDefender"
        self.role_list[2][1] = params

        self.role_list[3][0] = "TMiddleDefender"
        self.role_list[3][1] = params

        self.role_list[4][0] = "TForward"
        self.role_list[4][1] = params


    def tactic_instance(self, bot_id, tactic_id, params, other_bot_id=-1):
        if tactic_id == "TMiddleDefender":
            instance = TMiddleDefender.TMiddleDefender(bot_id, self.state, other_bot_id, params)
        elif tactic_id == "TAttacker":
            instance = TAttacker.TAttacker(bot_id, self.state, params)
        elif tactic_id == "TForward":
            instance = TForward.TForward(bot_id, self.state, params)
        elif tactic_id == "TPrimaryDefender":
            instance  = TPrimaryDefender.TPrimaryDefender(bot_id, self.state, params)
        elif tactic_id == "TGoalie":
            instance  = TGoalie.TGoalie(bot_id, self.state, params)
        elif tactic_id == "TReceiver":
            instance  = TReceiver.TReceiver(bot_id, self.state, params)
        else:
            instance = TMark.TMark(bot_id, self.state, params)

        return instance

    def update_bs(self,data):  # TO DO create a play super class and shift this method in that
        self.state = data

    def execute(self, data):
        self.update_bs(data) # updating the current befief state
        self.detected = 0
        for idx in range(len(self.state.homeDetected)):
            if self.state.homeDetected[idx]==True:
                self.detected += 1

        assigned_role=assign_roles(self.state)    #Bot id for ATTACKER, PD, MD, MD, FORW

        receiver_bot_id = [-1]

        # Begin five threads for five bots
        instances = []
        robots = []
        # NOT FIVE BUT BOTS DETECTED-1 
        for i in xrange(5):
            instances.append(self.tactic_instance(int(assigned_role[i]), self.role_list[i][0], self.role_list[i][1]))
        for i in xrange(5):
            robots.append(thread(instances[i], self.state, self.pub))
        print '___Begin threads____'
        for i in xrange(5):
            robots[i].start()

        for robot in robots:
            robot.join()
        print '____Exiting threads____'

