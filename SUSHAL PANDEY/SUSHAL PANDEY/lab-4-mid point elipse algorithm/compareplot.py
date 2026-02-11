import matplotlib.pyplot as plt

def midpoint_ellipse_regions(rx, ry, xc, yc):
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry

    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    R1x, R1y = [], []
    R2x, R2y = [], []

    # -------- Region 1 --------
    while (2 * ry2 * x) <= (2 * rx2 * y):
        R1x.append(xc + x)
        R1y.append(yc + y)

        if p1 < 0:
            x += 1
            p1 += 2 * ry2 * x + ry2
        else:
            x += 1
            y -= 1
            p1 += 2 * ry2 * x - 2 * rx2 * y + ry2

    p2 = (ry2 * (x + 0.5)**2) + (rx2 * (y - 1)**2) - (rx2 * ry2)

    #  Region 2 
    while y >= 0:
        R2x.append(xc + x)
        R2y.append(yc + y)

        if p2 > 0:
            y -= 1
            p2 += rx2 - 2 * rx2 * y
        else:
            y -= 1
            x += 1
            p2 += 2 * ry2 * x - 2 * rx2 * y + rx2

    return R1x, R1y, R2x, R2y


rx, ry = 100, 60
xc, yc = 0, 0

r1x, r1y, r2x, r2y = midpoint_ellipse_regions(rx, ry, xc, yc)

plt.scatter(r1x, r1y, label="Region 1")
plt.scatter(r2x, r2y, label="Region 2")

plt.title("Point Spacing in Region 1 vs Region 2")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.gca().set_aspect('equal')
plt.grid(True)
plt.show()