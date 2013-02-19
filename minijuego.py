# -*- coding: utf-8 -*-
'''
Created on 20/01/2012

    Shark Ball

@author: Alberto
'''
import pygame
import sys
from pygame.locals import *
from minijuegolib import *

pygame.init()
reloj = pygame.time.Clock()

# carga de ventana
visor = pygame.display.set_mode((ANCHO, ALTO))
icono = cargar_imagen("shark.ico", True)
pygame.display.set_caption('Shark Ball')
pygame.display.set_icon(icono)
pygame.mouse.set_visible(False)
fondo_juego = cargar_imagen( "fondo2.gif" )
visor.blit(fondo_juego, (0,0))

# carga de objetos
shark = Shark()
escenario = Escenario()

shark_grupo = pygame.sprite.RenderUpdates(shark)
marcador_vidas = pygame.sprite.RenderUpdates(Marcador_Vidas())
marcador_puntos = pygame.sprite.RenderUpdates(Marcador_Puntos())
decorado = pygame.sprite.RenderUpdates(Decorado(10), Decorado(570))
bola_grupo_roja = pygame.sprite.RenderUpdates(Bola(0))
bola_grupo_azul = pygame.sprite.RenderUpdates(Bola(1))
bola_grupo_verde = pygame.sprite.RenderUpdates(Bola(2))
bola_grupo_ambar = pygame.sprite.RenderUpdates(Bola(3))

# cargar pantalla inicial
escenario.draw(visor)
intervalo_bolas_rojas = 0
intervalo_bolas_azul = 0
intervalo_bolas_verde = 0
intervalo_bolas_ambar = 0

while True:
    # fps
    reloj.tick(60)
    
    # eventos
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == KEYDOWN:
            if evento.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if evento.key == K_f:
                visor = pygame.display.set_mode((ANCHO, ALTO), FULLSCREEN)
                visor.blit(fondo_juego, (0,0))
            
    # generación de bolas de colores
    intervalo_bolas_rojas += 1
    if intervalo_bolas_rojas >= 180:
        bola_grupo_roja.add(Bola(0))
        bola_grupo_roja.add(Bola(0))
        if shark.puntos >= 100:
            bola_grupo_roja.add(Bola(0))
        elif shark.puntos >= 175:
            bola_grupo_roja.add(Bola(0))
            bola_grupo_roja.add(Bola(0))
        elif shark.puntos >= 250:
            bola_grupo_roja.add(Bola(0))
        intervalo_bolas_rojas = 0
    
    intervalo_bolas_azul += 1
    if intervalo_bolas_azul >= 160:
        bola_grupo_azul.add(Bola(1))
        bola_grupo_azul.add(Bola(1))
        bola_grupo_azul.add(Bola(1))                                                                                
        if shark.puntos >= 100:
            bola_grupo_azul.add(Bola(0))
        intervalo_bolas_azul = 0
        
    intervalo_bolas_verde += 1
    if intervalo_bolas_verde >= 700:
        bola_grupo_verde.add(Bola(2))
        if shark.puntos >= 200:
            bola_grupo_verde.add(Bola(0))
        intervalo_bolas_verde = 0
        
    intervalo_bolas_ambar += 1
    if intervalo_bolas_ambar >= 1000:
        bola_grupo_ambar.add(Bola(3))
        if shark.vidas <= 3:
            bola_grupo_ambar.add(Bola(3)) 
        intervalo_bolas_ambar = 0
    
    # actualización de objetos
    shark_grupo.update()
    bola_grupo_roja.update()
    bola_grupo_azul.update()
    bola_grupo_verde.update()
    bola_grupo_ambar.update()
    marcador_vidas.update(visor, shark.vidas)
    marcador_puntos.update(visor, shark.puntos)
    decorado.update()
    
    # colisiones
    if pygame.sprite.groupcollide(shark_grupo, bola_grupo_azul, 0, 1):
        shark.puntos += random.randint(1, 2)
        shark.sonando = 20
        
    if pygame.sprite.groupcollide(shark_grupo, bola_grupo_roja, 0, 1):
        shark.vidas -= 1
        shark.muriendo = 25
        if shark.vidas == 0:
            escenario.update(visor, shark.puntos)
            shark.puntos = 0
            shark.vidas = 5
            shark.muriendo = 0
            intervalo_bolas_rojas = 0
            intervalo_bolas_azul = 0
            intervalo_bolas_verde = 0
            intervalo_bolas_ambar = 0
            escenario.draw(visor)
        
    if pygame.sprite.groupcollide(shark_grupo, bola_grupo_verde, 0, 1):
        shark.puntos += random.randint(10, 50)
        shark.sonando = 20
        
    if pygame.sprite.groupcollide(shark_grupo, bola_grupo_ambar, 0, 1):
        shark.vidas += 1
        shark.sonando = 20
            
    
    # limpiar pantalla
    shark_grupo.clear(visor, fondo_juego)
    bola_grupo_roja.clear(visor, fondo_juego)
    bola_grupo_azul.clear(visor, fondo_juego)
    bola_grupo_verde.clear(visor, fondo_juego)
    bola_grupo_ambar.clear(visor, fondo_juego)
    marcador_puntos.clear(visor, fondo_juego)
    marcador_vidas.clear(visor, fondo_juego)
    decorado.clear(visor, fondo_juego)
    
    # pintar pantalla
    shark_grupo.draw(visor)
    bola_grupo_roja.draw(visor)
    bola_grupo_azul.draw(visor)
    bola_grupo_verde.draw(visor)
    bola_grupo_ambar.draw(visor)
    marcador_puntos.draw(visor)
    marcador_vidas.draw(visor)
    decorado.draw(visor)
    
    pygame.display.update()
