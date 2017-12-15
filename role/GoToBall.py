from enum import Enum
import behavior
import _GoToPoint
import rospy
from utils.math_functions import *
from utils.config import *
class GoToBall(behavior.Behavior):
    """docstring for GoToBall"""
    class State(Enum):
        setup = 1 
        drive = 2
        near = 3
    ##
    ## @brief      
    ## Constructs the object.
    ##
    ## @param      self        The object
    ## @param      kub         The kub
    ## @param      theta       The theta
    ## @param      continuous  The continuous
    ##
    def __init__(self,kub,theta,continuous=False):

        super(GoToBall,self).__init__()
        self.kub = kub

        self.theta = theta

        self.add_state(GoToBall.State.setup,
            behavior.Behavior.State.running)

        self.add_state(GoToBall.State.drive,
            behavior.Behavior.State.running)
        
        self.add_state(GoToBall.State.near,
            behavior.Behavior.State.running)

        self.add_transition(behavior.Behavior.State.start,
            GoToBall.State.setup,lambda: True,'immediately')

        self.add_transition(GoToBall.State.setup,
            GoToBall.State.drive,lambda: self.target_present(),'setup')

        self.add_transition(GoToBall.State.drive,
            GoToBall.State.drive,lambda: not self.at_target_point(),'restart')

        self.add_transition(GoToBall.State.drive,
            GoToBall.state.near,lambda:self.at_target_point(),'complete')

        self.add_transition(GoToBall.State.near,
            GoToBall.State.near,lambda:not self.at_ball_pos(),'restart')

        self.add_transition(GoToBall.State.near,
            behavior.Behavior.State.completed,lambda:self.at_ball_pos(),'complete')

    def target_present(self):
        return self.target_point is not None

    def at_target_point(self):
        #print (dist(self.target_point,self.kub.get_pos(),210)
        return dist(self.target_point,self.kub.get_pos()) < 210.0

    def at_ball_pos(self):
        return dist(self.kub.state.ballPos,self.kub.get_pos()) < 210.0

    def terminate(self):
        super().terminate()
        
    def on_enter_setup(self):
        pass
    def execute_setup(self):
        self.target_point = getPointBehindTheBall(self.kub.state.ballPos,self.theta)
        _GoToPoint.init(self.kub, self.target_point, self.theta)
        pass
        
    def on_exit_setup(self):
        pass

    def on_enter_drive(self):
        pass

    def execute_drive(self):
        start_time = rospy.Time.now()
        start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)   
        t = _GoToPoint.execute(start_time)

    def on_exit_drive(self):
        pass

    def on_enter_near(self):
        _GoToPoint.init(self.kub, self.kub.state.ballPos, 0.0)
        pass

    def execute_near(self):
        start_time = rospy.Time.now()
        start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)   
        t = _GoToPoint.execute(start_time)

    def on_exit_near(self):
        pass
