import matplotlib.pyplot as plt

def plot_circle_points(xc, yc, x, y, xes, yes):
    pts = [
        ( x + xc,  y + yc),
        (-x + xc,  y + yc),
        ( x + xc, -y + yc),
        (-x + xc, -y + yc),
        ( y + xc,  x + yc),
        (-y + xc,  x + yc),
        ( y + xc, -x + yc),
        (-y + xc, -x + yc),
    ]
    for px, py in pts:
        xes.append(px)
        yes.append(py)

def midpoint_circle(r, xc=0, yc=0):
    x = 0
    y = r
    p = 1 - r

    xes, yes = [], []
    plot_circle_points(xc, yc, x, y, xes, yes)

    while x < y:
        x += 1
        if p < 0:
            p = p + 2*x + 1
        else:
            y -= 1
            p = p + 2*(x - y) + 1

        plot_circle_points(xc, yc, x, y, xes, yes)

    return xes, yes

def plot_midpoint_circle(r, xc=0, yc=0):
    xes, yes = midpoint_circle(r, xc, yc)
    plt.figure(figsize=(6,6))
    plt.scatter(xes, yes, marker='.', color='red')
    plt.title("Midpoint Circle Algorithm")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

plot_midpoint_circle(20, 0, 0)