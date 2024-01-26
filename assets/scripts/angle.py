import math as m

# find angle so that ball can move in corresponding direction


def calcAngle(start, end):  # start and end are doubles: (x, y)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    # angle between ball and mouse from ball in radians
    mouse_angle_rad = m.atan2(dy, dx)
    mouse_angle_deg = m.degrees(mouse_angle_rad)

    # conversion to 360 deg and adjust for psi0()
    angle_deg_test = 360 - (((mouse_angle_deg + 360) % 360) + 90)
    # convert back to radians for psi0()
    angle_rad_test = m.radians(angle_deg_test)

    angle = (angle_rad_test, angle_deg_test)
    return angle
