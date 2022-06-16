import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram,compileShader
import numpy as np
from s_loader import Mesh
import pyrr


class Cube:


    def __init__(self, position, eulers):

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
class App:
    def __init__(self):
        #initialise pygame
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((1200,900), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        #initialise opengl
        glClearColor(0.1, 0.2, 0.2, 1)
        
       
        # mesh
        self.mesh = Mesh('model/s_orbital.obj')
        print(self.mesh.vertex_count)
         # shader 
        self.program = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        
       
        # projection transform
        projection = pyrr.matrix44.create_perspective_projection(fovy = 45, aspect = 640/480, 
            near = 0.1, far =50000, dtype=np.float32)
        translate = pyrr.matrix44.create_from_translation(np.array([0, 0, -200], np.float32))
        identity = pyrr.matrix44.create_identity(dtype=np.float32)
        rotated = pyrr.matrix44.multiply(
            identity
        
            , pyrr.matrix44.create_from_x_rotation(theta=np.radians(45),dtype=np.float32,))
        translate = pyrr.matrix44.multiply(
            rotated, translate
        )
        glUseProgram(self.program)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'projection'),1,GL_FALSE,projection)
        glUniformMatrix4fv(glGetUniformLocation(self.program,'model'),1,GL_FALSE,translate)
        self.mainLoop()
    
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
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT)
            # glPointSize(10)
            # glLineWidth(5)

            glUseProgram(self.program)
            glBindVertexArray(self.mesh.vao)

            glDrawArrays(GL_TRIANGLES, 0, self.mesh.vertex_count)
            pg.display.flip()

            #timing
            self.clock.tick(60)
        self.quit()

App()