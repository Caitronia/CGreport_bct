import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

vertices = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])

edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),   
    (0,4), (1,5), (2,6), (3,7)    
]


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for edge in edges:
    points = vertices[list(edge)]
    ax.plot(points[:,0], points[:,1], points[:,2], color='black')


ax.set_box_aspect([1,1,1])

# Label axes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()