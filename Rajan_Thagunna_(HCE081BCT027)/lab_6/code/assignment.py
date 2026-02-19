import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
cube = np.array([
    [0,0,0],[1,0,0],[1,1,0],[0,1,0],
    [0,0,1],[1,0,1],[1,1,1],[0,1,1]
])
roof = np.array([
    [0,0,1],[1,0,1],[1,1,1],[0,1,1],
    [0.5,0.5,1.7]
])
def rotate_x(points, angle):
    t = np.radians(angle)
    R = np.array([
        [1, 0, 0],
        [0, np.cos(t), -np.sin(t)],
        [0, np.sin(t),  np.cos(t)]
    ])
    return points @ R.T
def rotate_y(points, angle):
    t = np.radians(angle)
    R = np.array([
        [ np.cos(t), 0, np.sin(t)],
        [ 0, 1, 0],
        [-np.sin(t), 0, np.cos(t)]
    ])
    return points @ R.T
def rotate_z(points, angle):
    t = np.radians(angle)
    R = np.array([
        [np.cos(t), -np.sin(t), 0],
        [np.sin(t),  np.cos(t), 0],
        [0, 0, 1]
    ])
    return points @ R.T
def get_faces(cube_t, roof_t):
    cube_faces = [
        [cube_t[i] for i in [0,1,2,3]],
        [cube_t[i] for i in [4,5,6,7]],
        [cube_t[i] for i in [0,1,5,4]],
        [cube_t[i] for i in [2,3,7,6]],
        [cube_t[i] for i in [1,2,6,5]],
        [cube_t[i] for i in [0,3,7,4]]
    ]
    roof_faces = [
        [roof_t[i] for i in [0,1,4]],
        [roof_t[i] for i in [1,2,4]],
        [roof_t[i] for i in [2,3,4]],
        [roof_t[i] for i in [3,0,4]]
    ]
    return cube_faces, roof_faces
angle = 45
cube_x, roof_x = rotate_x(cube, angle), rotate_x(roof, angle)
cube_y, roof_y = rotate_y(cube, angle), rotate_y(roof, angle)
cube_z, roof_z = rotate_z(cube, angle), rotate_z(roof, angle)
fig = plt.figure(figsize=(15,5))
titles = ["Rotation about X-axis",
          "Rotation about Y-axis",
          "Rotation about Z-axis"]
models = [(cube_x, roof_x),
          (cube_y, roof_y),
          (cube_z, roof_z)]
for i, (cube_t, roof_t) in enumerate(models):
    ax = fig.add_subplot(1,3,i+1, projection='3d')
    cube_faces, roof_faces = get_faces(cube_t, roof_t)
    ax.add_collection3d(Poly3DCollection(cube_faces, alpha=0.5))
    ax.add_collection3d(Poly3DCollection(roof_faces, alpha=0.7))
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    ax.set_zlim(-2,2)
    ax.set_title(titles[i])
plt.show()