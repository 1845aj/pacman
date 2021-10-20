import pygame
from pygame import mixer
from gameConstants import *
from pacman import Pacman
from enemy import Enemy
from nodes import Node, NodeGroup
import numpy as np
from pellets import PelletGroup

#? This is the main game object. The game state is set up in the constructor.
#? Maze data is pulled from a text file and the map is build from that data
#? update() will refresh the entities and update the display

class Game:
    def __init__(self, screen):
        self.background = None
        self.screen = pygame.display.set_mode((448, 560))
        self.clock = pygame.time.Clock()

        self.wallImg = pygame.image.load("wall.png").convert()
        self.data = self.readMazeData("mapDefault.txt")

        self.setBackground()
        self.background = self.constructWalls(self.background)
        self.initialiseSounds()

        self.nodes = NodeGroup("mapDefault.txt")
        self.nodes.setPortalPair((0,17), (27,17))
        self.pacman = Pacman(self.nodes.getStartTempNode())
        self.pellets = PelletGroup("mapDefault.txt")
        self.ghost = Enemy(self.nodes.getStartTempNode())
        
        self.sGameStart.play()
        


    def setBackground(self):
        self.background = pygame.surface.Surface((640,640)).convert()
        self.background.fill(BLACK)


    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.pellets.update(dt)
        self.ghost.update(dt)
        self.checkPelletEvents()
        self.checkEvents()
        self.render()


    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()


    def readMazeData(self, file):
        mapArr = np.loadtxt(file, dtype='<U1')
        print(mapArr)
        return mapArr


    def constructWalls(self, background):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col] == 'X':
                    sprite = self.wallImg
                    background.blit(sprite, (col*TILEHEIGHT, row*TILEWIDTH))

        return background

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)
            self.sChomp.play()

    
    def initialiseSounds(self):
        self.sGameStart = mixer.Sound('sounds/soundGameStart.wav')
        self.sChomp = mixer.Sound('sounds/soundChomp.wav')
        self.sFruit = mixer.Sound('sounds/soundFruit.wav')

    