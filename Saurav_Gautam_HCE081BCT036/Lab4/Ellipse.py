import matplotlib.pyplot as plt


def add_symmetric_points(dx_val, dy_val, center_x, center_y, xs, ys):
    xs.extend([
        center_x + dx_val,
        center_x - dx_val,
        center_x + dx_val,
        center_x - dx_val
    ])
    ys.extend([
        center_y + dy_val,
        center_y + dy_val,
        center_y - dy_val,
        center_y - dy_val
    ])


def midpoint_ellipse_algo(center_x, center_y, radius_x, radius_y):
    x_pos = 0
    y_pos = radius_y

    x_coords = []
    y_coords = []

    decision_region1 = (radius_y ** 2) - (radius_x ** 2 * radius_y) + (0.25 * radius_x ** 2)

    delta_x = 2 * (radius_y ** 2) * x_pos
    delta_y = 2 * (radius_x ** 2) * y_pos

    while delta_x < delta_y:
        add_symmetric_points(x_pos, y_pos, center_x, center_y, x_coords, y_coords)

        if decision_region1 < 0:
            x_pos += 1
            delta_x += 2 * (radius_y ** 2)
            decision_region1 += delta_x + (radius_y ** 2)
        else:
            x_pos += 1
            y_pos -= 1
            delta_x += 2 * (radius_y ** 2)
            delta_y -= 2 * (radius_x ** 2)
            decision_region1 += delta_x - delta_y + (radius_y ** 2)

    decision_region2 = (
        (radius_y ** 2) * ((x_pos + 0.5) ** 2) +
        (radius_x ** 2) * ((y_pos - 1) ** 2) -
        (radius_x ** 2) * (radius_y ** 2)
    )

    while y_pos >= 0:
        add_symmetric_points(x_pos, y_pos, center_x, center_y, x_coords, y_coords)

        if decision_region2 > 0:
            y_pos -= 1
            delta_y -= 2 * (radius_x ** 2)
            decision_region2 += (radius_x ** 2) - delta_y
        else:
            y_pos -= 1
            x_pos += 1
            delta_x += 2 * (radius_y ** 2)
            delta_y -= 2 * (radius_x ** 2)
            decision_region2 += delta_x - delta_y + (radius_x ** 2)

    return x_coords, y_coords



center_x = 5
center_y = 10
radius_x = 50
radius_y = 100

x_vals, y_vals = midpoint_ellipse_algo(center_x, center_y, radius_x, radius_y)

plt.scatter(x_vals, y_vals)
plt.title("Midpoint Ellipse Algorithm")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()