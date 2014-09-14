import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 30)   #initial window position
 
import math
import pygame
import simulation
import random

pygame.init()
pygame.display.set_caption ("Greenhouse simulation")

clock = pygame.time.Clock()
font = pygame.font.SysFont("timesnewromans", 40)

Menu_PlantTree = font.render("Plant Trees", True, (255,255,255))
Mode = "Planting Mode"

simulation = simulation.Simulation()
mapImage = pygame.image.load("map.png")
treeImage = pygame.image.load("tree.png")
treeImage = pygame.transform.smoothscale(treeImage, [15, 15])
treeImage.set_colorkey(treeImage.get_at([0,0]))

treeList = []

resolution = [1350, 700]
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
    
    #maxSimulationSize = [550, 500]
    maxSimulationSize = [899, 555]
    cellWidth = int(maxSimulationSize[0] / simulation.Width)
    cellHeight = int(maxSimulationSize[1] / simulation.Height)
    simulationSize = (cellWidth * simulation.Width, cellHeight * simulation.Height)
    simulationSurface = pygame.Surface(simulationSize)     # http://stackoverflow.com/questions/17581545/drawn-surface-transparency-in-pygame
    colorKey = [127, 33, 33]
    simulationSurface.fill(colorKey)
    simulationSurface.set_colorkey(colorKey)
    #simulationSurface.set_alpha(100)
    simulationSurface.set_alpha(simulation.PollutionDensity)
    
    for cellNumber, cell in enumerate(simulation.Grid):
        x = cellNumber % simulation.Width
        y = math.trunc(cellNumber / simulation.Width)       #use floor?
        
        pixelX = x * cellWidth
        pixelY = y * cellHeight 
        
        if cell >= 0.5:
            #color = pygame.Color(int(255 * cell), int(190 * cell), 0)
            color = pygame.Color(int(230 * cell), int(250 * cell), int(116 * cell))
                    
            #color.a = 255
            #pos = pygame.Rect((pixelX, pixelY), (cellWidth, cellHeight))
            #pygame.draw.rect(simulationSurface, color, pos)
            pos = (pixelX, pixelY)
            pygame.draw.circle(simulationSurface, color, pos, random.randint(cellWidth + 3, cellWidth + 8))
        
    simulationPos = [30, 50]
    mapImageScaled = pygame.transform.smoothscale(mapImage, simulationSize)
    screen.blit(mapImageScaled, simulationPos)
    
    screen.blit(simulationSurface, simulationPos)

    color = pygame.Color(255, 255, 255)
    pos = [simulationPos[0] + maxSimulationSize[0] - 70, simulationPos[1]]
    size = [20, maxSimulationSize[1] - 5]
    polutionDensityRect = pygame.Rect(pos, size)
    pygame.draw.rect(screen, color, polutionDensityRect)
    
    color = pygame.Color(255, 100, 130)
    #newHeight = sum(simulation.Grid) / ((simulation.Width + simulation.Height) / 2)
    size = [20, maxSimulationSize[1] - 5]
    newHeight = size[1] * (sum(simulation.Grid) / 3400)
    #if newHeight <= 200: 
    #    newHeight *= .2
    
    pos[1] = size[1] - newHeight + 52
    size[1] = newHeight
    polutionDensityRect = pygame.Rect(pos, size)
    pygame.draw.rect(screen, color, polutionDensityRect)
    
    mousePos = pygame.mouse.get_pos()
    mouseClick = pygame.mouse.get_pressed()
    
    # plant trees    
    simulationRect = pygame.Rect(simulationPos, simulationSize)
    if mouseClick[0] and Mode == "Planting Mode" and simulationRect.collidepoint(mousePos):
        cellX = (mousePos[0] - simulationPos[0]) / cellWidth
        cellY = (mousePos[1] - simulationPos[1]) / cellHeight
        
        cellX = math.floor(cellX)
        cellY = math.floor(cellY)
    
        simulation.PlantTree(cellX, cellY)
    
        size = treeImage.get_size()
        pos = [mousePos[0] - (size[0] / 2), mousePos[1] - (size[1] / 2)]
        treeList.append(pos)

    for pos in treeList:
        screen.blit(treeImage, pos)
    
    # menu
    MenuPos = [simulationPos[0] + maxSimulationSize[0] + size[0], simulationPos[1]]
    
    pygame.draw.rect(screen, pygame.Color(100, 128, 128), pygame.Rect(MenuPos, [300, maxSimulationSize[1]]))
    
    if Mode == "Planting Mode":
        pygame.draw.rect(screen, pygame.Color(50, 20, 40), pygame.Rect(MenuPos, [300, 73]))
        
    TextPos = [MenuPos[0] + 70, MenuPos[1] + 20]
    screen.blit(Menu_PlantTree, TextPos)
    
    MenuPos[1] += 70
    
    pygame.draw.line(screen, [255, 255, 255], MenuPos, [MenuPos[0] + 298, MenuPos[1]])

    simulation.update()
    pygame.display.update()
    clock.tick(60)