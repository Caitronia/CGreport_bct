import matplotlib.pyplot as plt

def plot_points(xc, yc, x, y, color):
    plt.scatter(
        [xc + x, xc - x, xc + x, xc - x],
        [yc + y, yc + y, yc - y, yc - y],
        c=color, s=10
    )

def animated_colored_ellipse(xc, yc, rx, ry):
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_title("Animated Midpoint Ellipse")
    ax.set_aspect('equal')
    ax.grid(True)

    # IMPORTANT: give limits so points are visible
    ax.set_xlim(xc - rx - 5, xc + rx + 5)
    ax.set_ylim(yc - ry - 5, yc + ry + 5)

    x = 0
    y = ry

    p1 = ry**2 - rx**2 * ry + 0.25 * rx**2
    dx = 2 * ry**2 * x
    dy = 2 * rx**2 * y

    while dx < dy:
        plot_points(xc, yc, x, y, 'red')
        plt.pause(0.05)

        if p1 < 0:
            x += 1
            dx += 2 * ry**2
            p1 += dx + ry**2
        else:
            x += 1
            y -= 1
            dx += 2 * ry**2
            dy -= 2 * rx**2
            p1 += dx - dy + ry**2

    p2 = (ry**2) * (x + 0.5)**2 + (rx**2) * (y - 1)**2 - rx**2 * ry**2

    while y > 0:
        plot_points(xc, yc, x, y, 'blue')
        plt.pause(0.05)

        if p2 > 0:
            y -= 1
            dy -= 2 * rx**2
            p2 += rx**2 - dy
        else:
            y -= 1
            x += 1
            dx += 2 * ry**2
            dy -= 2 * rx**2
            p2 += dx - dy + rx**2

    plt.ioff()
    plt.show(block=True)


animated_colored_ellipse(0, 0, 30, 20)
