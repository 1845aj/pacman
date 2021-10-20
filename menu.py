from gameConstants import *
import pygame

class Menu:
    def __init__(self, screen):
        # sizing variables (making sizing ez to change because im awful at UI design)
        self.xHalf = screen.get_width()/2
        self.yHalf = screen.get_height()/2
        self.btnHeight = 50
        self.btnWidth = 150
        self.margin = 5

        # fonts
        self.menuFont = pygame.font.SysFont('Arial',35)
        self.titleFont = pygame.font.SysFont('Arial', 60)
        self.subTitleFont = pygame.font.SysFont('Arial', 30)

        # initialize UI
        self.screen = screen
        screen.fill(GREY1)
        self.drawTitle()
        self.drawPlayBtn()
        self.drawConfBtn()
        self.drawExitBtn()
    

    def buttonClicked(self, mouse):
        # if exit clicked
        if self.exitBtnYPos <= mouse[1] <= self.exitBtnYPos+self.btnHeight and self.exitBtnXPos <= mouse[0] <= self.exitBtnXPos+self.btnWidth: 
            return 1
        # if config clicked
        elif self.confBtnYPos <= mouse[1] <= self.confBtnYPos+self.btnHeight and self.confBtnXPos <= mouse[0] <= self.confBtnXPos+self.btnWidth:
            return 2
        # if play clicked
        elif self.playBtnYPos <= mouse[1] <= self.playBtnYPos+self.btnHeight and self.playBtnXPos <= mouse[0] <= self.playBtnXPos+self.btnWidth:
            return 3
        # if blank space clicked
        else:
            return 0


    def drawPlayBtn(self):
        playBtnText = self.menuFont.render('PLAY' , True , (255,255,255))
        self.playBtnXPos = self.xHalf - (self.btnWidth/2)
        self.playBtnYPos = self.yHalf

        # draw playBtn rectangle to screen
        pygame.draw.rect(self.screen, GREY3, [self.playBtnXPos, self.playBtnYPos, self.btnWidth, self.btnHeight])
            
        # draw playBtn text to screen
        self.screen.blit(playBtnText, (self.playBtnXPos+30, self.playBtnYPos))


    def drawConfBtn(self):
        confBtnText = self.menuFont.render('CONF' , True , (255,255,255))
        self.confBtnXPos = self.xHalf - (self.btnWidth/2)
        self.confBtnYPos = self.yHalf + (self.btnHeight + self.margin)*1

        # draw playBtn rectangle to screen
        pygame.draw.rect(self.screen, GREY3, [self.confBtnXPos, self.confBtnYPos, self.btnWidth, self.btnHeight])
            
        # draw playBtn text to screen
        self.screen.blit(confBtnText, (self.confBtnXPos+30, self.confBtnYPos))


    def drawExitBtn(self):
        exitBtnText = self.menuFont.render('EXIT' , True , (255,255,255))
        self.exitBtnXPos = self.xHalf - (self.btnWidth/2)
        self.exitBtnYPos = self.yHalf + (self.btnHeight + self.margin)*2

        # draw exitBtn rectangle to screen
        pygame.draw.rect(self.screen, GREY3, [self.exitBtnXPos, self.exitBtnYPos, self.btnWidth, self.btnHeight])
            
        # draw exitBtn text to screen
        self.screen.blit(exitBtnText, (self.exitBtnXPos+30, self.exitBtnYPos))


    def drawTitle(self):
        # draw logo to screen
        pygame.draw.circle(self.screen, YELLOW, [150, 80], 40)

        # draw title to screen
        titleText = self.titleFont.render('Pacman' , True , (255,255,255))
        self.screen.blit(titleText, (200, 50))

        # draw course code to screen
        courseText = self.subTitleFont.render('2805ICT' , True , (255,255,255))
        self.screen.blit(courseText, (200, 155))

        # draw names to screen
        name1 = self.subTitleFont.render('Michael Fradley' , True , (255,255,255))
        name2 = self.subTitleFont.render('Brad Lyons' , True , (255,255,255))
        name3 = self.subTitleFont.render('Jeffery Neuffer' , True , (255,255,255))
        name4 = self.subTitleFont.render('Ashan Jayatillaka' , True , (255,255,255))

        self.screen.blit(name1, (60, 200))
        self.screen.blit(name2, (260, 200))
        self.screen.blit(name3, (60, 230))
        self.screen.blit(name4, (260, 230))

    
    def getConfig():
        pass