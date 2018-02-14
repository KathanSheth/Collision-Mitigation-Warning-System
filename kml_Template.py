# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 23:27:55 2017

@author: MSI_me
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 22:40:48 2017

@author: MSI_me
"""

import sys
import csv
import numpy as np
#from compiling_2 import *
from car_collision import *

#print 'print the number of arguments', len(sys.argv)
#print 'arguments', str(sys.argv)


main_name,extention=str(sys.argv[1]).split('.')
#print 'main_name:',main_name
#print 'extention:',extention
out_kml_name=main_name+'.kml'
print (out_kml_name)
times_v1=[]
longitudes_v1=[]
latitudes_v1=[]
times_v2=[]
longitudes_v2=[]
latitudes_v2=[]


with  open(str(sys.argv[1]), 'rt') as csvDataFile,open(str(sys.argv[2]), 'rt') as csvDataFile_v2,open(out_kml_name, 'w') as kml_file:

    kml_file.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
<!-- 

TimeStamp is recommended for Point.

Each Point represents a sample from a GPS.

-->

   <Document>
    <name>Points with TimeStamps</name>
	<Style id="sn_cabs3">
		<IconStyle>
			<color>ff0000ff</color>
			<scale>0.7</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
			</Icon>
			<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>
	<Style id="sh_cabs3">
		<IconStyle>
			<color>ff0000ff</color>
			<scale>0.816667</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
			</Icon>
			<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>
	<StyleMap id="msn_cabs3">
		<Pair>
			<key>normal</key>
			<styleUrl>#sn_cabs3</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#sh_cabs3</styleUrl>
		</Pair>
	</StyleMap>

	<Style id="sn_cabs2">
		<IconStyle>
			<color>ffff0000</color>
			<scale>0.7</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
			</Icon>
			<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>
	<Style id="sh_cabs2">
		<IconStyle>
			<color>ffff0000</color>
			<scale>0.816667</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
			</Icon>
			<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>
	<StyleMap id="msn_cabs2">
		<Pair>
			<key>normal</key>
			<styleUrl>#sn_cabs2</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#sh_cabs2</styleUrl>
		</Pair>
	</StyleMap>

	<StyleMap id="msn_cabs1">
		<Pair>
			<key>normal</key>
			<styleUrl>#sn_cabs1</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#sh_cabs1</styleUrl>
		</Pair>
	</StyleMap>
	<Style id="sh_cabs1">
		<IconStyle>
			<color>ff00ff00</color>
			<scale>0.7</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
			</Icon>
			<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>
	<Style id="sn_cabs1">
		<IconStyle>
			<color>ff00ff00</color>
			<scale>0.7</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/shapes/cabs.png</href>
			</Icon>
			<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>
		</IconStyle>
		<ListStyle>
		</ListStyle>
	</Style>''')
    kml_file.write('\n')
    count = 0
    
    csvReader = csv.reader(csvDataFile,delimiter=',', quotechar='"')
    #header1 = csvReader.next()
    csvReader_v2 = csv.reader(csvDataFile_v2,delimiter=',', quotechar='"')

    #print header1
    #print "-------------------------"
    previous = 0.0
    #previous_row = csvReader.next()
    previous_row = next(csvReader,None)
    #print "Sanjay"
    #print previous_row
    previous_row_v2 = next(csvReader_v2,None)
    #print previous_row_v2
    
    #previous_row_v2 = previous_row.next()
    #print next(next(csvReader,None))

    x_origin = previous_row[3]
    y_origin = previous_row[2]
    
    #for row_v1 in enumerate(csvReader,start=1):
    for row_v1,row_v2 in zip(csvReader,csvReader_v2):
        try:

            times_v1.append(row_v1[1])
            longitudes_v1.append(row_v1[2])
            latitudes_v1.append(row_v1[3])
            times_v2.append(row_v2[1])
            longitudes_v2.append(row_v2[2])
            latitudes_v2.append(row_v2[3])


            
            #previous_row = row
            #print previous_row[2],previous_row[3]
            #print "Renu"
            #print row_v1[2],row_v1[3]
                
                #distance = haversine(lon_1,lat_1,lon_2,lat_2)
                #bearing2 = new_bearing(lat_1,lon_1,lat_2,lon_2)
            distance_v1 = haversine(float(row_v1[2]),float(row_v1[3]),float(previous_row[2]),float(previous_row[3]))
            bearing_v1 = new_bearing(float(previous_row[3]),float(previous_row[2]),float(row_v1[3]),float(row_v1[2]))
            #print "Printing for Vehicle 1"
            #print distance_v1
            #print bearing_v1

                #rec(float(previous_row[3]),float(previous_row[2]),float(bearing_v1),float(distance_v1))
            x_cords_v1,y_cords_v1 = rec(float(row_v1[3]),float(row_v1[2]),float(bearing_v1),float(distance_v1))    
            previous_row[3] = row_v1[3]
            previous_row[2] = row_v1[2]

            #print "new" + previous_row[2],previous_row[3]

                #x = XfromGPS(float(previous_row[3]),float(previous_row[2]),float(row[3]),float(row[2]))
                #y = YfromGPS(float(previous_row[3]),float(previous_row[2]),float(row[3]),float(row[2]))

                #x = []
                #y = []
            x1_v1 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[0]),float(y_cords_v1[0]))
            y1_v1 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[0]),float(y_cords_v1[0]))
            x2_v1 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[1]),float(y_cords_v1[1]))
            y2_v1 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[1]),float(y_cords_v1[1]))
            x3_v1 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[2]),float(y_cords_v1[2]))
            y3_v1 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[2]),float(y_cords_v1[2]))
            x4_v1 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[3]),float(y_cords_v1[3]))
            y4_v1 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v1[3]),float(y_cords_v1[3]))
               
            #print "Cartesian Points are: "
            #print x1_v1,y1_v1,x2_v1,y2_v1,x3_v1,y3_v1,x4_v1,y4_v1
            x_v1 = np.array([x1_v1,x2_v1,x3_v1,x4_v1])
            y_v1 = np.array([y1_v1,y2_v1,y3_v1,y4_v1])
            #print x_v1,y_v1
            #print x_cords_v1,y_cords_v1

            #print "CALCULATION FOR VEHICLE 2 BEGINS___________________________________"
            #print row_v2[2],row_v2[3]
            distance_v2 = haversine(float(row_v2[2]),float(row_v2[3]),float(previous_row_v2[2]),float(previous_row_v2[3]))
            bearing_v2 = new_bearing(float(previous_row_v2[3]),float(previous_row_v2[2]),float(row_v2[3]),float(row_v2[2]))
            #print "Printing for Vehicle 2"
            #print distance_v2
            #print bearing_v2

            #rec(float(previous_row[3]),float(previous_row[2]),float(bearing_v1),float(distance_v1))
            x_cords_v2,y_cords_v2 = rec(float(row_v2[3]),float(row_v2[2]),float(bearing_v2),float(distance_v2))    
            previous_row_v2[3] = row_v2[3]
            previous_row_v2[2] = row_v2[2]


            #print "new" + previous_row_v2[2],previous_row_v2[3] 
            x1_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[0]),float(y_cords_v2[0]))
            y1_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[0]),float(y_cords_v2[0]))
            x2_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[1]),float(y_cords_v2[1]))
            y2_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[1]),float(y_cords_v2[1]))
            x3_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[2]),float(y_cords_v2[2]))
            y3_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[2]),float(y_cords_v2[2]))
            x4_v2 = XfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[3]),float(y_cords_v2[3]))
            y4_v2 = YfromGPS(float(x_origin),float(y_origin),float(x_cords_v2[3]),float(y_cords_v2[3]))
               
            #print "Cartesian Points for vehicle 2 are: "
            #print x1_v2,y1_v2,x2_v2,y2_v2,x3_v2,y3_v2,x4_v2,y4_v2
            x_v2 = np.array([x1_v2,x2_v2,x3_v2,x4_v2])
            y_v2 = np.array([y1_v2,y2_v2,y3_v2,y4_v2])
            #print x_v2,y_v2
            #print x_cords_v2,y_cords_v2

            vehicle_1 = np.array([(x1_v1,y1_v1),(x2_v1,y2_v1),(x3_v1,y3_v1),(x4_v1,y4_v1)])
            vehicle_2 = np.array([(x1_v2,y1_v2),(x2_v2,y2_v2),(x3_v2,y3_v2),(x4_v2,y4_v2)])

            col = collide(vehicle_1,vehicle_2)
            #if col[0] == False:
            if col == False:
                kml_file.write('<Placemark><TimeStamp><when>'+row_v1[1]+','+'</when></TimeStamp><styleUrl>#msn_cabs2</styleUrl><Point><coordinates>'+row_v1[2]+','+row_v1[3]+','+',0</coordinates></Point></Placemark>\n')
                kml_file.write('<Placemark><TimeStamp><when>'+row_v2[1]+','+'</when></TimeStamp><styleUrl>#msn_cabs1</styleUrl><Point><coordinates>'+row_v2[2]+','+row_v2[3]+','+',0</coordinates></Point></Placemark>\n')

            else:
                kml_file.write('<Placemark><TimeStamp><when>'+row_v1[1]+','+'</when></TimeStamp><styleUrl>#msn_cabs3</styleUrl><Point><coordinates>'+row_v1[2]+','+row_v1[3]+','+',0</coordinates></Point></Placemark>\n')
                kml_file.write('<Placemark><TimeStamp><when>'+row_v2[1]+','+'</when></TimeStamp><styleUrl>#msn_cabs3</styleUrl><Point><coordinates>'+row_v2[2]+','+row_v2[3]+','+',0</coordinates></Point></Placemark>\n')

            print (col)


            #break

        except IndexError:
            pass 

    kml_file.write('''\t</Document>                                                                                                           
</kml>''')   

