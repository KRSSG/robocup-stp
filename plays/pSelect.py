from plays.Referee.RefereeStop import RefereeStop


class pSelect:
	def selectPlay(self,data):
		# print("Message {}".format(data.ref_command))
		if data.ref_command == 0:
			# STOP Command from Referee
			return RefereeStop(data,None)


		# TO DO To write select play and return it instead of none 
		return None
