import matplotlib.pyplot as plt

def bresenham_line(x1, y1, x2, y2):
    xes, yes = [], []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x2 >= x1 else -1
    sy = 1 if y2 >= y1 else -1

    x, y = x1, y1

    if dx >= dy:
        p = 2 * dy - dx
        for _ in range(dx + 1):
            xes.append(x)
            yes.append(y)
            x += sx
            if p >= 0:
                y += sy
                p += 2 * (dy - dx)
            else:
                p += 2 * dy
    else:
        p = 2 * dx - dy
        for _ in range(dy + 1):
            xes.append(x)
            yes.append(y)
            y += sy
            if p >= 0:
                x += sx
                p += 2 * (dx - dy)
            else:
                p += 2 * dx

    return xes, yes


def plot_bresenham():
    print("Enter the coordinates for Bresenham Line Drawing")

    x1 = int(input("Enter x1: "))
    y1 = int(input("Enter y1: "))
    x2 = int(input("Enter x2: "))
    y2 = int(input("Enter y2: "))

    xes, yes = bresenham_line(x1, y1, x2, y2)

    plt.figure(figsize=(6, 6))
    plt.plot(xes, yes, marker='o', linestyle='-', linewidth=1)
    plt.title("Bresenham Line Drawing Algorithm")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.axis('equal')
    plt.show()


# Call the function
plot_bresenham()
