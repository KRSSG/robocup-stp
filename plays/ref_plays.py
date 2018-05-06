import sys
import os

sys.path.insert(0, 'plays_py/scripts')
from utils import tactics_union
from utils.robot_threads import robot_thread as thread

from tactic_factory import TStop
from tactic_factory import TMark
from tactic_factory import TPosition

class RefPlay(object):
    tactic_mapping = {"TStop": TStop.TStop,
                      "TMark": TMark.TMark,
                      "TPosition": TPosition.TPosition}
    def __init__(self, state, tactic, params, publisher):
        self.active_robots = 6
        self.role_list = [['' for i in range(2)] for j \
            in range(self.active_robots)]
        self.instances = []
        self.robots = []
        self.state = state
        self.publisher = publisher
        for i in range(self.active_robots):
            self.role_list[i][0] = tactic[i]
            self.role_list[i][1] = params[i]

    def tactic_instance(self):
        for i in range(self.active_robots):
            self.instances.append(RefPlay.tactic_mapping[self.role_list[i][0]]( \
                i, self.state, self.role_list[i][1]))

    def execute(self):
        for i in range(self.active_robots):
            self.robots.append(thread(self.instances[i], self.state, \
                self.publisher))
        for i in range(self.active_robots):
            self.robots[i].start()
        for robot in self.robots:
            robot.join()

class ref_halt(RefPlay):
    def __init__(self, state, publisher):
        params = tactics_union.Param()
        tactic = {0:"TStop", 1:"TStop", 2:"TStop", 3:"TStop", 4:"TStop", 5:"TStop"}
        params = {0:params, 1:params, 2:params, 3:params, 4:params, 5:params}
        RefPlay.__init__(self, state, tactic, params, publisher)

    def tactic_instance(self):
        RefPlay.tactic_instance(self)

    def execute(self):
        RefPlay.execute(self)

class ref_stop(RefPlay):
    def __init__(self, state, publisher):
        tactic = {0:"TPosition", 1:"TPosition", 2:"TPosition", 3:"TPosition", \
                  4:"TPosition", 5:"TPosition"}

        positions = [[0, 0, 0, 0], [1000, 1000, 0, 0], [2000, 2000, 0, 0],
                     [3000, 3000, 0, 0], [-1000, -1000, 0, 0], [-2000, -2000, 0, 0]]
        parameters = dict()
        for i in range(6):
          params = tactics_union.Param()
          params.PositionP.x = positions[i][0]
          params.PositionP.y = positions[i][1]
          params.PositionP.finalSlope = positions[i][2]
          params.PositionP.finalVelocity = positions[i][3]
          parameters[i] = params
        RefPlay.__init__(self, state, tactic, parameters, publisher)

    def tactic_instance(self):
        RefPlay.tactic_instance(self)

    def execute(self):
        self.tactic_instance()
        RefPlay.execute(self)

class ref_normal_start(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_force_start(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_prepare_kickoff_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_prepare_kickoff_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_prepare_penalty_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_prepare_penalty_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_direct_free_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_direct_free_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_indirect_free_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_indirect_free_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_timeout_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_timeout_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_goal_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_goal_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_ball_placement_yellow(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass

class ref_ball_placement_blue(RefPlay):
    def __init__(self):
        pass

    def tactic_instance(self, bot_id, tactic_id, params):
        pass

    def execute(self):
        pass
