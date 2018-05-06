from utils.config import MAX_BOT_OMEGA,MIN_BOT_OMEGA

def Get_Omega(kub_id, totalAngle, homePos):
    if totalAngle < 0.001:
        return 0.0
    MAX_w = (MAX_BOT_OMEGA+MIN_BOT_OMEGA)/4.0
    theta_lft = float(totalAngle - homePos[kub_id].theta)
    vw = (theta_lft/totalAngle)*MAX_w
    if abs(vw)<3*MIN_BOT_OMEGA:
        vw = MIN_BOT_OMEGA*(1 if vw>0 else -1)
    return vw


    