import matplotlib.pyplot as plt

def plot_octa_symmetry(cx, cy, a, b, list_x, list_y):
    pts = [
        ( a + cx,  b + cy),
        (-a + cx,  b + cy),
        ( a + cx, -b + cy),
        (-a + cx, -b + cy),
        ( b + cx,  a + cy),
        (-b + cx,  a + cy),
        ( b + cx, -a + cy),
        (-b + cx, -a + cy)
    ]
    for px, py in pts:
        list_x.append(px)
        list_y.append(py)

def midpoint_circle(radius, center_x=0, center_y=0):
    a = 0
    b = radius
    decision = 1 - radius

    xs = []
    ys = []

    plot_octa_symmetry(center_x, center_y, a, b, xs, ys)

    while a < b:
        a += 1
        if decision < 0:
            decision += 2 * a + 1
        else:
            b -= 1
            decision += 2 * (a - b) + 1

        plot_octa_symmetry(center_x, center_y, a, b, xs, ys)

    return xs, ys

def draw_circle():
    radius = int(input("Enter radius: "))
    center_x = int(input("Enter center X: "))
    center_y = int(input("Enter center Y: "))

    xs, ys = midpoint_circle(radius, center_x, center_y)

    plt.figure(figsize=(5, 5))
    plt.scatter(xs, ys, s=5)
    plt.title("Midpoint Circle Algorithm")
    plt.axis("equal")
    plt.axis("off")
    plt.show()

draw_circle()