from gameConstants import *
import pygame

class Config:
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


    def showUI(self, screen):
        self.screen = screen
        screen.fill(GREY1)
        self.drawTitle()
        self.drawFixedMapBtn()
        self.drawRandMapBtn()


    def buttonClicked(self, mouse):
        # if fixed clicked
        if self.fixedMapBtnYPos <= mouse[1] <= self.fixedMapBtnYPos+self.btnHeight and self.fixedMapBtnXPos <= mouse[0] <= self.fixedMapBtnXPos+self.btnWidth: 
            return 1
        # if rand clicked
        elif self.randMapBtnYPos <= mouse[1] <= self.randMapBtnYPos+self.btnHeight and self.randMapBtnXPos <= mouse[0] <= self.randMapBtnXPos+self.btnWidth:
            return 2
        else:
            return 0



    #? draw fixed
    def drawFixedMapBtn(self):
        fixedMapBtnText = self.menuFont.render('FIXED' , True , (255,255,255))
        self.fixedMapBtnXPos = self.xHalf - (self.btnWidth/2)
        self.fixedMapBtnYPos = self.yHalf

        # draw playBtn rectangle to screen
        pygame.draw.rect(self.screen, GREY3, [self.fixedMapBtnXPos, self.fixedMapBtnYPos, self.btnWidth, self.btnHeight])
            
        # draw playBtn text to screen
        self.screen.blit(fixedMapBtnText, (self.fixedMapBtnXPos+30, self.fixedMapBtnYPos))


    #? draw rand
    def drawRandMapBtn(self):
        randMapBtnText = self.menuFont.render('RAND' , True , (255,255,255))
        self.randMapBtnXPos = self.xHalf - (self.btnWidth/2)
        self.randMapBtnYPos = self.yHalf + (self.btnHeight + self.margin)*1

        # draw playBtn rectangle to screen
        pygame.draw.rect(self.screen, GREY3, [self.randMapBtnXPos, self.randMapBtnYPos, self.btnWidth, self.btnHeight])
            
        # draw playBtn text to screen
        self.screen.blit(randMapBtnText, (self.randMapBtnXPos+30, self.randMapBtnYPos))



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