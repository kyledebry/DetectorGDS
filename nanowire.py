import gdspy
import math

wire_width = 0.130
pitch = 0.240
active_diameter = 15
active_radius = active_diameter / 2

def linear_segment(path: gdspy.RobustPath, start):
    x ** 2 + y ** 2 = r

path = gdspy.RobustPath((0, 0), wire_width)

