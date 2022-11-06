import pygame
import numpy as np
from vector_object import VectorObject
class RenderVector:
    # Displays 3D vector objects on a Pygame screen

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width,height))
        self.fullScreen = False
        pygame.display.set_caption('VectorViewer')
        self.backgroundColor = (0,0,0)
        self.VectorObjs = []
        self.midScreen = np.array([width / 2, height / 2], dtype=float)
        self.target_fps = 60                            # affects movement speeds
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()
            
    def addVectorObj(self, VectorObj):
        self.VectorObjs.append(VectorObj)

    def run(self):
    # Main loop.
        vobj = VectorObject()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in vobj.key_to_function:
                        vobj.key_to_function[event.key](self)
            
            if self.paused == True:
                pygame.time.wait(100)
            
            else:
                # main components executed here
                self.rotate()
                self.display()
                
                # release any locks on screen
                while self.screen.get_locked():
                    self.screen.unlock()
                    
                # switch between currently showed and the next screen (prepared in "buffer")
                pygame.display.flip()
                self.clock.tick(self.target_fps) # this keeps code running at max target_fps

            # exit; close display, stop
    def rotate(self):
        # Rotate all objects. First calculate rotation matrix.
        # Then apply the relevant rotation matrix with object position to each VectorObject.
     
                
        # rotate and flatten (transform) objects
        for VectorObj in self.VectorObjs:
            VectorObj.increaseAngles()
            VectorObj.setRotationMatrix()
            VectorObj.rotate()
            VectorObj.transform(self.midScreen)
    def display(self):
        # Draw the VectorObjs on the screen. 

        # lock screen for pixel operations
        self.screen.lock()

        # clear screen.
        self.screen.fill(self.backgroundColor)
                   
        # draw the actual objects
        for VectorObj in self.VectorObjs:       
            for node in VectorObj.transNodes:
                # for each node, draw a small circle (radius = 5) in white (255,255,255)
                node_int = (int(node[0]), int(node[1]))
                pygame.draw.circle(self.screen, (255,255,255), node_int, 5)
            # just for testing purposes - assuming a cube with specific node order, draw edges
            if np.shape(VectorObj.transNodes)[0] == 8:
                pygame.draw.aalines(self.screen, (255,255,255), 1, VectorObj.transNodes[0:4,:])
                pygame.draw.aalines(self.screen, (255,255,255), 1, VectorObj.transNodes[4:8,:])
                for i in range(4):
                    pygame.draw.aaline(self.screen, (255,255,255), VectorObj.transNodes[i,:], VectorObj.transNodes[i+4,:])
        
        # unlock screen
        self.screen.unlock()
 
def terminate(self):

    self.running = False   

def pause(self):

    if self.paused == True:
        self.paused = False
    else:
        self.paused = True

if __name__ == '__main__':
    """ 
    Prepare screen, objects etc.
    """

    # set screen size
    # first check available full screen modes
    pygame.display.init()
    # disp_modes = pygame.display.list_modes(0, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    # disp_size = disp_modes[4] # selecting display size from available list. Assuming the 5th element is nice...
    disp_size = (1280, 800)

    rv = RenderVector(disp_size[0], disp_size[1])

    # set up a simple cube
    vobj = VectorObject()
    node_array = np.array([
            [ 100.0, 100.0, 100.0],
            [ 100.0, 100.0,-100.0],
            [ 100.0,-100.0,-100.0],
            [ 100.0,-100.0, 100.0],
            [-100.0, 100.0, 100.0],
            [-100.0, 100.0,-100.0],
            [-100.0,-100.0,-100.0],
            [-100.0,-100.0, 100.0]
            ])
    vobj.addNodes(node_array)
    speed_angles = np.array([1.0, -.3, 0.55])
    vobj.setRotateSpeed(speed_angles)
    position = np.array([0.0, 0.0, 1500.0, 1.0])
    vobj.setPosition(position)
 
    # add the object
    rv.addVectorObj(vobj)
     
    # run the main program
    rv.run()