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
    
    pygame.event.get()
    
    keypress = pygame.key.get_pressed()
    if keypress[pygame.K_ESCAPE]:
        isRunning = False
        pygame.quit()
        break
    
    cellWidth = 5
    cellHeight = 5
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
        
        #cell = x / simulation.Width
        cell = random.uniform(0, 1)
        color = pygame.Color(int(255 * cell), int(255 * cell), int(0 * cell))
        
        pygame.draw.rect(simulationSurface, color, pos)
    
    simulationPos = [50, 50]
    mapImageScaled = pygame.transform.smoothscale(mapImage, simulationSize)
    screen.blit(mapImageScaled, simulationPos)
    
    screen.blit(simulationSurface, simulationPos)
    
    pygame.display.update()
    clock.tick(60)