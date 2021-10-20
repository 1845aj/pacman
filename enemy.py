from pygame.locals import *
from gameConstants import *
from entity import Entity
from random import randint

class Enemy(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = 3
        # self.points = 200

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