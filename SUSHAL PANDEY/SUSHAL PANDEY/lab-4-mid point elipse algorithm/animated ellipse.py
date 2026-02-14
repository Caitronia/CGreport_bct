import matplotlib.pyplot as plt
import time
from IPython.display import display, clear_output

def midpoint_ellipse_animation(rx, ry, xc, yc, delay=1):
    x = 0
    y = ry

    rx2 = rx * rx
    ry2 = ry * ry

    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    fig, ax = plt.subplots(figsize=(6,4))
    ax.set_aspect('equal')
    ax.set_xlim(xc - rx - 10, xc + rx + 10)
    ax.set_ylim(yc - ry - 10, yc + ry + 10)
    ax.set_title("Midpoint Ellipse Animation")
    ax.grid(True)

    X, Y = [], []

    # Region 1 
    while (2 * ry2 * x) <= (2 * rx2 * y):
        for px, py in [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y)
        ]:
            X.append(px)
            Y.append(py)

        ax.plot(X, Y, 'b.')
        clear_output(wait=True)
        display(fig)
        time.sleep(delay)

        if p1 < 0:
            x += 1
            p1 += 2 * ry2 * x + ry2
        else:
            x += 1
            y -= 1
            p1 += 2 * ry2 * x - 2 * rx2 * y + ry2

    p2 = (ry2 * (x + 0.5)**2) + (rx2 * (y - 1)**2) - (rx2 * ry2)

    # Region 2 
    while y >= 0:
        for px, py in [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y)
        ]:
            X.append(px)
            Y.append(py)

        ax.plot(X, Y, 'b.')
        clear_output(wait=True)
        display(fig)
        time.sleep(delay)

        if p2 > 0:
            y -= 1
            p2 += rx2 - 2 * rx2 * y
        else:
            y -= 1
            x += 1
            p2 += 2 * ry2 * x - 2 * rx2 * y + rx2

    plt.show()


midpoint_ellipse_animation(80, 50, 0, 0, delay=1)