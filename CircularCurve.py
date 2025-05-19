import numpy as np
from dataclasses import dataclass

#DataClass
@dataclass
class Point:
    x:float
    y:float

#CurveCalculation    
class Horizontal_Circular_Curve:
    
    @staticmethod
    def circular_curve(BB, AB, PI: Point, D):
        Delta = abs(AB - BB)  # Central angle
        if Delta>180 :
            Delta=360-Delta

        R = 18000 / (np.pi * D)  # Radius formula for degree of curve
        L = R * np.deg2rad(Delta)  # Arc length
        LC = 2 * R * np.sin(np.deg2rad(Delta / 2))  # Long chord
        T = R * np.tan(np.deg2rad(Delta / 2))  # Tangent length
        E = R * ((1 / np.cos(np.deg2rad(Delta / 2))) - 1)  # External distance
        M = R * (1 - np.cos(np.deg2rad(Delta / 2)))  # Middle ordinate

        # Bearings in radians
        BBAzimuth = np.deg2rad(BB)
        ABAzimuth = np.deg2rad(AB)

        # Back tangent direction (from PI to PC)
        PC = Point(
        x=PI.x - T * np.sin(BBAzimuth),
        y=PI.y - T * np.cos(BBAzimuth)
        )

        # Ahead tangent direction (from PI to PT)
        PT = Point(
        x=PI.x + T * np.sin(ABAzimuth),
        y=PI.y + T * np.cos(ABAzimuth)
        )

        return (Delta, R, L, LC, T, E, M, BBAzimuth, ABAzimuth, PC, PT)

    @staticmethod
    def Find_center_of_circle(PC,PT,BB,AB,R):
        # Finding Direction of the curve, either Right hand side or Left hand side i.e. clockwise or anticlockwise from PT to PC

        Direction_Angle=(AB-BB+360) %360
        if  0<Direction_Angle<180:  
            Direction='RHC'
        else:
            Direction='LHC'

        #Calculate the midpoint of the chord (PC-PT)
        Mid_Chord=Point(x=(PC.x+PT.x)/2, y=(PC.y+PT.y)/2)

        #Calculate the length of the chord (PC-PT)
        Chord_length=np.sqrt((PT.x-PC.x)**2+(PT.y-PC.y)**2)

        #Chord Vector (normalized perpendicular vector to chord)
        dx=PT.x-PC.x
        dy=PT.y-PC.y
        
        #Calculate the perpendicualr distance from the midpoint to the center
        Half_Chord=Chord_length/2
        perpendicular_distance=np.sqrt(R**2-Half_Chord**2)

        #perpendicular unit vector
        nx=-dy/Chord_length
        ny=dx/Chord_length

        #Calculate the Center coordinates
        if Direction=='RHC':
            Center_Point=Point(x=Mid_Chord.x+perpendicular_distance*nx,y=Mid_Chord.y+perpendicular_distance*ny)
        else:
            Center_Point=Point(x=Mid_Chord.x-perpendicular_distance*nx,y=Mid_Chord.y-perpendicular_distance*ny)
        return Center_Point,Direction
    
    @staticmethod
    def Generate_arc_points(Center_Point, PC: Point, PT: Point, R, Direction):
        # Calculate angles from center to PC and PT with respect to x direction counterclockwise
        theta_start = np.arctan2(PT.y - Center_Point.y, PT.x - Center_Point.x)
        theta_end = np.arctan2(PC.y - Center_Point.y, PC.x - Center_Point.x)

        # Fix sweep direction
        if Direction == 'RHC':
            if theta_end > theta_start:
                theta_end -= 2 * np.pi
        else:
            if theta_end < theta_start:
                theta_end += 2 * np.pi

        # Interpolate angles
        angles = np.linspace(theta_start, theta_end, 100)
    
        #Calculating the arc points
        arc_points = [
        Point(
            x=Center_Point.x + R * np.cos(angle),
            y=Center_Point.y + R * np.sin(angle)
            ) for angle in angles
        ]

        return arc_points  # Return the full list
            
