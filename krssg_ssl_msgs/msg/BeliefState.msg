# beliefstate message

bool               isteamyellow
uint32             frame_number
float64            t_capture
float64            t_sent
geometry_msgs/Pose2D  ballPos
geometry_msgs/Point32 ballVel
geometry_msgs/Pose2D[] awayPos
geometry_msgs/Pose2D[] homePos
geometry_msgs/Pose2D[] awayVel
geometry_msgs/Pose2D[] homeVel
bool ballDetected
bool[] homeDetected
bool[] awayDetected
uint8   our_bot_closest_to_ball
uint8   opp_bot_closest_to_ball
uint8   our_goalie			#returns 10 for no goalie
uint8   opp_goalie			#returns 10 for no goalie
uint8   opp_bot_marking_our_attacker
bool    ball_at_corners
bool    ball_in_our_half
bool    ball_in_our_possession
bool    ball_in_our_dbox

# Referee messages -- Recieved from RefBox
uint32 home_team_size
uint32 away_team_size
uint8   ref_play_id
# == 0    -> Normal play is in execution
# == else -> Play id of the referee play in execution

uint64 ref_time_stamp
uint8 ref_stage
int32 ref_stage_time_left
uint8 ref_command

# Score of blue team
uint8 blue_score
uint8 yellow_score

# botID of goalie
uint32 blue_goalie
uint32 yellow_goalie

# No. of bots which got red cards
uint32 blue_redcards
uint32 yellow_redcards

# Point specified by referee for ball placement
point_2d ref_ball_point

string blue_name
string yellow_name

# Total no. of yellow cards issued from the beginning
uint32 blue_yellow_cards
uint32 yellow_yellow_cards

# Time (microseconds) left for bots which recieved yellow card sorted from
# smallest to largest. This array is empty if no yellow card is recieved.
uint32[] blue_yellow_card_times
uint32[] yellow_yellow_card_times

# Number of timeouts left, if currently in a timeout, it's excluded
uint32 blue_timeouts
uint32 yellow_timeouts

# Number of micro seconds of time the team can use for timeout
uint32 blue_timeout_time
uint32 yelow_timeout_time
