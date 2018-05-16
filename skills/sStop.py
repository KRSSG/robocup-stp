import skill_node

def execute(param, state, bot_id, gv, pub):
	skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, 0, 0, False)
