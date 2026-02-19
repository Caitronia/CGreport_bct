import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def scale(vertices, sx, sy, sz):
    S = np.array([
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, sz]
    ])
    return vertices @ S.T

def rotate_z(vertices, angle_deg):
    theta = np.radians(angle_deg)
    Rz = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])
    return vertices @ Rz.T

def translate(vertices, tx, ty, tz):
    return vertices + np.array([tx, ty, tz])

transformed = scale(vertices, 1.5, 0.5, 1)
transformed = rotate_z(transformed, 45)
transformed = translate(transformed, 2, 1, 0.5)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for edge in edges:
    pts = vertices[list(edge)]
    ax.plot(pts[:,0], pts[:,1], pts[:,2], color='black')

for edge in edges:
    pts = transformed[list(edge)]
    ax.plot(pts[:,0], pts[:,1], pts[:,2], color='olivedrab')

ax.set_box_aspect([1,1,1])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()