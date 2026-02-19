import matplotlib.pyplot as plt
def plot_points(cx, cy, x, y, xs, ys):
    points = [
        (x + cx,  y + cy),
        (-x + cx, y + cy),
        (x + cx, -y + cy),
        (-x + cx, -y + cy),
        (y + cx,  x + cy),
        (-y + cx, x + cy),
        (y + cx, -x + cy),
        (-y + cx, -x + cy)
    ]

    for px, py in points:
        xs.append(px)
        ys.append(py)

def midpoint_circle(r, cx=0, cy=0):
    x = 0
    y = r
    p = 1 - r

    xs = []
    ys = []

    plot_points(cx, cy, x, y, xs, ys)

    while x < y:
        x = x + 1

        if p < 0:
            p = p + 2*x + 1
        else:
            y = y - 1
            p = p + 2*(x - y) + 1

        plot_points(cx, cy, x, y, xs, ys)

    return xs, ys

def draw_circle(r, cx=0, cy=0):
    xs, ys = midpoint_circle(r, cx, cy)

    plt.figure(figsize=(6, 6))
    plt.scatter(xs, ys, color='blue')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Midpoint Circle Algorithm")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

draw_circle(100000, 0, 0)