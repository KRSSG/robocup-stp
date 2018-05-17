from plays.Referee.RefereeStop import RefereeStop
from plays.Referee.RefereeHalt import RefereeHalt


class pSelect:
	def selectPlay(self, data, pub):
		if data.ref_command == 0:
			# HALT Command from Referee
			return RefereeHalt(data, pub)
		if data.ref_command == 1:
			# STOP Command from Referee
			return RefereeStop(data, pub)


		# TO DO To write select play and return it instead of none 
		return None
