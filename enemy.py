from pygame.locals import *
from gameConstants import *
from entity import Entity
from random import randint
from modes import ModeController
from vector2D import Vector2D

class Enemy(Entity):
    def __init__(self, node, pacman=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2D()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)

    def randomDirection(self, directions):
            return directions[randint(0, len(directions)-1)]

    #? update() for enemy, similar to pacman but uses a rng to choose a direction
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
         
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.randomDirection(directions)   
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)
            self.setPosition()
    
    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2D()

    def chase(self):
        self.goal = self.pacman.position

    
    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]
