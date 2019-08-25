import gdspy
import math

wire_width = 0.130
turn_width = 0.2
pitch = 0.240
active_diameter = 15
active_radius = active_diameter / 2


def linear_segment(path: gdspy.RobustPath, start):
    x = math.sqrt(max(active_radius ** 2 - start[1] ** 2, 0))
    if start[0] <= 0:
        displacement = (x - start[0], 0)
    else:
        displacement = (-x - start[0], 0)

    path.segment(displacement, relative=True)

    return start[0] + displacement[0], start[1]


def turn(path: gdspy.RobustPath, direction: int, start):
    # width_function = lambda u: (math.cos(u / (math.pi / 8)) ** 2) * wire_width\
    #                            + (math.sin(u / (math.pi / 8)) ** 2) * turn_width
    radius = pitch / 2
    path.turn(radius, direction * math.pi)

    if direction * start[0]:
        end_y = start[1] + 2 * radius
    else:
        end_y = start[1] - 2 * radius

    return start[0], end_y


def make_nanowire_meander():
    path = gdspy.RobustPath((-active_radius, 0), wire_width)
    start = (0, 0)
    position = start
    direction = -1
    half_meander = gdspy.Cell('HALF_MEANDER')
    half_meander.add(path)

    while abs(position[1]) < active_radius:
        position = linear_segment(path, position)
        position = turn(path, direction, position)
        direction *= -1
        print(position)

    path.segment((-position[0], 0), relative=True)

    gdspy.LayoutViewer()


make_nanowire_meander()
