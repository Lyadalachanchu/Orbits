import pygame
import sys
import math
import random


class Planet:
    def __init__(self, mass_planet, pos, vel, id, color=(255,255,255)):
        self.mass = mass_planet
        self.pos = pos
        self.deltaT = 1/60
        self.vel = vel
        self.id = id
        self.distances = []
        self.accelerations = []
        self.angles = []
        self.color = color

    def calculateDistance(self):
        self.distances = []
        for i in self.planets:
            self.distances.append(math.sqrt((i.pos[0]-self.pos[0])**2+(i.pos[1]-self.pos[1])**2))
            #print(self.distances)
        return self.distances

    def calculateAcceleration(self):
        self.accelerations = []
        for counter, i in enumerate(self.planets):
            self.accelerations.append(((1*i.mass)/(self.calculateDistance()[counter]**2)))
        return self.accelerations

    def calculateAngle(self):
        self.angles = []
        for counter, i in enumerate(self.planets):
            if(self.pos[0]>=i.pos[0] and self.pos[1] <=i.pos[1]):#top right
                #print("top right")
                self.angles.append((math.asin((i.pos[1]-self.pos[1])/self.calculateDistance()[counter])))
            elif(self.pos[0]<i.pos[0] and self.pos[1] <=i.pos[1]):#top left
                #print("top left")
                self.angles.append((math.asin((i.pos[0]-self.pos[0])/self.calculateDistance()[counter]))+(math.pi)/2)
            elif(self.pos[0]<i.pos[0] and self.pos[1] > i.pos[1]):#bottom left
                #print("bottom left")
                self.angles.append((math.asin((self.pos[1]-i.pos[1])/self.calculateDistance()[counter]))+(math.pi))
            elif(self.pos[0]>=i.pos[0] and self.pos[1]>i.pos[1]):#bottom right
                #print("bottom right")
                self.angles.append((math.asin((self.pos[0]-i.pos[0])/self.calculateDistance()[counter]))+(3*math.pi)/2)
        return self.angles;

    def xAcc(self):
        sum = 0
        for counter, i in enumerate(self.planets):
            sum += -self.calculateAcceleration()[counter]*math.cos(self.calculateAngle()[counter])
        return sum

    def yAcc(self):
        sum = 0
        for counter, i in enumerate(self.planets):
            sum+= self.calculateAcceleration()[counter]*math.sin(self.calculateAngle()[counter])
        return sum

    def changePos(self):
        self.vel[0] += self.xAcc()*self.deltaT
        self.vel[1] += self.yAcc()*self.deltaT      

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]


        return self.pos[0], self.pos[1]

    def setPlanets(self, planets):
        self.planets = list(planets)
        self.f = []
        for ind, x in enumerate(self.planets):
            if(x.id == self.id):
                self.planets.pop(ind)

class sim():
    def __init__(self, planets):
        self.planets = planets

    def run(self, fps, size):
        pygame.init()
        fpsClock = pygame.time.Clock()
        screen = pygame.display.set_mode((size, size))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)


        counter = 0
        startpos = (0,0)
        endpos = (0,0)
        start_time = 0
        end_time = 0
        while True:

            counter += 1
            screen.fill((0, 0, 0))


            ev = pygame.event.get()
    
            for event in ev:

                if event.type == pygame.MOUSEBUTTONDOWN:
                    startpos = list(pygame.mouse.get_pos())
                    start_time = pygame.time.get_ticks()

                if event.type == pygame.MOUSEBUTTONUP:
                    endpos = list(pygame.mouse.get_pos())
                    end_time = pygame.time.get_ticks()
                    xv = (endpos[0]-startpos[0])/(end_time-start_time)
                    yv = (endpos[1]-startpos[1])/(end_time-start_time)
                    self.planets.append(Planet(random.randint(500, 1000), endpos, [3*xv, 3*yv], counter))
            
                if event.type == pygame.QUIT:
                    pygame.quit()

            for planet in self.planets:
                planet.setPlanets(self.planets)
            for planet in self.planets:
                x, y = planet.changePos()


                out_of_bounds = False
                if (((x > size) or (x < 0)) or ((y > size) or (y < 0))):
                    out_of_bounds = True
                if out_of_bounds:
                    self.planets.remove(planet)
                pygame.draw.circle(screen, planet.color, ((int)(x), (int)(y)), 5)
            
            textsurface = myfont.render(str(len(self.planets)), False, (255, 255, 255))
            screen.blit(textsurface,(10,10))
            pygame.display.flip()
            fpsClock.tick(fps)
        