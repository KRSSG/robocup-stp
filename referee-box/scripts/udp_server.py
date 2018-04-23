import referee_pb2
import socket
import time
import sys
import random
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except:
    print 'Failed to create socket'
    sys.exit()

host = 'localhost'
port = 10003

while True:
    # Set the protobuf message
    time.sleep(1)
    message = referee_pb2.SSL_Referee()
    message.packet_timestamp = int(time.time())
    message.stage = referee_pb2.SSL_Referee.NORMAL_FIRST_HALF_PRE
    message.stage_time_left = random.randint(0, 10)
    message.command = referee_pb2.SSL_Referee.HALT
    message.command_counter = random.randint(0, 10)
    message.command_timestamp = int(time.time())
    # Blue Team
    message.blue.name = "kgpkubs"
    message.blue.score = 1
    message.blue.red_cards = 0
    message.blue.yellow_cards = 0
    message.blue.yellow_card_times.extend([10, 10])
    message.blue.timeouts = 0
    message.blue.timeout_time = random.randint(0, 10)
    message.blue.goalie = 0
    # Yellow Team
    message.yellow.name = "kgpkubs"
    message.yellow.score = 1
    message.yellow.red_cards = 0
    message.yellow.yellow_cards = 0
    message.yellow.yellow_card_times.extend([10, 10])
    message.yellow.timeouts = 0
    message.yellow.timeout_time = random.randint(0, 10)
    message.yellow.goalie = 0

    if random.randint(0, 2):
      message.designated_position.x = float(random.randint(-1000, 1000))
      message.designated_position.y = float(random.randint(-1000, 1000))

    try:
        sock.sendto(message.SerializeToString(), (host, port))
        print 'Sent message at UNIX TIME: {}'.format(int(time.time()))
    except socket.error:
        print "Error -- Couldn't write the message"
        sys.exit()
