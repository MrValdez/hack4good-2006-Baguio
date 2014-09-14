import math
import pygame
import simulation
import random

pygame.init()
pygame.display.set_caption ("Greenhouse simulation")

clock = pygame.time.Clock()

simulation = simulation.Simulation()
mapImage = pygame.image.load("map.png")

resolution = [800, 600]
screen = pygame.display.set_mode(resolution)

    
isRunning = True
while isRunning:
    screen.fill([0, 0, 0])
    
    
    keypress = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keypress[pygame.K_ESCAPE] = True
    
    if keypress[pygame.K_ESCAPE]:
        isRunning = False
        pygame.quit()
        break
    
    cellWidth = 50
    cellHeight = 50
    simulationSize = (cellWidth * simulation.Width, cellHeight * simulation.Height)
    simulationSurface = pygame.Surface(simulationSize)     # http://stackoverflow.com/questions/17581545/drawn-surface-transparency-in-pygame
    colorKey = [127, 33, 33]
    simulationSurface.fill(colorKey)
    simulationSurface.set_colorkey(colorKey)
    simulationSurface.set_alpha(100)
    
    for cellNumber, cell in enumerate(simulation.Grid):
        x = cellNumber % simulation.Width
        y = math.trunc(cellNumber / simulation.Width)       #use floor?
        
        pixelX = x * cellWidth
        pixelY = y * cellHeight 
        pos = pygame.Rect((pixelX, pixelY), (cellWidth, cellHeight))
        
        if cell <= 0:
            color = pygame.Color(*colorKey)
        else:
            color = pygame.Color(int(255 * cell), int(190 * cell), 0)
        
        #color.a = 255
        pygame.draw.rect(simulationSurface, color, pos)
    
    simulationPos = [50, 50]
    mapImageScaled = pygame.transform.smoothscale(mapImage, simulationSize)
    screen.blit(mapImageScaled, simulationPos)
    
    screen.blit(simulationSurface, simulationPos)
    
    mousePos = pygame.mouse.get_pos()
    simulationRect = pygame.Rect(simulationPos, simulationSize)
    if simulationRect.collidepoint(mousePos):
        cellX = (mousePos[0] - simulationPos[0]) / cellWidth
        cellY = (mousePos[1] - simulationPos[1]) / cellHeight
        
        cellX = math.floor(cellX)
        cellY = math.floor(cellY)
    
        simulation.PlantTree(cellX, cellY)

    pygame.display.update()
    clock.tick(60)