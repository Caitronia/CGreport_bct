import matplotlib.pyplot as plt

def midpoint_ellipse(rx, ry, xc, yc):
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry

    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    X, Y = [], []

    while (2 * ry2 * x) <= (2 * rx2 * y):
        X.extend([xc + x, xc - x, xc + x, xc - x])
        Y.extend([yc + y, yc + y, yc - y, yc - y])

        if p1 < 0:
            x += 1
            p1 += 2 * ry2 * x + ry2
        else:
            x += 1
            y -= 1
            p1 += 2 * ry2 * x - 2 * rx2 * y + ry2

    p2 = (ry2 * (x + 0.5)**2) + (rx2 * (y - 1)**2) - (rx2 * ry2)

    while y >= 0:
        X.extend([xc + x, xc - x, xc + x, xc - x])
        Y.extend([yc + y, yc + y, yc - y, yc - y])

        if p2 > 0:
            y -= 1
            p2 += rx2 - 2 * rx2 * y
        else:
            y -= 1
            x += 1
            p2 += 2 * ry2 * x - 2 * rx2 * y + rx2

    return X, Y


ellipses = [
    (80, 40, 0, 0, 'red'),
    (60, 30, 150, 50, 'blue'),
    (40, 70, -150, -50, 'green')
]

plt.figure()

for rx, ry, xc, yc, color in ellipses:
    x, y = midpoint_ellipse(rx, ry, xc, yc)
    plt.scatter(x, y, s=8, c=color, label=f"rx={rx}, ry={ry}")

plt.title("Ellipses with Different Radii and Centres")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.gca().set_aspect('equal')
plt.grid(True)
plt.legend()
plt.show()
