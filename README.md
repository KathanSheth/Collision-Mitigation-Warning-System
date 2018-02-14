# GPS Based Collision Mitigation Warning System

---


[//]: # (Image References)
[image1]: ./images/rectangle.png
[image2]: ./images/output.png

## This project is first part of three project series which is related to Self-driving car. Vehicle-to-Vehicle (V2V) communication is very important part of self-driven cars and safety is the most important aspect of self-driven car. This system provides warning if two cars are approaching to each other and are in "Danger" zone. 


### File Structure : 

input_v1.csv - dataset for vehicle 1

input_v2.csv - dataset for vehicle 2

car_collison.py - includes functions for heading, distance, cartesian coordinate conversion, Rectangle formation and Collision detection

kml_generate.py - File to generate the output file which will be in the form of '.kml' file. You can open it in Google Earth for visualization.


### Run Command:

`python kml_generate.py input_v1.csv input_v2.csv`

# Working:

When running this application in Google Earth using .kml file(output generated from this system), car color changes to "RED" if there is a chance of collision between two cars. The concept includes heading calculation, harvesine distance, define rectangle area according to velocity and check collision with Separte Axis Theorem.

## 1. Distance and Heading Calculation


GPS locations for two vehicles (Vehicle 1 and Vehicle 2) are given in csv files for four different datasets. 

From difference between two consecutive GPS coordinate data and timestamp, we can find the vehicles heading and distance for both the vehicles. I have used Harvesine formula for distance calculation between two points which is written in `harvesine`function.

Bearing (Heading) calculation is explained in `new_bearing` function. 

## 2. Define Rectangle to find collision. 

ASSUMTION - Lane width is 4m and Time to Collide (TTC) is 8 seconds.

![alt text][image1]

Here the idea is to define rectangle in the direction of heading. This rectangle indicates "danger" zone for that car. 
Basically, we have to define rectangle from following steps:

- Calculate the length of the rectangle which depends on velocity of the car 
- Width, which is fixed(4m)
- Define points in the direction of heading.

This is defined in `rec` function. See the code for more explanation regarding implementation.

## 3. Cartesian Coordinates

After getting the rectangle coordinates, convert those to cartesian coordinates and get (x1,y1) , (x2,y2) , (x3,y3) , (x4,y4).

This is explained in `XfromGPS` and `YfromGPS`

## 4. Collision Detection using SAT

This is the final section which includes collision detection using two rectangles (defined earlier for two cars) using Separate Axis Theorem. 

This is defined in `collision` and `separating_axis` functions.

The final output looks like this:

![alt text][image2]

## Reference:

The idea (Question definition) is from one of the projects from Wayne State University which I got from Internet.

Credit to https://hackmd.io/s/ryFmIZrsl for explaining Separate axis theorem.


