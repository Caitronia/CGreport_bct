import matplotlib.pyplot as plt

def plot_ellipse_points(x, y, xc, yc, x_points, y_points):
    
    x_points.extend([xc + x, xc - x, xc + x, xc - x])
    y_points.extend([yc + y, yc + y, yc - y, yc - y])


def midpoint_ellipse(xc, yc, rx, ry):
    x = 0
    y = ry

    x_points = []
    y_points = []

    p1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)

    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y

    while dx < dy:
        plot_ellipse_points(x, y, xc, yc, x_points, y_points)

        if p1 < 0:
            x += 1
            dx = dx + (2 * ry * ry)
            p1 = p1 + dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            p1 = p1 + dx - dy + (ry * ry)
    p2 = ((ry * ry) * ((x + 0.5) ** 2)) + \
         ((rx * rx) * ((y - 1) ** 2)) - \
         (rx * rx * ry * ry)


    while y >= 0:
        plot_ellipse_points(x, y, xc, yc, x_points, y_points)

        if p2 > 0:
            y -= 1
            dy = dy - (2 * rx * rx)
            p2 = p2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            p2 = p2 + dx - dy + (rx * rx)

    return x_points, y_points



xc = 0     
yc = 0    
rx = 20   
ry = 10   

x_pts, y_pts = midpoint_ellipse(xc, yc, rx, ry)

plt.scatter(x_pts, y_pts)
plt.title("Midpoint Ellipse Algorithm")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()
