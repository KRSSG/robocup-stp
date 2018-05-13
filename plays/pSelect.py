from plays.Referee.RefereeStop import RefereeStop


class pSelect:
	def selectPlay(self,data):
		if data.ref_command == 1:
			# STOP Command from Referee
			return RefereeStop(data,None)


		# TO DO To write select play and return it instead of none 
		return None
