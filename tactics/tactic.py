# Super class for all the tactics

import sys
import time
import os
sys.path.append('plays_py/scripts')

from abc import ABCMeta, abstractmethod

class Tactic(object):
	# this default time is in milliseconds
	__metaclass__ = ABCMeta

	DEFAULT_TIMEOUT_PERIOD = 50
	def __init__(self, bot_id, state, param=None):
		self.param = param
		self.state = state
		self.bot_id     = bot_id
		self.time_out   = Tactic.DEFAULT_TIMEOUT_PERIOD
		self.begin_time = time.time()

	@abstractmethod
	def execute(self,state):
		pass

	@abstractmethod
	def isComplete(self,state):
		pass

	@abstractmethod
	def updateParams(self,state):
		pass
