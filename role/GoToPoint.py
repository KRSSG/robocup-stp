from enum import Enum
import behavior
import _GoToPoint
from utils.math_functions import *
class GoToPoint(behavior.Behavior):
	"""docstring for GoToPoint"""
	##
	## @brief      Class for state.
	##
	class State(Enum):
		setup = 1 
		drive = 2

	##
	## @brief      Constructs the object.
	##
	## @param      self   The object
	## @param      point  The point
	##
	def __init__(self,kub,point,theta,continuous=False):
		# print "gtp"
		#GoToPoint.behavior.Behavior()
		#g = behavior.Behavior()
		#print "gtp2"
		super(GoToPoint,self).__init__()
		self.kub = kub
		#self.state = state

		self.target_point = point
		self.theta = theta

		self.add_state(GoToPoint.State.setup,
			behavior.Behavior.State.running)
		self.add_state(GoToPoint.State.drive,
			behavior.Behavior.State.running)
		

		self.add_transition(behavior.Behavior.State.start,
			GoToPoint.State.setup,lambda: True,'immediately')

		self.add_transition(GoToPoint.State.setup,
			GoToPoint.State.drive,lambda: self.target_present,'setup')

		self.add_transition(GoToPoint.State.drive,
			GoToPoint.State.drive,lambda: not self.at_new_point(),'restart')

		self.add_transition(GoToPoint.State.drive,
			behavior.Behavior.State.completed,lambda:self.at_new_point(),'complete')

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
	def at_new_point(self):
		#print (dist(self.target_point,self.new_point),210)
		return dist(self.target_point,self.new_point) < 210.0

		
	def on_enter_setup(self):
		pass
	def execute_setup(self):
		_GoToPoint.init(self.kub,self.target_point,self.theta)
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
		t = _GoToPoint.run()
		self.new_point = self.kub.get_pos()
		

	
	def on_exit_drive(self):
		pass




