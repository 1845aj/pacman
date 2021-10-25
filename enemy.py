from pygame.locals import *
from gameConstants import *
from entity import Entity
from random import randint
from modes import ModeController
from vector2D import Vector2D
from numpy import *
class Enemy(Entity):
    def __init__(self, node, pacman=None, enemy1=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2D()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.enemy1 = enemy1
        self.homeNode = node

    def randomDirection(self, directions):
            return directions[randint(0, len(directions)-1)]

    #? update() for enemy, similar to pacman but uses rng to choose a direction
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

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50)
            self.directionMethod = self.randomDirection         

    def normalMode(self):
        self.setSpeed(100)
        self.directionMethod = self.goalDirection

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection


class Enemy1(Enemy):
    def __init__(self, node, pacman=None, enemy1=None):
        Enemy.__init__(self, node, pacman, enemy1)
        self.name = ENEMY1
        self.color = RED

class Enemy2(Enemy):
    def __init__(self, node, pacman=None, enemy1=None):
        Enemy.__init__(self, node, pacman, enemy1)
        self.name = ENEMY2
        self.color = PINK

    def scatter(self):
        self.goal = Vector2D(TILEWIDTH*NCOLS, 0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

class Enemy3(Enemy):
    def __init__(self, node, pacman=None, enemy1=None):
        Enemy.__init__(self, node, pacman, enemy1)
        self.name = ENEMY3
        self.color = TEAL

    def scatter(self):
        self.goal = Vector2D(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.enemy1.position) * 2
        self.goal = self.enemy1.position + vec2

class Enemy4(Enemy):
    def __init__(self, node, pacman=None, enemy1=None):
        Enemy.__init__(self, node, pacman, enemy1)
        self.name = ENEMY4
        self.color = ORANGE

    def scatter(self):
        self.goal = Vector2D(0, TILEHEIGHT*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4



class GhostGroup(object):
    def __init__(self, node, pacman):
        self.enemy1 = Enemy1(node, pacman)
        self.enemy2 = Enemy2(node, pacman)
        self.enemy3 = Enemy3(node, pacman, self.enemy1)
        self.enemy4 = Enemy4(node, pacman)
        self.ghosts = [self.enemy1, self.enemy2, self.enemy3, self.enemy4]
        self.startNode = node

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def reset(self):
        for ghost in self:
            ghost.reset()

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()
    
    def setPosition(self):
        self.position = self.node.position.copy()

    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal
            distances.append(vec.magnitudeSquared())
        index = distances.index(min(distances))
        return directions[index]




