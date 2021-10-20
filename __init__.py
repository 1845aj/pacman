import pygame
from gameConstants import *
from menu import Menu
from game import Game



def main():
    # initialize pygame
    pygame.init()

    # set window title
    pygame.display.set_caption("Pacman")

    # create a surface
    screen = pygame.display.set_mode((480, 640))

    # create menu obj
    menu = Menu(screen=screen)

    running = True
    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if quit, exit the main loop
                running = False

            # onClick event handler
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()

                if menu.buttonClicked(mouse=mousePos) == 1:
                    print("exit pressed")
                    running = False
                if menu.buttonClicked(mouse=mousePos) == 2:
                    print("config pressed")
                if menu.buttonClicked(mouse=mousePos) == 3:
                    print("play pressed")

                    #* This is where the main game starts
                    # recreate a screen
                    screen = pygame.display.set_mode((640, 640))
                    # create game object
                    game = Game(screen=screen)
                    # dont actually need this but could use to return to menu?
                    gameRunning = True

                    #* Game loop
                    while gameRunning:
                        game.update()
              
            # refresh display
            pygame.display.update()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    main()
