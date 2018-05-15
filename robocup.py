import sys, os
import rospy
from krssg_ssl_msgs.msg import BeliefState
from krssg_ssl_msgs.msg import Referee
from krssg_ssl_msgs.msg import gr_Commands
from plays.pSelect import pSelect
from velocity.getVel import GetVelocity

bs_msg = BeliefState()

def referee_callback(msg):
    global bs_msg
    print msg.command
    bs_msg.ref_time_stamp = msg.packet_timestamp
    bs_msg.ref_stage = msg.stage
    bs_msg.ref_stage_time_left = msg.stage_time_left
    bs_msg.ref_command = msg.command
    bs_msg.ref_command_counter = msg.command_counter
    bs_msg.ref_command_timestamp = msg.command_timestamp
    if bs_msg.isteamyellow:
        bs_msg.opp_name = msg.blue.name
        bs_msg.opp_score = msg.blue.score
        bs_msg.opp_redcards = msg.blue.red_cards
        bs_msg.opp_yellow_card_times = msg.blue.yellow_card_times
        bs_msg.opp_yellow_cards = msg.blue.yellow_cards
        bs_msg.opp_timeouts = msg.blue.timeouts
        bs_msg.opp_goalie = msg.blue.goalie

        bs_msg.our_name = msg.blue.name
        bs_msg.our_score = msg.blue.score
        bs_msg.our_redcards = msg.blue.red_cards
        bs_msg.our_yellow_card_times = msg.blue.yellow_card_times
        bs_msg.our_yellow_cards = msg.blue.yellow_cards
        bs_msg.our_timeouts = msg.blue.timeouts
        bs_msg.our_goalie = msg.blue.goalie

    else:
        bs_msg.our_name = msg.blue.name
        bs_msg.our_score = msg.blue.score
        bs_msg.our_redcards = msg.blue.red_cards
        bs_msg.our_yellow_card_times = msg.blue.yellow_card_times
        bs_msg.our_yellow_cards = msg.blue.yellow_cards
        bs_msg.our_timeouts = msg.blue.timeouts
        bs_msg.our_goalie = msg.blue.goalie

        bs_msg.opp_name = msg.blue.name
        bs_msg.opp_score = msg.blue.score
        bs_msg.opp_redcards = msg.blue.red_cards
        bs_msg.opp_yellow_card_times = msg.blue.yellow_card_times
        bs_msg.opp_yellow_cards = msg.blue.yellow_cards
        bs_msg.opp_timeouts = msg.blue.timeouts
        bs_msg.opp_goalie = msg.blue.goalie
    
    bs_msg.blueTeamOnPositiveHalf = msg.blueTeamOnPositiveHalf

def bs_callback(msg):
    # print "BS Callback"
    global  bs_msg  
    bs_msg.isteamyellow = msg.isteamyellow
    bs_msg.frame_number = msg.frame_number
    bs_msg.camera_id = msg.camera_id
    bs_msg.t_capture = msg.t_capture
    bs_msg.t_sent = msg.t_sent
    bs_msg.ballPos = msg.ballPos
    bs_msg.ballVel = msg.ballVel
    bs_msg.awayPos = msg.awayPos
    bs_msg.homePos = msg.homePos
    bs_msg.awayVel = msg.awayVel
    bs_msg.homeVel = msg.homeVel
    bs_msg.ballDetected = msg.ballDetected
    bs_msg.homeDetected = msg.homeDetected
    bs_msg.awayDetected = msg.awayDetected
    bs_msg.our_bot_closest_to_ball = msg.our_bot_closest_to_ball
    bs_msg.opp_bot_closest_to_ball = msg.opp_bot_closest_to_ball
    bs_msg.opp_bot_marking_our_attacker = msg.opp_bot_marking_our_attacker
    bs_msg.ball_at_corners = msg.ball_at_corners
    bs_msg.ball_in_our_half = msg.ball_in_our_half
    bs_msg.ball_in_our_possession = msg.ball_in_our_possession
    bs_msg.ball_in_our_dbox = msg.ball_in_our_dbox

    playSelector = pSelect()
    play = playSelector.selectPlay(bs_msg)
    if play is not None:
        play.publisher = pub
        play.execute(gv)
        # pass

gv = []


def main():
    global pub, gv
    print "Initializing the node "
    # rospy.init_node('play_py_node',anonymous=False)
    start_time = rospy.Time.now()
    start_time = 1.0*start_time.secs + 1.0*start_time.nsecs/pow(10,9)

    for i in xrange(6):
        os.environ['bot'+str(i)]=str(start_time)
        os.environ['fc'+str(i)]='1'
    for i in xrange(6):
        print os.environ.get('bot'+str(i))

    for i in xrange(6):
        start_time = float(os.environ.get('bot'+str(i)))
        gv.append(GetVelocity(start_time = start_time,kubs_id = i))

    pub = rospy.Publisher('/grsim_data', gr_Commands, queue_size=1000)
    rospy.Subscriber("/ref_data", Referee, referee_callback, queue_size=1000)
    rospy.Subscriber('/belief_state', BeliefState, bs_callback, queue_size=1000)
    rospy.spin()

if __name__=='__main__':
    rospy.init_node('play_py_node',anonymous=False)
    main()