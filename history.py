import pygame
from pygame.locals import *

#metodo creado para poder visualizar la historia del jugador 
def Intro():
    salir=False
    screen = pygame.display.set_mode((800,600))
    fondo = pygame.image.load("historia.png")
    fondo1 = pygame.transform.scale(fondo, (800, 600))  

    while not salir:
        for e in pygame.event.get():
            if e.type == QUIT:
                import sys
                sys.exit(0)
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    
                    salir = True
            
        screen.blit(fondo1,(0,0))
        pygame.display.flip()
        pygame.time.delay(10)