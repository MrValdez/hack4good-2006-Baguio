# http://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators
import locale
locale.setlocale(locale.LC_ALL,"")

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
font2 = pygame.font.SysFont("timesnewromans", 25)

Menu_PlantTree = font.render("Plant Trees", True, (255,255,255))
Mode = "Planting Mode"
Money = 1000

Year = 1984
CurrentYearPos = 0.0

CurrentPowerPos = [0.0, 0.0, 0.0]

simulation = simulation.Simulation()

mapImage = pygame.image.load("map.png")
#maxSimulationSize = [550, 500]
maxSimulationSize = [899, 555]
cellWidth = int(maxSimulationSize[0] / simulation.Width)
cellHeight = int(maxSimulationSize[1] / simulation.Height)
simulationSize = (cellWidth * simulation.Width, cellHeight * simulation.Height)
mapImageScaled = pygame.transform.smoothscale(mapImage, simulationSize)
simulation.setMapImage(mapImageScaled)

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
        
        if cell > 0.3:
            if cell > 1: cell = 1
            #color = pygame.Color(int(255 * cell), int(190 * cell), 0)
            color = pygame.Color(int(230 * cell), int(250 * cell), int(116 * cell))
                    
            #color.a = 255
            #pos = pygame.Rect((pixelX, pixelY), (cellWidth, cellHeight))
            #pygame.draw.rect(simulationSurface, color, pos)
            pos = (pixelX, pixelY)
            size = int(cellWidth * cell)
            pygame.draw.circle(simulationSurface, color, pos, random.randint(size + 3, size + 5))
        
    simulationPos = [30, 50]
    screen.blit(mapImageScaled, simulationPos)
    
    screen.blit(simulationSurface, simulationPos)

    for pos in treeList:
        screen.blit(treeImage, pos)

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
    if mouseClick[0] and \
        Mode == "Planting Mode" and \
        simulationRect.collidepoint(mousePos) and \
        Money > 0:
        cellX = (mousePos[0] - simulationPos[0]) / cellWidth
        cellY = (mousePos[1] - simulationPos[1]) / cellHeight
        
        cellX = math.floor(cellX)
        cellY = math.floor(cellY)
    
        simulation.PlantTree(cellX, cellY)
    
        size = treeImage.get_size()
        pos = [mousePos[0] - (size[0] / 2), mousePos[1] - (size[1] / 2)]
        treeList.append(pos)
        
        Money -= 1

    # menu
    MenuPos = [simulationPos[0] + maxSimulationSize[0] + size[0], simulationPos[1]]
    
    pygame.draw.rect(screen, pygame.Color(100, 128, 128), pygame.Rect(MenuPos, [300, maxSimulationSize[1]]))
    
    ButtonPlantingMode = pygame.Rect(MenuPos, [300, 73])
    if Mode == "Planting Mode":
        pygame.draw.rect(screen, pygame.Color(50, 20, 40), ButtonPlantingMode)
        
    TextPos = [MenuPos[0] + 70, MenuPos[1] + 20]
    screen.blit(Menu_PlantTree, TextPos)
    
    MenuPos[1] += 70
    
    pygame.draw.line(screen, [255, 255, 255], MenuPos, [MenuPos[0] + 298, MenuPos[1]])

    MenuPos[1] += 10
    TextPos = [MenuPos[0] + 20, MenuPos[1]]
    Menu_Tax = font.render("+           TAX            -", True, (255,255,255))
    screen.blit(Menu_Tax, TextPos)

    MenuPos[1] += 40
    pygame.draw.line(screen, [255, 255, 255], MenuPos, [MenuPos[0] + 298, MenuPos[1]])

    MenuPos[1] += 10
    TextPos = [MenuPos[0] + 20, MenuPos[1]]
    Menu_Tax = font2.render("Pass Business friendly bill", True, (255,255,255))
    MenuPos[1] -= 3
    
    ButtonPower1 = pygame.Rect(MenuPos, [300 * CurrentPowerPos[0], 24])
    pygame.draw.rect(screen, pygame.Color(0, 40, 228), ButtonPower1)
    screen.blit(Menu_Tax, TextPos)

    MenuPos[1] += 30
    pygame.draw.line(screen, [255, 255, 255], MenuPos, [MenuPos[0] + 298, MenuPos[1]])

    MenuPos[1] += 10
    TextPos = [MenuPos[0] + 20, MenuPos[1]]
    MenuPos[1] -= 3
    ButtonPower2 = pygame.Rect(MenuPos, [300 * CurrentPowerPos[1], 23])
    pygame.draw.rect(screen, pygame.Color(0, 40, 228), ButtonPower2)
    Menu_Tax = font2.render("Pass Tourism friendly bill", True, (255,255,255))
    screen.blit(Menu_Tax, TextPos)

    MenuPos[1] += 30
    pygame.draw.line(screen, [255, 255, 255], MenuPos, [MenuPos[0] + 298, MenuPos[1]])

    MenuPos[1] += 10
    TextPos = [MenuPos[0] + 20, MenuPos[1]]
    MenuPos[1] -= 4
    ButtonPower3 = pygame.Rect(MenuPos, [300 * CurrentPowerPos[2], 30])
    pygame.draw.rect(screen, pygame.Color(120, 255, 100), ButtonPower3)
    Menu_Tax = font2.render("Government Initiative: Green bill", True, (255,255,255))
    screen.blit(Menu_Tax, TextPos)

    MenuPos[1] += 30
    pygame.draw.line(screen, [255, 255, 255], MenuPos, [MenuPos[0] + 298, MenuPos[1]])

    MenuPos[1] += 190
    TextPos = [MenuPos[0] + 20, MenuPos[1]]
    Menu_Money = font.render("Treasury: %sm" % (str(locale.format("%d", Money, grouping=True))), True, (255,255,255))
    screen.blit(Menu_Money, TextPos)

    if mouseClick[0] and ButtonPower1.collidepoint(mousePos) and CurrentPowerPos[0] >= 1:
        Mode = "Power1"
        CurrentPowerPos[0] = 0
    if mouseClick[0] and ButtonPower2.collidepoint(mousePos) and CurrentPowerPos[1] >= 1:
        Mode = "Power2"
        CurrentPowerPos[1] = 0
    if mouseClick[0] and ButtonPower3.collidepoint(mousePos) and CurrentPowerPos[2] >= 1:
        Mode = "Power3"
        CurrentPowerPos[2] = 0
    if mouseClick[0] and ButtonPlantingMode.collidepoint(mousePos):
        Mode = "Planting Mode"

    MenuPos[1] += 70
    TextPos = [MenuPos[0] + 80, MenuPos[1] + 10]
    Menu_Year = font.render("Year %i" % (Year), True, (255,255,255))
    pygame.draw.rect(screen, pygame.Color(0, 40, 228), pygame.Rect(MenuPos, [300 * CurrentYearPos, 50]))
    screen.blit(Menu_Year, TextPos)

    if CurrentYearPos > 1:
        CurrentYearPos = 0
        Year += 1
        Money += random.randint(100,300)
        
    CurrentYearPos += 0.007
    
    CurrentPowerPos[0] += 0.002
    CurrentPowerPos[1] += 0.001
    CurrentPowerPos[2] += 0.0005

    for index, power in enumerate(CurrentPowerPos):
        if power > 1:
            CurrentPowerPos[index] = 1
        

    simulation.update(Year)
    pygame.display.update()
    clock.tick(60)