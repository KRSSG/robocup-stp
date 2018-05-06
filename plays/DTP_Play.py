import sys
import time
import threading
from utils import tactics_union
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import gr_Commands
from plays.Stall_function import assign_roles
import rospy
from utils.config import *
from tactics import *
from utils.robot_threads import robot_thread as thread

class DTP_Play(object):
    def __init__(self,pub):
        self.state = BeliefState()
        self.pub = pub
        self.time = time.clock()
        self.detected = 6
        self.role_list = [['' for i in range(2)] for j in range(self.detected)]

        params = tactics_union.Param()

        params.DribbleTurnPassP.x = -HALF_FIELD_MAXX
        params.DribbleTurnPassP.y = 0

        self.role_list[0][0] = "TDTP"
        self.role_list[0][1] = params

        self.role_list[1][0] = "TStop"
        self.role_list[1][1] = params

        self.role_list[2][0] = "TStop"
        self.role_list[2][1] = params

        self.role_list[3][0] = "TStop"
        self.role_list[3][1] = params

        self.role_list[4][0] = "TStop"
        self.role_list[4][1] = params

        self.role_list[5][0] = "TStop"
        self.role_list[5][1] = params


    def tactic_instance(self, bot_id, tactic_id, params):
        if tactic_id == "TDTP":
            instance = TDTP.TDTP(bot_id, self.state, params)
        elif tactic_id == "TStop":
            instance = TStop.TStop(bot_id, self.state, params)

        return instance

    def update_bs(self,data):  # TO DO create a play super class and shift this method in that
        self.state = data

    def execute(self, data):
        self.update_bs(data) # updating the current befief state
        self.detected = 0
        for idx in range(len(self.state.homeDetected)):
            if self.state.homeDetected[idx]==True:
                self.detected += 1

        # Begin five threads for five bots
        instances = []
        robots = []
        # NOT FIVE BUT BOTS DETECTED-1 
        count = 0 
        for i in xrange(5):
            if i == data.our_goalie:
                continue
            instances.append(self.tactic_instance(i, self.role_list[i][0], self.role_list[i][1]))

        count = 0 
        for i in xrange(5):
            if i == data.our_goalie:
                continue
            robots.append(thread(instances[count], self.state, self.pub))
            count = count+1
        print '___Begin threads____'
        count = 0
        for i in xrange(5):
            if i == data.our_goalie:
                continue
            robots[count].start()
            count = count+1


        for robot in robots:
            robot.join()
        print '____Exiting threads____'
