import numpy as np
import pygame
class VectorObject:
    key_to_function = {
    pygame.K_ESCAPE: (lambda x: x.terminate()),         # ESC key to quit
    pygame.K_SPACE:  (lambda x: x.pause())              # SPACE to pause
    }
    def __init__(self):
        self.position = np.array([0.0, 0.0, 0.0, 1.0])      # position
        self.angles = np.array([0.0, 0.0, 0.0])
        self.angleScale = (2.0 * np.pi) / 360.0             # to scale degrees. 
        self.rotationMatrix = np.zeros((3,3))
        self.rotateSpeed = np.array([0.0, 0.0, 0.0])
        self.nodes = np.zeros((0, 4))                       # nodes will have unrotated X,Y,Z coordinates plus a column of ones for position handling
        self.rotatedNodes = np.zeros((0, 3))                # rotatedNodes will have X,Y,Z coordinates after rotation ("final 3D coordinates")
        self.transNodes = np.zeros((0, 2))                  # transNodes will have X,Y coordinates

        
    def setPosition(self, position):
        # move object by giving it a rotated position.
        self.position = position 

    def setRotateSpeed(self, angles):
        # set object rotation speed.
        self.rotateSpeed = angles 

    def addNodes(self, node_array):
        # add nodes (all at once); add a column of ones for using position in transform
        self.nodes = np.hstack((node_array, np.ones((len(node_array), 1))))
        self.rotatedNodes = node_array # initialize rotatedNodes with nodes (no added ones required)

    def increaseAngles(self):
        self.angles += self.rotateSpeed
        for i in range(3):
            if self.angles[i] >= 360: self.angles[i] -= 360
            if self.angles[i] < 0: self.angles[i] += 360
   
    def setRotationMatrix(self):
        # Set matrix for rotation using angles
        
        (sx, sy, sz) = np.sin((self.angles) * self.angleScale)
        (cx, cy, cz) = np.cos((self.angles) * self.angleScale)
 
        # build a matrix for X, Y, Z rotation (in that order, see Wikipedia: Euler angles) including position shift. 
        # add a column of zeros for later position use
        self.rotationMatrix = np.array([[cy * cz               , -cy * sz              , sy      ],
                                        [cx * sz + cz * sx * sy, cx * cz - sx * sy * sz, -cy * sx],
                                        [sx * sz - cx * cz * sy, cz * sx + cx * sy * sz, cx * cy ]])

    def rotate(self):
        # Apply a rotation defined by a given rotation matrix.
        matrix = np.vstack((self.rotationMatrix, self.position[0:3]))   # add position to rotation matrix to move object at the same time
        self.rotatedNodes = np.dot(self.nodes, matrix)

    def transform(self, midScreen):
        # Add screen center.
        # add midScreen to center on screen to get to transNodes.
        self.transNodes = self.rotatedNodes[:, 0:2] + midScreen