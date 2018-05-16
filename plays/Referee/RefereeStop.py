from plays.Referee.RefPlay import RefPlay
from utils import tactics_union

class RefereeStop(RefPlay):
	def __init__(self, state, publisher):
		super(RefereeStop, self).__init__( state,publisher)

	def tactic_instance(self):
		tactic = {0:"TPosition", 1:"TPosition", 2:"TPosition", 3:"TPosition", \
				  4:"TPosition", 5:"TPosition"}

		positions = [[-1000, 0, 0, 0], [-1000, -1000, 0, 0], [-1000, 1000, 0, 0],
					 [3000, 000, 0, 0], [3000, 2000, 0, 0], [3000, -2000, 0, 0]]
		parameters = dict()
		for i in range(6):
		  params = tactics_union.Param()
		  params.PositionP.x = positions[i][0]
		  params.PositionP.y = positions[i][1]
		  params.PositionP.finalSlope = positions[i][2]
		  params.PositionP.finalVelocity = positions[i][3]
		  parameters[i] = params
		RefPlay.tactic_instance(self, tactic, parameters)

	def execute(self,gv):
		self.tactic_instance()
		RefPlay.execute(self,gv)