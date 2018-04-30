import skill_node
import math
def execute(param,state,bot_id, pub):
	print("Testing Motion")
	speed = param.speed
	motionAngle = param.motionAngle
	omega = param.omega
	theta  =  state.homePos[bot_id].theta - motionAngle
	print("Velocity Tangent", speed * math.cos(theta))	
	print("Velocity Normal", -speed * math.sin(theta))	
	skill_node.send_command(pub, state.isteamyellow, bot_id, -speed * math.sin(theta), -speed * math.cos(theta), omega, 0, False)