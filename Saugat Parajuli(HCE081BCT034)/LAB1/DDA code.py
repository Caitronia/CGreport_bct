import matplotlib.pyplot as plt

def dda_line(x1, y1, x2, y2):
    points = []

    dx = x2 - x1
    dy = y2 - y1

    steps = int(max(abs(dx), abs(dy)))

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    for _ in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_inc
        y += y_inc

    return points


# input coordinates
x1, y1 = 2, 2
x2, y2 = 12, 7

# generate line points
line_points = dda_line(x1, y1, x2, y2)

# separate x and y for plotting
x_vals = [p[0] for p in line_points]
y_vals = [p[1] for p in line_points]

# plot
plt.figure()
plt.plot(x_vals, y_vals, marker='o')
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()
