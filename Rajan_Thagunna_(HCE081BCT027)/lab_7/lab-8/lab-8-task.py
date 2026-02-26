import matplotlib.pyplot as plt

plt.figure()


plt.plot(2, 8, 'ro')  
plt.text(2, 8, " Point (2,8)")

x_line = [1, 6]
y_line = [1, 4]
plt.plot(x_line, y_line, 'b-', linewidth=2)
plt.text(3.5, 2.5, " Line")


x_triangle = [7, 9, 8, 7]
y_triangle = [1, 1, 4, 1]
plt.plot(x_triangle, y_triangle, 'g-', linewidth=2)
plt.text(8, 4.2, " Triangle")


x_polygon = [3, 5, 6, 4.5, 2.5, 3]
y_polygon = [5, 6, 8, 9, 7, 5]
plt.plot(x_polygon, y_polygon, 'm-', linewidth=2)
plt.text(4.5, 9.3, " Polygon")

plt.xlim(0, 12)
plt.ylim(0, 12)
plt.gca().set_aspect('equal')
plt.grid(True)
plt.title("Fundamental Shapes in Computer Graphics")
plt.show()