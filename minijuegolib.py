# -*- coding: utf-8 -*-

'''
Created on 20/01/2012

@author: Alberto
'''
import pygame
from pygame.locals import *
import os
import sys
import time
import random
##############
# constantes #
##############
BLANCO = (255,255,255)
AZUL = (0,0,255)
ALTO = 480
ANCHO = 640
######################
# funciones de carga #
######################
def cargar_imagen(archivo, usarTransparencia = False):
    '''
    cargar_imagen(archivo) --> imagen
    Carga una imagen desde un archivo, devolviendo el objeto apropiado)
    '''
    lugar = os.path.join( "data", archivo )
    try:
        imagen = pygame.image.load(lugar)
    except pygame.error, mensaje:
        print "No puedo cargar la imagen:", lugar
        raise SystemExit, mensaje
    imagen = imagen.convert()
    if usarTransparencia:
        colorTransparente = imagen.get_at( (0,0) )
        imagen.set_colorkey( colorTransparente )
    return imagen

def cargar_fuente(archivo):
    '''
    cargar_fuente(archivo) --> fuente
    Carga una fuente desde un archivo, devolviendo el objeto apropiado)
    '''
    lugar = os.path.join( "data", archivo )
    return lugar

def cargar_sonido(archivo):
    '''
    cargar_sonido(archivo) --> devuelve objeto Sound
    '''
    class SinSonido:
        def play( self ):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return SinSonido()

    lugar = os.path.join( "data", archivo )

    try:
        sound = pygame.mixer.Sound( lugar )
    except pygame.error, message:
        print "No puedo cargar el sonido:", lugar
        raise SystemExit, message

    return sound
#####################
# objetos del juego #
#####################
class Bola(pygame.sprite.Sprite):
    '''
    Clase del objeto Bola
    '''
    def __init__(self, color):
        pygame.sprite.Sprite.__init__( self )
        if color == 0:
            self.image = cargar_imagen("roja.gif", True)
        elif color == 1:
            self.image = cargar_imagen("azul.gif", True)
        elif color == 2:
            self.image = cargar_imagen("verde.gif", True)
        elif color == 3:
            self.image = cargar_imagen("ambar.gif", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = 640
        self.rect.centery = random.randint(45, 470)
        self.dx = random.randint( -8, -3)
    def update(self):
        self.rect.move_ip( (self.dx, 0) )
        if self.rect.left < 0:
            self.kill()
        if self.rect.top < 0 or self.rect.bottom > ALTO:
            self.kill()
        
class Shark(pygame.sprite.Sprite):
    '''
    Clase del personaje principal, Shark
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.normal = cargar_imagen("shark.gif", True)
        self.comiendo = cargar_imagen("shark2.gif", True)
        self.toque =  cargar_sonido( "WaterDrop.wav" )
        self.image = self.normal
        self.muriendo = 0
        self.sonando = 0
        self.rect = self.image.get_rect()
        self.rect.left = -80
        self.rect.top = 45
        self.dy = 5
        self.dx = 24
        self.puntos = 0
        self.vidas = 5
    def update(self):
        self.muere()
        self.sonar()
        if self.muriendo == 0:
            self.image = self.normal
            teclas = pygame.key.get_pressed()
            if teclas[K_q]:
                self.rect.move_ip((0, -self.dy))
            if teclas[K_a]:
                self.rect.move_ip((0, self.dy))
            self.resize()
    def resize(self):
        if self.rect.top < 45:
            self.rect.top = 45
        elif self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
    def muere(self):
        self.toque.stop()
        if self.muriendo > 0:
            self.toque.play()
            self.image = self.comiendo
            self.muriendo -= 1
    def sonar(self):
        if self.sonando > 0:
            self.toque.play()
            self.sonando -= 1
            
                
class Marcador_Vidas(pygame.sprite.Sprite):
    '''
    Clase del marcador de vidas
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.fuente = cargar_fuente('UNISPACE.TTF')
        self.marcador = pygame.font.Font(self.fuente, 36)  
    def update(self, screen, vidas):
        self.image = self.marcador.render("Vidas: "+str(vidas), True, BLANCO)
        self.rect = (130,10,50,50)
        screen.blit(self.image, self.rect)
        pygame.display.update()
        
class Marcador_Puntos(pygame.sprite.Sprite):
    '''
    Clase del marcador de puntos
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.fuente = cargar_fuente('UNISPACE.TTF')
        self.marcador = pygame.font.Font(self.fuente, 36)  
    def update(self, screen, puntos):
        self.image = self.marcador.render("Puntos: "+str(puntos), True, BLANCO)
        self.rect = (320,10,50,50)
        screen.blit(self.image, self.rect)
        pygame.display.update()
        
class Decorado(pygame.sprite.Sprite):
    '''
    Clase del decorado del escenario
    '''
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.normal = cargar_imagen("cangrejo.gif", True)
        self.image = self.normal
        self.rect = self.image.get_rect()
        self.rect.left = pos
        self.rect.bottom = 45
        
class Escenario(object):
    '''
    Clase del escenario y menu principal
    '''
    def draw(self, screen):
        fondo = cargar_imagen('fondo1.gif')
        screen.blit(fondo, (0,0))
        self.fuente = cargar_fuente('UNISPACE.TTF')
        tipoLetra2 = pygame.font.Font(self.fuente, 28)
        mensaje2 = 'Pulsa cualquier para comenzar'
        texto2 = tipoLetra2.render(mensaje2, True, AZUL)
        screen.blit(texto2, (140,270,350,30))
        pygame.display.update()
        self.sonido_play = cargar_sonido('Jungle.wav')
        self.sonido_play.play(-1)
        esperar = True
        while esperar:
            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == KEYDOWN:
                    esperar = False
                                    
        fondo2 = cargar_imagen('fondo2.gif')
        screen.blit(fondo2, (0,0))
        
    def update(self, screen, puntos):
        fondo3 = cargar_imagen('fondo3.gif')
        screen.blit(fondo3, (0,0))
        mensaje = 'Puntos totales: '+ str(puntos)
        tipoLetra3 = pygame.font.Font(self.fuente, 48)
        texto = tipoLetra3.render(mensaje, True, AZUL)
        screen.blit(texto, (100,290,350,30))
        pygame.display.update()
        esperar = True
        while esperar:
            for evento in pygame.event.get():
                if evento.type == KEYDOWN:
                        esperar = False
        self.sonido_play.stop()