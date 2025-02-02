import gdspy
import math

bridge_straight_dim = (10, 1.5)
bridge_taper_dim = (50, 100)
lead_dim = (150, 500)
lead_curve_radius = 50
film_dim = (2000, 1000)
film_height_buffer = 1000
bridge_border = 1
lead_border = 10
border_taper_start = 0.25


def border_interpolate(u):
    if u < border_taper_start:
        return bridge_border
    else:
        return (u - border_taper_start) * (lead_border - bridge_border) / (1 - border_taper_start) + bridge_border


quarter_bridge_cell = gdspy.Cell('QUARTER_BRIDGE')

quarter_bridge = gdspy.RobustPath((0, bridge_straight_dim[1] / 2 + bridge_border / 2), bridge_border, ends='round')
quarter_bridge.segment((bridge_straight_dim[0] / 2, bridge_straight_dim[1] / 2 + bridge_border / 2), relative=False)
quarter_bridge.bezier(
    [(bridge_taper_dim[0] + bridge_straight_dim[0] / 2, bridge_straight_dim[1] / 2 + bridge_border / 2),
     (bridge_taper_dim[0] + bridge_straight_dim[0] / 2, bridge_taper_dim[1])],
    width=border_interpolate, relative=False)
qb_lead_turn_start = (bridge_taper_dim[0] + bridge_straight_dim[0] / 2, lead_dim[1] / 2 - lead_curve_radius)
quarter_bridge.segment(qb_lead_turn_start, relative=False)
quarter_bridge.turn(lead_curve_radius, -math.pi / 2)
quarter_bridge.segment((lead_dim[0], lead_dim[1] / 2))
quarter_bridge.turn(math.sqrt(2) * (film_dim[1] + film_height_buffer - lead_dim[1]), math.pi / 4)
quarter_bridge_cell.add(quarter_bridge)

tuning_fork_half = gdspy.RobustPath(qb_lead_turn_start, lead_border)
tuning_fork_half.segment((qb_lead_turn_start[0], qb_lead_turn_start[1] + lead_curve_radius))
tuning_fork_half.bezier([(qb_lead_turn_start[0], qb_lead_turn_start[1] + 2 * lead_curve_radius),
                         (0, qb_lead_turn_start[1] + 2 * lead_curve_radius),
                         (0, qb_lead_turn_start[1] + 3 * lead_curve_radius)], relative=False)
tuning_fork_half.segment((0, film_dim[1] + film_height_buffer))

quarter_bridge_cell.add(tuning_fork_half)

qb_right = gdspy.boolean(quarter_bridge.to_polygonset(), tuning_fork_half.to_polygonset(), 'or')
qb_left = gdspy.copy(qb_right)
qb_left.mirror((0, 1))

bridge_top = gdspy.boolean(qb_right, qb_left, 'or')
bridge_bottom = gdspy.copy(bridge_top)
bridge_bottom.mirror((1, 0))

bridge = gdspy.Cell('BRIDGE')
bridge.add([bridge_top, bridge_bottom])

main = gdspy.Cell('MAIN')
main.add(gdspy.CellArray(bridge, 2, 2, (10000, 10000)))

# Save all created cells in file 'first.gds'.
gdspy.write_gds('bridge.gds')

# Optionally, display all cells using the internal viewer.
gdspy.LayoutViewer()
