from math import radians, cos, sin, acos, radians

#this will get the distance in kilometres between two locations, specified as latitude, longitude
def distance(p1, p2):
    lat1, long1 = radians(p1[0]), radians(p1[1]) #location1
    lat2, long2 = radians(p2[0]), radians(p2[1]) #location2

    #convert them into appropriate spherical coordinates
    p1 = cos(lat1), 0, sin(lat1)
    p2 = cos(lat2)*cos(long2-long1), cos(lat2)*sin(long2-long1), sin(lat2)

    #find the dot product of these coordinates
    dp = sum(c1*c2 for c1,c2 in zip(p1, p2))

    return 6373 * acos(dp) #scale the distance by earth's radius