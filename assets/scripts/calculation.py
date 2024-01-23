import math

#find angle so that ball can move in corresponding direction
def calcAngle(start, end):
    dx = end[0] - start[0] 
    dy = end[1] - start[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)

    angle = [angle_rad, angle_deg]

    return angle