#! /usr/bin/env python

import rospy
from std_msgs.msg import String
import socket
import referee_pb2
import time
import datetime

# import custom data message files
from krssg_ssl_msgs.msg import debug_msg
from krssg_ssl_msgs.msg import team_info
from krssg_ssl_msgs.msg import point_2d


def udp_parser(referee_msg):

	ros_msg     = debug_msg()
	blue_team   = team_info()
	yellow_team = team_info()
	ball_point  = point_2d()

	# blue team's details
	blue_team.name  = referee_msg.blue.name
	blue_team.score = referee_msg.blue.score
	blue_team.red_cards = referee_msg.blue.red_cards
	blue_team.yellow_cards = referee_msg.blue.yellow_cards
	blue_team.yellow_card_times = referee_msg.blue.yellow_card_times
	blue_team.goalie = referee_msg.blue.goalie
	blue_team.timeouts = referee_msg.blue.timeouts
	blue_team.timeout_time = referee_msg.blue.timeout_time

	# yellow team's details
	yellow_team.name  = referee_msg.yellow.name
	yellow_team.score = referee_msg.yellow.score
	yellow_team.red_cards = referee_msg.yellow.red_cards
	yellow_team.yellow_cards = referee_msg.yellow.yellow_cards
	yellow_team.yellow_card_times =referee_msg.yellow.yellow_card_times
	yellow_team.goalie = referee_msg.yellow.goalie
	yellow_team.timeouts = referee_msg.yellow.timeouts
	yellow_team.timeout_time = referee_msg.yellow.timeout_time

	# ball's position details
	if referee_msg.HasField('designated_position'):
	  ball_point.x = referee_msg.designated_position.x
	  ball_point.y = referee_msg.designated_position.y
	else:
	  ball_point.x = -10000
	  ball_point.y = -10000

	# Decode all the remaining messages
	ros_msg.ts              = referee_msg.packet_timestamp
	ros_msg.stage           = int(referee_msg.stage)
	ros_msg.stage_time_left = referee_msg.stage_time_left
	ros_msg.command         = int(referee_msg.command)
	ros_msg.blue            = blue_team
	ros_msg.yellow          = yellow_team
	ros_msg.b_point         = ball_point

	# Return the packet
	return ros_msg

def PRINT_ROS(ros_msg):
	msg = ''
	msg += '-'*50
	msg += '\nTime Stamp: {}\n'.format(ros_msg.ts)
	msg += 'Stage: {}\n'.format(ros_msg.stage)
	msg += 'Stage Time Left: {}\n'.format(ros_msg.stage_time_left)
	msg += 'Command: {}\n'.format(ros_msg.command)
	if int(ros_msg.b_point.x) != -10000:
	  msg += 'Designated ball Position: [{}, {}]\n'.format(ros_msg.b_point.x, ros_msg.b_point.y)
	else:
	  msg += 'No Designated ball Position\n'
	msg += '----Blue Team Details----\n'
	msg += 'Name: {}\n'.format(ros_msg.blue.name)
	msg += 'Score: {}\n'.format(ros_msg.blue.score)
	msg += 'Red Cards: {}\n'.format(ros_msg.blue.red_cards)
	msg += 'Yellow Cards: {}\n'.format(ros_msg.blue.yellow_cards)
	msg += 'Yellow Cards Time Remaining: [ '
	for i in range(len(ros_msg.blue.yellow_card_times)):
	  msg += '{} '.format(ros_msg.blue.yellow_card_times[i])
	msg += ']\n'
	msg += 'Timeouts Remaining: {}\n'.format(ros_msg.blue.timeouts)
	msg += 'Timeout Time Left: {}\n'.format(ros_msg.blue.timeout_time)
	msg += 'Goalie: {}\n'.format(ros_msg.blue.goalie)
	msg += '----Yellow Team Details----\n'
	msg += 'Name: {}\n'.format(ros_msg.yellow.name)
	msg += 'Score: {}\n'.format(ros_msg.yellow.score)
	msg += 'Red Cards: {}\n'.format(ros_msg.yellow.red_cards)
	msg += 'Yellow Cards: {}\n'.format(ros_msg.yellow.yellow_cards)
	msg += 'Yellow Cards Time Remaining: [ '
	for i in range(len(ros_msg.yellow.yellow_card_times)):
	  msg += '{} '.format(ros_msg.yellow.yellow_card_times[i])
	msg += ']\n'
	msg += 'Timeouts Remaining: {}\n'.format(ros_msg.yellow.timeouts)
	msg += 'Timeout Time Left: {}\n'.format(ros_msg.yellow.timeout_time)
	msg += 'Goalie: {}\n'.format(ros_msg.yellow.goalie)
	msg += '-'*50
	msg += '\n'
	print msg

def client_data():
	# Initialise ros node and topic
	pub = rospy.Publisher('ref_data', debug_msg, queue_size=1000)
	rospy.init_node('referee', anonymous=False)

	# host = '224.5.23.1'
	host = 'localhost'
	port = 10003
	max_bits = 1024

	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print 'Socket created'
	except socket.error, msg:
		print 'Failed to create socket. Error: ', str(msg[1])

	try:
		sock.bind((host, port))
		print 'Binding done!'
	except socket.error, msg:
		print 'Bind failed. Error: ', str(msg[1])

	print 'Waiting on port: ', port

	# receive data from client
	while True:
		# Read the message from referee
		single_message = referee_pb2.SSL_Referee()
		data, addr = sock.recvfrom(max_bits)

		# Parse the udp data to protobuf message
		single_message.ParseFromString(data)

		# Convert protobuf message into ROS message type
		ros_msg = udp_parser(single_message)

		print 'Received following message from referee at: {} \
			   '.format(datetime.datetime.fromtimestamp( \
        	   int(time.time()) \
               ).strftime('%Y-%m-%d %H:%M:%S'))
		PRINT_ROS(ros_msg)
		# Publish the message
		pub.publish(ros_msg)

	sock.close()

if __name__=='__main__':
	try:
		client_data()
	except rospy.ROSInterruptException:
		pass
