import numpy as np
import os
import time
from concurrent.futures import ThreadPoolExecutor

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from planet import Planet

def keyboard(key, x, y):
    print("exiting")
    if key == b'\x1b':
        os._exit(0)

class Universe:
    def __init__(self, size_scale, observable_width, observable_height):
        self.planets = np.array(
            [Planet(_id=k, mass=1, color=(255,255,255), x=0, y=0) for k in range(int(300*size_scale))]\
            +[Planet(_id=k, mass=2, color=(0,255,255), x=0, y=0) for k in range(int(300*size_scale), int(400*size_scale))]\
            +[Planet(_id=k, mass=5, color=(255,255,0), x=0, y=0) for k in range(int(400*size_scale), int(470*size_scale))]\
            +[Planet(_id=k, mass=10, color=(255,0,0), x=0, y=0) for k in range(int(470*size_scale), int(500*size_scale))]
        )
        self.observable_width = observable_width
        self.observable_height = observable_height

        self.universe = {}

    def fill_universe(self, planet):
        self.universe[(planet.x, planet.y)] = planet

    def draw(self):
        ms = time.time()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glBegin(GL_POINTS)
        for planet in self.planets:
            glColor3f(*planet.color)
            glVertex2f(planet.x, planet.y)
        glEnd()
        
        glutSwapBuffers()
        print(f"draw time = {time.time()-ms}")

    def update(self, value):
        ms = time.time()
        tmp_planets = np.array(list(self.planets))

        def update_planet(planet):
            planet.update(self.planets)
            self.fill_universe(planet)
            
        print(self.universe)
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(update_planet, planet) for planet in tmp_planets]
            for future in futures:
                future.result()

        print(f"update time = {time.time()-ms}")

        planets = tmp_planets
        
        glutPostRedisplay()
        glutTimerFunc(100, self.update, 0) 

    def big_bang(self):
        for planet in self.planets:
            planet.init_random_speed()
            self.fill_universe(planet)

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(self.observable_width, self.observable_height)
        glutCreateWindow(b"Particle System")
        
        glClearColor(0.0, 0.0, 0.0, 0.0)  # Black background
        glPointSize(1.0)  # Set point size to 1 pixel
        
        glutDisplayFunc(self.draw)
        glutTimerFunc(0, self.update, 0)
        glutKeyboardFunc(keyboard)
        glutMainLoop()


def main():
    universe = Universe(2.0, 1920, 1080)
    universe.big_bang()

if __name__ == "__main__":
    main()
