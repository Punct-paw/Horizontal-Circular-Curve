import numpy as np
from dataclasses import dataclass

# DataClass
@dataclass
class Point:
    x: float
    y: float

# CurveCalculation
class Horizontal_Circular_Curve:
    @staticmethod
    def Deg_toRad(deg):
        return deg * np.pi / 180

    @staticmethod
    def circular_curve(BB, AB, PI: Point, D):
        Delta = abs(AB - BB)  # Deflection angle in degrees
        R = 100 / D * 180 / np.pi  # Radius from degree of curve
        L = R * Delta * (np.pi / 180)  # Arc length
        LC = 2 * R * np.sin(Horizontal_Circular_Curve.Deg_toRad(Delta) / 2)  # Chord length
        T = R * np.tan(Horizontal_Circular_Curve.Deg_toRad(Delta) / 2)  # Tangent length
        E = R * ((1 / np.cos(Horizontal_Circular_Curve.Deg_toRad(Delta) / 2)) - 1)  # External distance
        M = R * (1 - np.cos(Horizontal_Circular_Curve.Deg_toRad(Delta) / 2))  # Middle ordinate
        BBAzimuth = Horizontal_Circular_Curve.Deg_toRad(BB)  # Back bearing in radians
        ABAzimuth = Horizontal_Circular_Curve.Deg_toRad(AB)  # Ahead bearing in radians
        PC = Point(x=PI.x - T * np.sin(BBAzimuth), y=PI.y - T * np.cos(BBAzimuth))  # Point of Curvature
        PT = Point(x=PI.x + T * np.sin(ABAzimuth), y=PI.y + T * np.cos(ABAzimuth))  # Point of Tangency
        return Delta, R, L, LC, T, E, M, BBAzimuth, ABAzimuth, PC, PT

    @staticmethod
    def Find_center_of_circle(PC, PT, BB, AB, R):
        # Calculate signed deflection angle
        Delta_signed = ((AB - BB) + 180) % 360 - 180
        Direction = 'LHC' if Delta_signed > 0 else 'RHC'  # LHC: counterclockwise, RHC: clockwise

        # Calculate midpoint of chord (PC-PT)
        Mid_Chord = Point(x=(PC.x + PT.x) / 2, y=(PC.y + PT.y) / 2)
        # Calculate chord length
        Chord_length = np.sqrt((PT.x - PC.x) ** 2 + (PT.y - PC.y) ** 2)
        # Chord vector
        dx = PT.x - PC.x
        dy = PT.y - PC.y
        # Calculate perpendicular distance from midpoint to center
        Half_Chord = Chord_length / 2
        perpendicular_distance = np.sqrt(R ** 2 - Half_Chord ** 2)
        # Perpendicular unit vector (counterclockwise from chord)
        nx = -dy / Chord_length
        ny = dx / Chord_length
        # Calculate center coordinates
        if Direction == 'RHC':  # Clockwise: center on clockwise side
            Center_Point = Point(
                x=Mid_Chord.x - perpendicular_distance * nx,
                y=Mid_Chord.y - perpendicular_distance * ny
            )
        else:  # LHC: counterclockwise
            Center_Point = Point(
                x=Mid_Chord.x + perpendicular_distance * nx,
                y=Mid_Chord.y + perpendicular_distance * ny
            )
        return Center_Point, Direction

    @staticmethod
    def Generate_arc_points(Center_Point, PC, PT, R, Direction, num_points=100):
        # Calculate angles of PC and PT relative to the center
        angle_start = np.atan2(PC.y - Center_Point.y, PC.x - Center_Point.x)
        angle_end = np.atan2(PT.y - Center_Point.y, PT.x - Center_Point.x)

        # Normalize angles to [0, 2π)
        angle_start = angle_start % (2 * np.pi)
        angle_end = angle_end % (2 * np.pi)

        # Ensure correct sweep direction
        if Direction == 'RHC':  # Clockwise (negative sweep)
            if angle_start < angle_end:
                angle_start += 2 * np.pi
        else:  # LHC (counterclockwise, positive sweep)
            if angle_end < angle_start:
                angle_end += 2 * np.pi

        # Generate angles
        angles = np.linspace(angle_start, angle_end, num_points)

        # Generate arc points
        arc_points = []
        for a in angles:
            point = Point(
                x=Center_Point.x + R * np.cos(a),
                y=Center_Point.y + R * np.sin(a)
            )
            arc_points.append(point)
        return arc_points