import matplotlib.pyplot as plt

def midpoint_ellipse(rx, ry, xc, yc):
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry
    tworx2 = 2 * rx2
    twory2 = 2 * ry2

    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    dx = 0
    dy = tworx2 * y

    points = []

    while dx < dy:
        points.extend([
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y)
        ])
        x += 1
        dx += twory2
        if p1 < 0:
            p1 += ry2 + dx
        else:
            y -= 1
            dy -= tworx2
            p1 += ry2 + dx - dy

    p2 = ry2 * (x + 0.5)**2 + rx2 * (y - 1)**2 - rx2 * ry2
    while y >= 0:
        points.extend([
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y)
        ])
        y -= 1
        dy -= tworx2
        if p2 > 0:
            p2 += rx2 - dy
        else:
            x += 1
            dx += twory2
            p2 += rx2 - dy + dx

    return points

# Define multiple ellipses with different radii and centers
ellipses = [
    (60, 40, 100, 100),
    (30, 70, 200, 150),
    (50, 50, 300, 80),
    (80, 30, 150, 250)
]

# Plotting
plt.figure(figsize=(8, 8))
for rx, ry, xc, yc in ellipses:
    points = midpoint_ellipse(rx, ry, xc, yc)
    x_vals, y_vals = zip(*points)
    plt.scatter(x_vals, y_vals, s=1)

plt.gca().set_aspect('equal')
plt.title("Multiple Ellipses with Midpoint Algorithm")
plt.grid(True)
plt.show()