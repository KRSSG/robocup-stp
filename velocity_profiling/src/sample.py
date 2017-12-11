import profiler

vel = Velocity(path,t0,kubPos)
expectedTime = getTime(pathLength){"IF output is REPLAN, replan"}
angle = eachPoint()

1>ShouldReplan()
2>if t>expectedTime
	"Out of Time, Replan"
3>trapezoid(t)
4>positioIndex()
	if positionindex == -1
		"Completed Path"
	vx,vy = getVelocity()
5>errorx,errory === path[positionindex] - curPos
6>highDev --> Replan
7>vx,vy = PID(vx,vy)
8>Publish