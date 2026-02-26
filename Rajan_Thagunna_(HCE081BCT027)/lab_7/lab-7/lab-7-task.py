import matplotlib.pyplot as plt

xmin, xmax = 2, 8
ymin, ymax = 2, 6


def liang_barsky(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    p = [-dx, dx, -dy, dy]
    q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]

    u1 = 0.0
    u2 = 1.0

    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return None  
        else:
            u = q[i] / p[i]
            if p[i] < 0:
                u1 = max(u1, u)
            else:
                u2 = min(u2, u)

    if u1 > u2:
        return None

    cx1 = x1 + u1 * dx
    cy1 = y1 + u1 * dy
    cx2 = x1 + u2 * dx
    cy2 = y1 + u2 * dy

    return cx1, cy1, cx2, cy2


def draw_window():
    plt.plot([xmin, xmax, xmax, xmin, xmin],
             [ymin, ymin, ymax, ymax, ymin],
             'b-', linewidth=2)
    plt.xlim(0, 12)
    plt.ylim(0, 10)
    plt.gca().set_aspect('equal')
    plt.grid(True)


def draw_line_case(x1, y1, x2, y2, title):
    plt.figure()
    draw_window()

    result = liang_barsky(x1, y1, x2, y2)

    plt.plot([x1, x2], [y1, y2], 'r--', linewidth=2, label="Outside Part")

    if result:
        cx1, cy1, cx2, cy2 = result

        plt.plot([cx1, cx2], [cy1, cy2],
                 'g-', linewidth=3, label="Clipped (Visible) Part")

        print(f"\n{title}")
        print("Clipped Line Coordinates:")
        print(f"({cx1:.2f}, {cy1:.2f}) to ({cx2:.2f}, {cy2:.2f})")

    else:
        print(f"\n{title}")
        print("Line Completely Outside (Rejected)")

    plt.title(title)
    plt.legend()
    plt.show()



draw_line_case(3, 3, 7, 5, "1) Completely Inside")
draw_line_case(9, 7, 11, 9, "2) Completely Outside")
draw_line_case(1, 4, 4, 4, "3) Partial Inside (One Intersection)")
draw_line_case(1, 3, 9, 5, "4) Partial Inside (Two Intersections)")