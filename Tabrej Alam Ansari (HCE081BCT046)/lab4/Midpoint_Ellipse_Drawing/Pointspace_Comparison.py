import matplotlib.pyplot as plt

def midpoint_ellipse(rx, ry, xc, yc):
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry
    tworx2 = 2 * rx2
    twory2 = 2 * ry2

    # Region 1
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
    dx = 0
    dy = tworx2 * y

    region1_points = []
    region2_points = []

    while dx < dy:  # Region 1
        region1_points.extend([
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

    # Region 2
    p2 = ry2 * (x + 0.5)**2 + rx2 * (y - 1)**2 - rx2 * ry2
    while y >= 0:
        region2_points.extend([
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

    return region1_points, region2_points

# Example ellipse
rx, ry, xc, yc = 60, 40, 100, 100
region1, region2 = midpoint_ellipse(rx, ry, xc, yc)

# Plotting
plt.figure(figsize=(7,7))
if region1:
    x1, y1 = zip(*region1)
    plt.scatter(x1, y1, s=5, color='blue', label='Region 1 (slope < 1)')
if region2:
    x2, y2 = zip(*region2)
    plt.scatter(x2, y2, s=5, color='red', label='Region 2 (slope ≥ 1)')

plt.gca().set_aspect('equal')
plt.title("Midpoint Ellipse Algorithm: Region 1 vs Region 2")
plt.legend()
plt.grid(True)
plt.show()