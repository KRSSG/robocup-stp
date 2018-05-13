# beliefstate message

bool               isteamyellow
uint32             frame_number
uint8			   camera_id
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
uint32 ref_command_counter
uint64 ref_command_timestamp




string our_name
uint8 our_score
uint32 our_redcards
uint32[] our_yellow_card_times
uint32 our_yellow_cards
uint32 our_timeouts
uint32 our_timeout_time
uint8   our_goalie			#returns 10 for no goalie

string opp_name
uint8 opp_score
uint32 opp_redcards
uint32[] opp_yellow_card_times
uint32 opp_yellow_cards
uint32 opp_timeouts
uint32 opp_timeout_time
uint8   opp_goalie			#returns 10 for no goalie


# Point specified by referee for ball placement
point_2d ref_ball_point
bool blueTeamOnPositiveHalf
