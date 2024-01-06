oldBearing = 359
side = 'W'

match side:
	case 'N': #value entered must be 0 < x < 360
		if oldBearing <= 90:
			new = 360 - oldBearing
		else:
			new = 180 - oldBearing
		#correct
	case 'E': #value entered must be 0 < x < 180
		if oldBearing <= 90:
			new = 180 - oldBearing
		else:
			new = 180 - oldBearing
		#correct
	case 'S': #value entered must be 90 < x < 360
		if oldBearing <= 180:
			new = 360 - oldBearing
		else:
			new = 360 - oldBearing
		#correct
	case 'W': #value entered must be 180 < x < 360
		if oldBearing <= 270:
			new = 540 - oldBearing
		else:
			new = 540 - oldBearing
		#correct
			
print(f"old: {oldBearing}, new: {new}")