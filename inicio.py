import pygame
import ConfigParser
import random
import pygame
from pygame.locals import *
#Contantes globales

# Colores
NEGRO    = (   0,   0,   0)
BLANCO   = ( 255, 255, 255)
AZUL     = (   0,   0, 255)
ROJO     = ( 255,   0,   0)
VERDE    = (   0, 255,   0)

# Dimensiones pantalla
ANCHO = 800
ALTO  = 600

pygame.init()
pantalla = pygame.display.set_mode([ANCHO,ALTO])
def ini():

	fondom = pygame.image.load("title_box.png")
	fondo1 = pygame.transform.scale(fondom, (800, 600))  
	pantalla.blit(fondo1, (0, 0)) 
	

