import pygame
from pygame.locals import *
from vector2D import Vector2D
from gameConstants import *
from random import randint


class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {UP:Vector2D(0, -1),DOWN:Vector2D(0, 1), 
                          LEFT:Vector2D(-1, 0), RIGHT:Vector2D(1, 0), STOP:Vector2D()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
       
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection
        self.setStartNode(node)
        self.image = None


    
    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()

    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True
    


    def setPosition(self):
        self.position = self.node.position.copy()
          

    def validDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False


    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node


    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False


    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        

    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False


    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16


    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)

  
    def validDirections(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)]



    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
         
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.directionMethod(directions)


            
               
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)
            
            self.setPosition()


    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) 


    


    