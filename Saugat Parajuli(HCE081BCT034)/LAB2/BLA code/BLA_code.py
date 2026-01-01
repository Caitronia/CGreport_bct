import matplotlib.pyplot as plt

def bresenham(x1, y1, x2, y2):
    x_points = []
    y_points = []

    dx = x2 - x1
    dy = y2 - y1

    p = 2 * dy - dx
    x, y = x1, y1

    x_points.append(x)
    y_points.append(y)

    while x < x2:
        x += 1
        if p < 0:
            p = p + 2 * dy
        else:
            y += 1
            p = p + 2 * (dy - dx)

        x_points.append(x)
        y_points.append(y)

    return x_points, y_points


# Input points
x1, y1 = 2, 2
x2, y2 = 10, 6

x, y = bresenham(x1, y1, x2, y2)

# Plotting the line
plt.plot(x, y, marker='o')
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Bresenham Line Drawing Algorithm")
plt.grid(True)
plt.show()
