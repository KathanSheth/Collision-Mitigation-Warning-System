import math
import csv
from math import radians, cos, sin, asin, sqrt,atan2,degrees,pi
import numpy as np

def collide(p1, p2):
    '''
    Return True and the MPV if the shapes collide. Otherwise, return False and
    None.

    p1 and p2 are lists of ordered pairs, the vertices of the polygons in the
    counterclockwise direction.
    '''
    edges = []
    orthog = []

    p1 = [np.array(v, 'float64') for v in p1]
    p2 = [np.array(v, 'float64') for v in p2]
    
    p1_length = len(p1)
    p2_length = len(p2)

    # Find edge vector for both polygons

    for i in range(p1_length):
        p1_edge = p1[(i + 1)%p1_length] - p1[i]
        edges.append(p1_edge)

    for i in range(p2_length):
        p2_edge = p2[(i + 1)%p2_length] - p2[i]
        edges.append(p2_edge)


    # Find Orthogonals for each of the vector.
    for i in edges:
        orthog.append(np.array([-i[1], i[0]]))

    for i in orthog:
        separates = is_separating_axis(i, p1, p2)
        
        if separates:
           # they do not collide
            return False
        
    return True


def is_separating_axis(i, p1, p2):
    """
    Return True if o is a separating axis of p1 and p2.
    Otherwise, return False
    """
    min1, max1 = float('+inf'), float('-inf')
    min2, max2 = float('+inf'), float('-inf')

    for v in p1:
        projection = np.dot(v, i)

        min1 = min(min1, projection)
        max1 = max(max1, projection)

    for v in p2:
        projection = np.dot(v, i)

        min2 = min(min2, projection)
        max2 = max(max2, projection)

    if max1 >= min2 and max2 >= min1:
        return False
    else:
        return True

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def angleFromCoordinate(lon1,lat1,lon2,lat2):

    dLon = lon2 - lon1
    #print dLon
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon)

    brng = atan2(y, x)

    brng = degrees(brng)
    brng = (brng + 360) % 360
    #brng = 360 - brng
    return brng;


def XfromGPS(lat1_deg,long1_deg,lat2_deg,long2_deg):
    R=6.371*math.pow(10,6)          #earth radius
    lat1_ =lat1_deg*math.pi/180     #convert degrees into radians
    lat2_ =lat2_deg*math.pi/180
    long1_ =long1_deg*math.pi/180
    long2_ =long2_deg*math.pi/180
    x = np.array(R*(long2_-long1_)*np.cos(lat1_))
    return x

def YfromGPS(lat1_deg,long1_deg,lat2_deg,long2_deg):
    R=6.371*math.pow(10,6)           #earth radius
    lat1_ =lat1_deg*math.pi/180      #convert degrees into radians
    lat2_ =lat2_deg*math.pi/180
    long1_ =long1_deg*math.pi/180
    long2_ =long2_deg*math.pi/180
    y = np.array(R*(lat2_-lat1_))
    return y

def new_bearing(lat1,lon1,lat2,lon2):
    R = 6371 * 10^3
    lat1_ = lat1 * math.pi /180
    lat2_ = lat2 * math.pi /180

    lon1_=lon1*math.pi/180
    lon2_=lon2*math.pi/180


    y2 = R*(lat2_-lat1_)
    x2 = R*(lon2_-lon1_)*cos(lat1_)
    #b2 = atan2(x2,y2)*180/math.pi+180
    b2 = atan2(x2,y2)*180/math.pi
    b2 = (b2 + 360) % 360
    #print b2
    #print y2
    #print x2
    return b2

def rec(lat1,lon1,heading,distance):
    #print heading
    #Idea is to find two points CW and ACW 90 degree to the point at 2m distance
    #First find theta1 and theta2 and then with distance 2m calculate two points of rectangle

    d = 0.002
    R = 6371
    theta1 = heading - 90
    theta2 = heading + 90
    if theta1 < 0:
        theta1 = theta1 + 360

    if theta2 > 360:
        theta2 = theta2 - 360
    #print theta1
    #print theta2

    theta1_R = math.radians(theta1)
    theta2_R = math.radians(theta2)

    lat1_R = math.radians(lat1)
    lon1_R = math.radians(lon1)

    lat2_p1 = asin(sin(lat1_R) * cos(d/R) + cos(lat1_R) * sin(d/R) * cos(theta1_R))
    lon2_p1 = lon1_R + atan2(sin(theta1_R) * sin(d/R) * cos(lat1_R),cos(d/R) - sin(lat1_R) * sin(lat2_p1))

    lat2_p1 = math.degrees(lat2_p1)
    lon2_p1 = math.degrees(lon2_p1)

    lat2_p1_R = math.radians(lat2_p1)
    lon2_p1_R = math.radians(lon2_p1)


    lat2_p2 = asin(sin(lat1_R) * cos(d/R) + cos(lat1_R) * sin(d/R) * cos(theta2_R))
    lon2_p2 = lon1_R + atan2(sin(theta2_R) * sin(d/R) * cos(lat1_R),cos(d/R) - sin(lat1_R) * sin(lat2_p2))

    lat2_p2 = math.degrees(lat2_p2)
    lon2_p2 = math.degrees(lon2_p2)

    lat2_p2_R = math.radians(lat2_p2)
    lon2_p2_R = math.radians(lon2_p2)


    #print "################"
    #print lat2_p1,lon2_p1
#    print lon2_p1
    #print "################"
    #print lat2_p2,lon2_p2
#    print lon2_p2
    #print "################"

    #Now we have to find other two points of rectangle
    #For that we need length of rectangle which is velocity * TTC. TTC is given as 8s
    #Here each pair of points are given in the timespan of 1 second
    #So velocity will be equal to distance
    #And distance will be velocity * 8. Here it is l1

    velocity_v1 = distance * 1

    l1 = velocity_v1 * 8
    #print l1


    heading_ = math.radians(heading)
    lat2_p3 = asin(sin(lat2_p2_R) * cos(l1/R) + cos(lat2_p2_R) * sin(l1/R) * cos(heading_))
    lon2_p3 = lon2_p2_R + atan2(sin(heading_) * sin(l1/R) * cos(lat2_p2_R),cos(l1/R) - sin(lat2_p2_R) * sin(lat2_p3))

    lat2_p3 = math.degrees(lat2_p3)
    lon2_p3 = math.degrees(lon2_p3)

    lat2_p3_R = math.radians(lat2_p3)
    lon2_p3_R = math.radians(lon2_p3)

    lat2_p4 = asin(sin(lat2_p1_R) * cos(l1/R) + cos(lat2_p1_R) * sin(l1/R) * cos(heading_))
    lon2_p4 = lon2_p1_R + atan2(sin(heading_) * sin(l1/R) * cos(lat2_p1_R),cos(l1/R) - sin(lat2_p1_R) * sin(lat2_p4))

    lat2_p4 = math.degrees(lat2_p4)
    lon2_p4 = math.degrees(lon2_p4)

    lat2_p4_R = math.radians(lat2_p4)
    lon2_p4_R = math.radians(lon2_p4)




    #print "################"
    #print lat2_p3,lon2_p3
#    print lon2_p3
    #print "################"
    #print "################"
    #print lat2_p4,lon2_p4
#    print lon2_p4
    #print "################"

    x = np.array([lat2_p1,lat2_p2,lat2_p3,lat2_p4])
    y = np.array([lon2_p1,lon2_p2,lon2_p3,lon2_p4])
    return x,y
    

x_cords = []
y_cords = []




# with open('input_v1.csv') as csvDataFile,open('input_v2.csv','rU') as csvDataFile_v2:
#     count = 0
    
#     csvReader = csv.reader(csvDataFile,delimiter=',', quotechar='"')
#     #header1 = csvReader.next()
#     csvReader_v2 = csv.reader(csvDataFile_v2,delimiter=',', quotechar='"')

#     #print header1
#     #print "-------------------------"
#     previous = 0.0
#     #previous_row = csvReader.next()
#     previous_row = next(csvReader,None)
#     #print "Sanjay"
#     #print previous_row
#     previous_row_v2 = next(csvReader_v2,None)
#     #print previous_row_v2
    
#     #previous_row_v2 = previous_row.next()
#     #print next(next(csvReader,None))

#     x_origin = previous_row[3]
#     y_origin = previous_row[2]
    
#     #for row_v1 in enumerate(csvReader,start=1):
#     for row_v1,row_v2 in zip(csvReader,csvReader_v2):
#         try:
            
#             #previous_row = row
#             #print previous_row[2],previous_row[3]
#             #print "Renu"
#             #print row_v1[2],row_v1[3]
                
#                 #distance = haversine(lon_1,lat_1,lon_2,lat_2)
#                 #bearing2 = new_bearing(lat_1,lon_1,lat_2,lon_2)
#             distance_v1 = haversine(float(row_v1[2]),float(row_v1[3]),float(previous_row[2]),float(previous_row[3]))
#             bearing_v1 = new_bearing(float(previous_row[3]),float(previous_row[2]),float(row_v1[3]),float(row_v1[2]))
#             #print "Printing for Vehicle 1"
#             #print distance_v1
#             #print bearing_v1

#                 #rec(float(previous_row[3]),float(previous_row[2]),float(bearing_v1),float(distance_v1))
#             x_cords_v1,y_cords_v1 = rec(float(row_v1[3]),float(row_v1[2]),float(bearing_v1),float(distance_v1))    
#             previous_row[3] = row_v1[3]
#             previous_row[2] = row_v1[2]

#             #print "new" + previous_row[2],previous_row[3]

#                 #x = XfromGPS(float(previous_row[3]),float(previous_row[2]),float(row[3]),float(row[2]))
#                 #y = YfromGPS(float(previous_row[3]),float(previous_row[2]),float(row[3]),float(row[2]))

#                 #x = []
#                 #y = []
#             x1_v1 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[0]),float(y_cords_v1[0]))
#             y1_v1 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[0]),float(y_cords_v1[0]))
#             x2_v1 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[1]),float(y_cords_v1[1]))
#             y2_v1 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[1]),float(y_cords_v1[1]))
#             x3_v1 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[2]),float(y_cords_v1[2]))
#             y3_v1 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[2]),float(y_cords_v1[2]))
#             x4_v1 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[3]),float(y_cords_v1[3]))
#             y4_v1 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[3]),float(y_cords_v1[3]))
               
#             #print "Cartesian Points are: "
#             #print x1_v1,y1_v1,x2_v1,y2_v1,x3_v1,y3_v1,x4_v1,y4_v1
#             x_v1 = np.array([x1_v1,x2_v1,x3_v1,x4_v1])
#             y_v1 = np.array([y1_v1,y2_v1,y3_v1,y4_v1])
#             #print x_v1,y_v1
#             #print x_cords_v1,y_cords_v1

#             #print "CALCULATION FOR VEHICLE 2 BEGINS___________________________________"
#             #print row_v2[2],row_v2[3]
#             distance_v2 = haversine(float(row_v2[2]),float(row_v2[3]),float(previous_row_v2[2]),float(previous_row_v2[3]))
#             bearing_v2 = new_bearing(float(previous_row_v2[3]),float(previous_row_v2[2]),float(row_v2[3]),float(row_v2[2]))
#             #print "Printing for Vehicle 2"
#             #print distance_v2
#             #print bearing_v2

#             #rec(float(previous_row[3]),float(previous_row[2]),float(bearing_v1),float(distance_v1))
#             x_cords_v2,y_cords_v2 = rec(float(row_v2[3]),float(row_v2[2]),float(bearing_v2),float(distance_v2))    
#             previous_row_v2[3] = row_v2[3]
#             previous_row_v2[2] = row_v2[2]


#             #print "new" + previous_row_v2[2],previous_row_v2[3] 
#             x1_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[0]),float(y_cords_v2[0]))
#             y1_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[0]),float(y_cords_v2[0]))
#             x2_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[1]),float(y_cords_v2[1]))
#             y2_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[1]),float(y_cords_v2[1]))
#             x3_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[2]),float(y_cords_v2[2]))
#             y3_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[2]),float(y_cords_v2[2]))
#             x4_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[3]),float(y_cords_v2[3]))
#             y4_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[3]),float(y_cords_v2[3]))
               
#             #print "Cartesian Points for vehicle 2 are: "
#             #print x1_v2,y1_v2,x2_v2,y2_v2,x3_v2,y3_v2,x4_v2,y4_v2
#             x_v2 = np.array([x1_v2,x2_v2,x3_v2,x4_v2])
#             y_v2 = np.array([y1_v2,y2_v2,y3_v2,y4_v2])
#             #print x_v2,y_v2
#             #print x_cords_v2,y_cords_v2

#             vehicle_1 = np.array([(x1_v1,y1_v1),(x2_v1,y2_v1),(x3_v1,y3_v1),(x4_v1,y4_v1)])
#             vehicle_2 = np.array([(x1_v2,y1_v2),(x2_v2,y2_v2),(x3_v2,y3_v2),(x4_v2,y4_v2)])

#             col = collide(vehicle_1,vehicle_2)

#             #print col


#             #break

#         except IndexError:
#             pass    

# #    previous_row_v2[3] = 42.50202848
# #    previous_row_v2[2] = -83.18495249

# #    count = 4
#     #for count,row in enumerate(csvReader_v2,start=1):
    
#     # for row_v2 in csvReader_v2:    
#     #     try:    
            
#     #         print row_v2[2],row_v2[3]
#     #         distance_v2 = haversine(float(row_v2[2]),float(row_v2[3]),float(previous_row_v2[2]),float(previous_row_v2[3]))
#     #         bearing_v2 = new_bearing(float(previous_row_v2[3]),float(previous_row_v2[2]),float(row_v2[3]),float(row_v2[2]))
#     #         print "Printing for Vehicle 2"
#     #         print distance_v2
#     #         print bearing_v2

#     #         #rec(float(previous_row[3]),float(previous_row[2]),float(bearing_v1),float(distance_v1))
#     #         x_cords_v2,y_cords_v2 = rec(float(row_v2[3]),float(row_v2[2]),float(bearing_v2),float(distance_v2))    
#     #         previous_row_v2[3] = row_v2[3]
#     #         previous_row_v2[2] = row_v2[2]


#     #         print "new" + previous_row_v2[2],previous_row_v2[3] 
#     #         x1_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[0]),float(y_cords_v2[0]))
#     #         y1_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[0]),float(y_cords_v2[0]))
#     #         x2_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[1]),float(y_cords_v2[1]))
#     #         y2_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[1]),float(y_cords_v2[1]))
#     #         x3_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[2]),float(y_cords_v2[2]))
#     #         y3_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[2]),float(y_cords_v2[2]))
#     #         x4_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[3]),float(y_cords_v2[3]))
#     #         y4_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[3]),float(y_cords_v2[3]))
               
#     #         print "Cartesian Points for vehicle 2 are: "
#     #         print x1_v2,y1_v2,x2_v2,y2_v2,x3_v2,y3_v2,x4_v2,y4_v2
#     #         x_v2 = np.array([x1_v2,x2_v2,x3_v2,x4_v2])
#     #         y_v2 = np.array([y1_v2,y2_v2,y3_v2,y4_v2])
#     #         print x_v2,y_v2
#     #         print x_cords_v2,y_cords_v2  
    
                
#     #             #print row[2],row[3]
#     #         break

#     #     except IndexError:
#     #         pass    

#     