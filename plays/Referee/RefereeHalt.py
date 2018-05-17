from plays.Referee.RefPlay import RefPlay
from utils import tactics_union

class RefereeHalt(RefPlay):
	def __init__(self, state, publisher):
		super(RefereeHalt, self).__init__( state, publisher)

	def tactic_instance(self):
		tactic = {0:"TStop", 1:"TStop", 2:"TStop", 3:"TStop", \
				  4:"TStop", 5:"TStop"}
		parameters = dict()
		params = tactics_union.Param()
		for i in range(self.active_robots):
			parameters[i] = params

		RefPlay.tactic_instance(self, tactic, parameters)

	def execute(self,gv):
		self.tactic_instance()
		RefPlay.execute(self,gv)