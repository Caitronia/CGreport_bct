import matplotlib.pyplot as plt

def bresenham(x0, y0, x1, y1):
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1

    x, y = x0, y0

    if dx >= dy:
        err = dx / 2
        for _ in range(dx + 1):
            points.append((x, y))
            x += sx
            err -= dy
            if err < 0:
                y += sy
                err += dx
    else:
        err = dy / 2
        for _ in range(dy + 1):
            points.append((x, y))
            y += sy
            err -= dx
            if err < 0:
                x += sx
                err += dy

    return points

x0, y0 = 2, 3
x1, y1 = 10, 7

points = bresenham(x0, y0, x1, y1)

x_vals = [p[0] for p in points]
y_vals = [p[1] for p in points]

plt.plot(x_vals, y_vals, marker='o')
plt.show()


import matplotlib.pyplot as plt

# DDA Line
def dda(x1, y1, x2, y2):
    x_pts, y_pts = [], []
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1

    for i in range(steps + 1):
        x_pts.append(round(x))
        y_pts.append(round(y))
        x += x_inc
        y += y_inc

    return x_pts, y_pts

# Bresenham Line
def bresenham(x0, y0, x1, y1):
    points_x, points_y = [], []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x1 >= x0 else -1
    sy = 1 if y1 >= y0 else -1
    x, y = x0, y0

    if dx >= dy:
        p = 2*dy - dx
        for _ in range(dx + 1):
            points_x.append(x)
            points_y.append(y)
            x += sx
            if p >= 0:
                y += sy
                p += 2*dy - 2*dx
            else:
                p += 2*dy
    else:
        p = 2*dx - dy
        for _ in range(dy + 1):
            points_x.append(x)
            points_y.append(y)
            y += sy
            if p >= 0:
                x += sx
                p += 2*dx - 2*dy
            else:
                p += 2*dx

    return points_x, points_y

# Compare lines
x1, y1, x2, y2 = 2, 3, -10, 15

x_d, y_d = dda(x1, y1, x2, y2)
x_b, y_b = bresenham(x1, y1, x2, y2)

plt.figure(figsize=(6,6))
plt.plot(x_d, y_d, marker='o', linestyle='-', color='red', label='DDA')
plt.plot(x_b, y_b, marker='x', linestyle='-', color='green', label='Bresenham')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.title("DDA vs Bresenham (Different Octant)")
plt.show()




