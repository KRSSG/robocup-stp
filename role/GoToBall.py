from enum import Enum
import behavior
import _Move
from utils.math_functions import *
import _GoToPoint
class GoToBall(behavior.Behavior):
    """docstring for GoToBall"""
    ##
    ## @brief      Class for state.
    ##
    class State(Enum):
        setup = 1 
        drive = 2
        near = 3

    ##
    ## @brief      Constructs the object.
    ##
    ## @param      self   The object
    ## @param      point  The point
    ##
    def __init__(self,kub,theta,continuous=False):
        # print "gtp"
        #GoToBall.behavior.Behavior()
        #g = behavior.Behavior()
        #print "gtp2"
        super(GoToBall,self).__init__()
        self.kub = kub
        #self.state = state

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
            GoToBall.State.drive,lambda: self.target_present,'setup')

        self.add_transition(GoToBall.State.drive, 
            GoToBall.State.near, lambda: self.at_new_point(),'complete')

        self.add_transition(GoToBall.State.drive,
            GoToBall.State.drive,lambda: not self.at_new_point(),'restart')

        self.add_transition(GoToBall.State.near,
            behavior.Behavior.State.completed,lambda:self.kub_near_ball(),'near')

        self.add_transition(GoToBall.State.near,
            GoToBall.State.near,lambda: not self.kub_near_ball(),'restart near')


    ##
    ## @brief      { function_description }
    ##
    ## @param      self  The object
    ##
    ## @return     { description_of_the_return_value }
    ##
    def target_present(self):
        return self.target_point is not None

    ##
    ## @brief      { function_description }
    ##
    ## @return     { description_of_the_return_value }
    ##

    def kub_near_ball(self):
        return dist(self.kub.state.ballPos, self.new_point) < 100.0
        
    def at_new_point(self):
        return not self.is_move_completed

        
    def on_enter_setup(self):
        pass

    def execute_setup(self):
        self.target_point = getPointBehindTheBall(self.kub.state.ballPos,self.theta)
        _Move.init(self.kub,self.theta)
        pass
        
    def on_exit_setup(self):
        pass

    def on_enter_drive(self):
        pass

    def terminate(self):
        super().terminate()
    ##
    ## @brief      { function_description }
    ##
    ## @param      self   The object
    ## @param      kub    The kub
    ## @param      state  The state
    ##
    ## @return     { description_of_the_return_value }
    ##
    def execute_drive(self):
        self.is_move_completed = _Move.run()
        # print (self.is_move_completed,"fghjhgfdxcgvbjhytdfxcbgv")
        self.new_point = self.kub.get_pos()
        

    
    def on_exit_drive(self):
        pass

    def on_enter_near(self):
        _GoToPoint.init(self.kub,self.kub.state.ballPos,self.theta)
        pass

    def on_exit_near(self):
        pass

    def execute_near(self):
        t = _GoToPoint.run()
        self.new_point = self.kub.get_pos()












# from enum import Enum
# import behavior
# import _Move
# from utils.math_functions import *

# class GoToBall(behavior.Behavior):
#     """docstring for GoToBall"""
#     ##
#     ## @brief      Class for state.
#     ##
#     class State(Enum):
#         setup = 1 
#         drive = 2
#         near = 3

#     ##
#     ## @brief      Constructs the object.
#     ##
#     ## @param      self   The object
#     ## @param      point  The point
#     ##
#     def __init__(self,kub,theta = 0.0, continuous=False):
#         #GoToBall.behavior.Behavior()
#         #g = behavior.Behavior()
#         print "gtp2"
#         super(GoToBall,self).__init__()
#         self.kub = kub

#         self.theta = theta

#         self.add_state(GoToBall.State.setup,
#             behavior.Behavior.State.running)
#         self.add_state(GoToBall.State.drive,
#             behavior.Behavior.State.running)
#         self.add_state(GoToBall.State.near,
#             behavior.Behavior.State.running)
        

#         self.add_transition(behavior.Behavior.State.start,
#             GoToBall.State.setup,lambda: True,'immediately')

#         self.add_transition(GoToBall.State.setup,
#             GoToBall.State.drive,lambda: self.move_present(),'setup')

#         self.add_transition(GoToBall.State.drive,
#             behavior.Behavior.State.completed,lambda:self.at_new_point() ,'complete')

#         # self.add_transition(GoToBall.State.near,
#         #     behavior.Behavior.State.completed,lambda:self.is_kub_near_ball(),'complete')

#         # self.add_transition(behavior.Behavior.State.completed,
#         #     behavior.Behavior.State.start,lambda:not self.at_new_point(),'complete')
#     ##
#     ## @brief      { function_description }
#     ##
#     ## @param      self  The object
#     ##
#     ## @return     { description_of_the_return_value }
#     ##
#     def move_present(self):
#         return self.move_point is not None

    
#     def is_kub_near_ball(self):
#         return self.new_point.dist(self.kub.state.ballPos) < 100
        

#     ##
#     ## @brief      { function_description }
#     ##
#     ## @return     { description_of_the_return_value }
#     ##
#     def at_new_point(self):
#         # for _ in xrange(10):
#         # print "new pnt",dist(self.move_point, self.new_point) <
#         print "new pnt",dist(self.move_point, self.new_point)<100,dist(self.move_point, self.new_point)
#         return dist(self.move_point, self.new_point) < 100

        
#     def on_enter_setup(self):
#         # for _ in xrange(10):
#         # print "entsetp"
#         pass

#     def execute_setup(self):
#         # print "exe stp"
#         self.move_point = getPointBehindTheBall(self.kub.state.ballPos,self.theta)
#         print(self.move_point.x,self.move_point.y)
#         print(self.kub.state.ballPos.x,self.kub.state.ballPos.y)
#         _Move.init(self.kub,self.theta)
        
#     def on_exit_setup(self):
#         # for _ in xrange(10):
#         # print "exit stp"
#         pass

#     def on_enter_drive(self):
#         # for _ in xrange(10):
#         # print "ent drv"
#         pass

#     def terminate(self):
#         super().terminate()
#     ##
#     ## @brief      { function_description }
#     ##
#     ## @param      self   The object
#     ## @param      kub    The kub
#     ## @param      state  The state
#     ##
#     ## @return     { description_of_the_return_value }
#     ##
#     def execute_drive(self):
#         # print("exe drive")
#         _Move.run()
#         # print(self.move_point.x,self.move_point.y)
#         # print(self.kub.state.ballPos.x,self.kub.state.ballPos.y)
#         self.new_point = self.kub.get_pos()

#     def on_exit_drive(self):
#         # for _ in xrange(10):
#         # print "ext drv"
#         pass







# # class GoToBall(behavior.Behavior):

# #     class State(Enum):
# #         setup = 1
# #         drive = 2

# #     def __init__():
# #         super(GoToBall, self).__init__():
# #         for state in GoToBall.State:
# #             self.add_state(state, behavior.Behavior.State.running)


# #         self.add_transition(behavior.Behavior.State.start, GoToBall.State.setup, lambda: True)
# #         self.add_transition(GoToBall.State.setup, GoToBall.State.drive, lambda: self.is_setup_completed())
# #         self.add_transition(GoToBall.State.drive, GoToBall.State.behind, lambda: self.at_new_point())
# #         self.add_transition(GoToBall.State.behind, GoToBall.State.GoToBall, lambda: self.is_ball_near__kub())
# #         self.add_transition(GoToBall.State.GoToBall, behavior.Behavior.State.completed, lambda: self.isDriveCompleted())
# #         self.add_transition(GoToBall.State.behind, behavior.Behavior.State.completed, lambda: self.isDriveCompleted())

# #     def is_setup_completed(self):
# #         return True

# #         pass

# #     def at_new_point(self):
# #         return self.new_point.dist(self.move_point) < 1.0

# #     def is_ball_near__kub(self):
# #         return self.new_point.dist(self.state.ballPos) < 1.0
# #         pass


# #     def terminate(self):
# #         super().terminate()

# #     def on_enter_setup(self):
# #         self.move_point = getPointBehindTheBall(self.state.ballPos)

# #     def execute_setup(self):
# #         _Move.init(self.kub,self.move_point)
# #         pass

# #     def on_exit_setup(self):
# #         pass

# #     def on_enter_behind(self):
# #         pass

# #     def execute_behind(self):
# #         pass

# #     def on_exit_behind(self):
# #         pass



# #     def on_enter_drive(self):
# #         pass

# #     def execute_drive(self):
# #         _Move.run()
# #         self.new_point = self.kub.get_pos()
# #         pass

# #     def on_exit_drive(self):
# #         pass

