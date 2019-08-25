import gdspy
import math

wire_width = 0.130
turn_width = 2
pitch = 0.240
space_width = pitch - wire_width
active_diameter = 15
lined_area = 60
active_radius = active_diameter / 2
lead_width = 1

def add_line(cell: gdspy.Cell, y, side):
    x = side * lined_area / 2

    if abs(y) > active_radius:
        end_x = lead_width / 2
        end_x = math.copysign(end_x, x)
        start_x = -end_x
    else:
        end_x = math.sqrt(max(active_radius ** 2 - y ** 2, 0))
        end_x = math.copysign(end_x, -x)
        start_x = end_x - math.copysign(turn_width, x)
    line_1 = gdspy.RobustPath((x, y), space_width, ends='round')
    line_2 = gdspy.RobustPath((start_x, y), space_width, ends='round')
    cell.add(line_1)
    cell.add(line_2)
    line_1.segment((end_x, y))
    line_2.segment((-x, y))


def make_nanowire_meander():
    meander = gdspy.Cell('MEANDER')

    y = 0
    while y < lined_area / 2:
        add_line(meander, y, -1)
        y += 2 * pitch        

    y = -2 * pitch
    while y > -lined_area / 2:
        add_line(meander, y, -1)
        y -= 2 * pitch

    y = pitch
    while y < lined_area / 2:
        add_line(meander, y, 1)
        y += 2 * pitch

    y = -pitch
    while y > -lined_area / 2:
        add_line(meander, y, 1)
        y -= 2 * pitch
    return meander


def make_circle():
    circle = gdspy.Cell('CIRCLE')
    left_circle = gdspy.RobustPath((-turn_width, -active_radius), width=pitch, ends='round')
    left_circle.arc(active_radius, 3 * math.pi / 2, math.pi / 2)
    circle.add(left_circle)
    right_circle = gdspy.RobustPath((turn_width, active_radius), width=pitch, ends='round')
    right_circle.arc(active_radius, math.pi / 2, -math.pi / 2)
    circle.add(right_circle)

    return circle


meander = make_nanowire_meander()
circle = make_circle()
dev_poly = gdspy.boolean(meander.get_polygons(), circle.get_polygons(), 'or')
device = gdspy.Cell('DEVICE')
device.add(dev_poly)

gdspy.LayoutViewer()

