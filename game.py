import pygame
from pygame import mixer
from gameConstants import *
from pacman import Pacman
from nodes import Node, NodeGroup
import numpy as np
from pellets import PelletGroup
from enemy import *
from pause import Pause

#? This is the main game object. The game state is set up in the constructor.
#? Maze data is pulled from a text file and the map is build from that data
#? update() will refresh the entities and update the display

class Game:
    def __init__(self, screen):
        # UI Text
        self.UIFont = pygame.font.SysFont('Arial', 30)
        self.bigFont = pygame.font.SysFont('Arial Bold', 72)

        self.reset()


    def reset(self):
        self.isRunning = True
        self.gameOver = False
        self.gameLost = False

        

        self.background = None
        self.screen = pygame.display.set_mode((448, 560))
        self.clock = pygame.time.Clock()
        self.pause = Pause(True)
        
        self.wallImg = pygame.image.load("wall.png").convert()
        self.setBackground()
        self.data = self.readMazeData("mapDefault.txt")
        
        self.background = self.constructWalls(self.background)
        self.initialiseSounds()

        self.nodes = NodeGroup("mapDefault.txt")
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        self.pellets = PelletGroup("mapDefault.txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.enemy1.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.enemy2.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.enemy3.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.enemy4.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        spawnkey = self.nodes.constructKey(2+11.5, 3+14)
        self.ghosts.setSpawnNode(self.nodes.nodesLUT[spawnkey])
        self.sGameStart.play()
        #* Game Session Data
        self.level = 0
        self.lives = 2
        self.score = 0


    def restartGame(self):
        self.gameLost = True
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.reset()


    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None


    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.reset()


    def setBackground(self):
        self.background = pygame.surface.Surface((640,640)).convert()
        self.background.fill(BLACK)


    def update(self):
        dt = self.clock.tick(30) / 1000.0       
        self.pellets.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt)
            self.ghosts.update(dt)        
            self.checkPelletEvents()
            self.checkGhostEvents()
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

        
    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    ghost.reset()
                    ghost.visible = False
                    ghost.setSpeed(0)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -=  1
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.pause.setPause(pauseTime=1, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=1, func=self.resetLevel)


    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.showEntities()
                        else:
                            self.hideEntities()
                if event.key == K_r:
                    self.endGame()


    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.drawUI()
        if self.gameOver:
            self.drawWinScreen()
        elif self.gameLost:
            self.drawGameOverScreen()
        elif self.pause.paused:
            self.drawPauseScreen()

        pygame.display.update()


    def readMazeData(self, file):
        mapArr = np.loadtxt(file, dtype='<U1')
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
            self.score += 10
            if pellet.name == POWERPELLET:
                self.sFruit.play()
                self.score +=50
                self.ghosts.startFreight()
            else:
                self.sChomp.play()

            if self.pellets.isEmpty():
                self.gameOver = True
                self.hideEntities()
                self.drawWinScreen()
                self.pause.setPause(pauseTime=10, func=self.endGame)


    def initialiseSounds(self):
        self.sGameStart = mixer.Sound('sounds/soundGameStart.wav')
        self.sChomp = mixer.Sound('sounds/soundChomp.wav')
        self.sFruit = mixer.Sound('sounds/soundFruit.wav')


    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()


    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()


    def endGame(self):
        self.isRunning = False


    def drawUI(self):
        livesStr = "Lives: " + str(self.lives)
        livesText = self.UIFont.render(livesStr , True , (50,200,50))

        scoreStr = "Score: " + str(self.score)
        scoreText = self.UIFont.render(scoreStr , True , (50,200,50))

        self.screen.blit(scoreText, (0, 0))
        self.screen.blit(livesText, (200, 0))


    def drawWinScreen(self):
        winText = self.bigFont.render('You Win!' , True , (50,200,50))
        self.screen.blit(winText, (120, 250))
        subText = self.UIFont.render('Press the \'r\' key to return to menu.', True, (20,240,240))
        self.screen.blit(subText, (35, 300))


    def drawPauseScreen(self):
        pauseText = self.bigFont.render('PAUSED' , True , (50,200,50))
        pauseSubText = self.UIFont.render('\'SPACE\' key to continue!', True , (20,240,240))

        self.screen.blit(pauseText, (120, 250))
        self.screen.blit(pauseSubText, (90, 300))


    def drawGameOverScreen(self):
        mainText = self.bigFont.render('Game Over!' , True , (50,200,50))
        self.screen.blit(mainText, (120, 250))
        subtext = self.UIFont.render('\'SPACE\' key to continue!', True , (20,240,240))
        self.screen.blit(subtext, (35, 300))