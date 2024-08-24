import math
class Boid():
    def __init__(self, x: float, y: float, vx: float, vy: float) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        #angle between velocity and x axis
        self.angle = math.atan2(vy, vx)
        self.target_angle = self.angle

    def update_angle(self, angle_step=0.05):
        #add pi to make sure the angle_diff is between -pi and pi 
        #then mod to stay within bteween 0 and 2pi then take out the pi we added eariler
        #https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
        angle_diff = (self.target_angle - self.angle + math.pi) % (2 * math.pi) - math.pi
        if abs(angle_diff) < angle_step:
            self.angle = self.target_angle
        else:
            self.angle += angle_step * (1 if angle_diff > 0 else -1)