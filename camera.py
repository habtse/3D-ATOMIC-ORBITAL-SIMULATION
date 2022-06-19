import numpy as np


class Camera:

    def __init__(self):
        self.position = np.array([.0,0.0,3.0])
        self.target = np.array([0.0,0.0,0.0])
        self.up = np.array([0.0,1.0,0.0])
        # self.front = np.array([0.0,0.0,-1.0])
        self.theta = -90
        self.phi = 0
        self.update_camera()
    def update_camera(self):
        self.front = np.array(
            [
                np.cos(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.phi)),
                np.sin(np.deg2rad(self.theta)) * np.cos(np.deg2rad(self.phi))
                
            ],
            dtype = np.float32
        )