import matplotlib.pyplot as plt

def bresenham_line(x_start, y_start, x_end, y_end):
    x_points, y_points = [], []
    
    delta_x = abs(x_end - x_start)
    delta_y = abs(y_end - y_start)
    
    step_x = 1 if x_end >= x_start else -1
    step_y = 1 if y_end >= y_start else -1
    
    x, y = x_start, y_start

    if delta_x >= delta_y:
        decision_param = 2 * delta_y - delta_x
        for _ in range(delta_x + 1):
            x_points.append(x)
            y_points.append(y)
            x += step_x
            if decision_param >= 0:
                y += step_y
                decision_param += 2 * delta_y - 2 * delta_x
            else:
                decision_param += 2 * delta_y
    else:
        decision_param = 2 * delta_x - delta_y
        for _ in range(delta_y + 1):
            x_points.append(x)
            y_points.append(y)
            y += step_y
            if decision_param >= 0:
                x += step_x
                decision_param += 2 * delta_x - 2 * delta_y
            else:
                decision_param += 2 * delta_x

    return x_points, y_points

def plot_bresenham(x_start, y_start, x_end, y_end):
    x_points, y_points = bresenham_line(x_start, y_start, x_end, y_end)
    
    plt.figure(figsize=(6, 6))
    plt.plot(x_points, y_points, marker='o', linestyle='-')
    plt.title("Bresenham Line Drawing Algorithm")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

# Example usage
plot_bresenham(2, 3, 20, 15)
