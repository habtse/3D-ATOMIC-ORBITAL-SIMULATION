import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
from objLoader import Mesh
import pyrr
import math
from camera import Camera


        
class Model:


    def __init__(self, position, eulers):

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
class Scene:
    def __init__(self,):
        self.model = Model([0,0,0],[0,0,0])
        self.camera = Camera()
    def spin(self,dTheta,dPhi):
        self.camera.theta += dTheta
        if self.camera.theta > 360:
            self.camera.theta -= 360
        elif self.camera.theta < 0:
            self.camera.theta += 360
        
        self.camera.phi = min(
            89, max(-89, self.camera.phi + dPhi)
        )
        self.camera.update_camera()
        
class App:
    def __init__(self,index):
        #initialise pygame
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        self.screenWidth , self.screenHeight =(1200,900)
        pg.display.set_mode((self.screenWidth , self.screenHeight), pg.OPENGL|pg.DOUBLEBUF)
        
        self.clock = pg.time.Clock()
        #initialise opengl
        glClearColor(0.0, 0.0, 0.0, 1)
        
        list_of_func = ["s_orbital", "px_orbital",  "py_orbital","pz_orbital", "dzx_orbital","dz2_orbital", "dyz_orbital", "dxy_orbital",  "dx2-y2_orbital", "f1_orbital", "f2_orbital", "f3_orbital", "f4_orbital", "f5_orbital","f6_orbital", "f7_orbital",]
        selected = list_of_func[index]
        # mesh
        self.mesh = Mesh("models/"+selected+".obj")
         # shader 
        self.program = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        
       
        # projection transform
        
        
        self.camera = Camera()
        
                
        self.angles = [0,0,0]
        
        # self.mainLoop()
    
    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader
    
    def mainLoop(self):
        running = True
        while (running):
            #check events
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
            
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)
            # glDepthTest()
            # glPointSize(10)
            # glLineWidth(5)
            
            self.handleKeys()
            
            projection = pyrr.matrix44.create_perspective_projection(fovy = 45, aspect = 640/480, 
            near = 0.1, far =50000, dtype
            =np.float32)
        
            glUseProgram(self.program)
            glUniformMatrix4fv(glGetUniformLocation(self.program,'projection'),1,GL_FALSE,projection)
                
            translate = pyrr.matrix44.create_from_translation(np.array([0, 0,-200], np.float32))
            
            
            identity = pyrr.matrix44.create_identity(dtype=np.float32)
            rotated = pyrr.matrix44.multiply(
                identity
            
                , pyrr.matrix44.create_from_z_rotation(theta=np.radians(self.angles[2]) ,dtype=np.float32,))
            rotated = pyrr.matrix44.multiply(
                rotated,
            
                    pyrr.matrix44.create_from_y_rotation(theta=np.radians(self.angles[1]) ,dtype=np.float32,))
            rotated = pyrr.matrix44.multiply(
                rotated,
            
                    pyrr.matrix44.create_from_x_rotation(theta=np.radians(self.angles[0]) ,dtype=np.float32,))
            translate = pyrr.matrix44.multiply(
                rotated, translate
            )
            glUniformMatrix4fv(glGetUniformLocation(self.program,'model'),1,GL_FALSE,translate)
            view = pyrr.matrix44.create_look_at(self.camera.position, self.camera.target, self.camera.up)
            glUniformMatrix4fv(glGetUniformLocation(self.program,'view'),1,GL_FALSE,view)
                
            glUseProgram(self.program)
            glBindVertexArray(self.mesh.vao)

            glDrawArrays(GL_TRIANGLES, 0, self.mesh.vertex_count)
            pg.display.flip()

            #timing
            self.clock.tick(60)
            pg.display.flip()
        self.quit()
    def length(self,v):
        return math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])
    def normalize(self,v):
        l = self.length(v)
        return [v[0]/l, v[1]/l, v[2]/l]    
    def handleKeys(self,):
        

        keys = pg.key.get_pressed()
        cameraSpeed = 1

        if keys[pg.K_w]:
            
            self.camera.position  += (cameraSpeed*3) * self.camera.front
        if keys[pg.K_a]:
            
            front =  self.normalize(self.camera.front)
            up =  self.normalize(self.camera.up)
            cross = np.cross(front, up)
            self.camera.position -= (cameraSpeed )* cross
        if keys[pg.K_s]:
            self.camera.position  -= (cameraSpeed *3)* self.camera.front
        if keys[pg.K_d]:
            front =  self.normalize(self.camera.front)
            up =  self.normalize(self.camera.up)
            cross = np.cross(front, up)
            self.camera.position += (cameraSpeed) * cross
        if keys[pg.K_DOWN]:
            self.angles[0] -=   1
            
        if keys[pg.K_UP]:
            self.angles[0] +=   1
        if keys[pg.K_LEFT]:
            self.angles[1] -=   1
        if keys[pg.K_RIGHT]:
            self.angles[1] +=   1
        
    def handleMouse(self,):

        (x,y) = pg.mouse.get_pos()
        theta_increment =  0.05 * ((self.screenWidth // 2) - x)
        phi_increment =  0.05 * ((self.screenHeight // 2) - y)
        Scene().spin(theta_increment, phi_increment)
        pg.mouse.set_pos((self.screenWidth // 2,self.screenHeight // 2))
