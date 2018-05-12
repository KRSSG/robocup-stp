import sys
import PlaySelector
import TestSkills
import rospy
from krssg_ssl_msgs.msg import GUI_call

class GUI_link:
	def __init__(self):
		self.path = "RRT"
		self.initialPosition = "Position 1"
		self.team = "Team Yellow"
		self.goalie = "0"
		self.play = "Offensive"
		self.skillchoice = "goToBall"
		self.bot = "0"
		self.ballx=0
		self.bally=0
	def skill_triggered(self):
		print "STARTED NEW SKILL"
		TestSkills.main(int(self.bot))
	def play_triggered(self):
		print self.path, self.initialPosition, self.team, self.goalie, self.play
	def play_selector_triggered(self):
		PlaySelector.main()

# gui_class_object=GUI_link()
# 
def gui_callback(msg):
	print(msg.button)
	print(msg.params)
	if (msg.button  == "skill_test"):
		params = str(msg.params).split(' ')
		skill = params[0]
		params = params[1:]
		if skill in "goToBall":
			bot_id = int(params[0])
			TestSkills.main(int(bot_id))


def main():
	rospy.init_node('gui',anonymous=False)
	rospy.Subscriber('/gui_call', GUI_call, gui_callback, queue_size=1000)
	rospy.spin()

if __name__ == '__main__':
	print "STARTED"
	main()
