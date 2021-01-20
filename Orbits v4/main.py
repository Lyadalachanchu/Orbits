import pygame
import sys
from planet import Planet, sim
import math
import random

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))


###Change these parameters
sun_mass = 100000
planet_mass = 900

sun_pos = [(int)(width/2), (int)(width/2)]
sun_vel = [0, 0]
sun = Planet(sun_mass, sun_pos, sun_vel, 10, color=(255,255,0))
system = []
'''
system = [
		[[sun_pos[0]+300, sun_pos[1]], [0, 1]],
		[[sun_pos[0]-300, sun_pos[1]], [0, -1]]
]'''

planets = []
for p in range(len(system)):
	planets.append(Planet(random.randint(500, 1000), system[p][0], system[p][1], p))
planets.append(sun)
###end of parameters

system = sim(planets)
system.run(fps, height)

pygame.quit()