import random
import math

class Simulation:
    def __init__(self):
        self.Vehicle = 0.0       # by the thousands
        self.Population = 0.0    # by the thousands
        self.mapImage = None

        self.Width, self.Height = 50, 50
#        self.Width, self.Height = 200, 200
        self.Grid = [0] * self.Width * self.Height          # this is the pollution grid (todo: variable name will be refactored later)
        self.GridTree = [0] * self.Width * self.Height      # what position has trees

        self.PollutionSpeed = 10
        self.PollutionSpeedCurrent = 3

        self.maxPollution = 1.0

        self.PollutionDensity = 100     # 0 - 255. Affected by current date
        self.PollutionDensity = 180

    def setMapImage(self, mapImage):
        self.mapImage = mapImage
        
    def update(self, Year):
        """
        1. spread polution
        2. lower polution with trees
        """
        self.PollutionDensity = 100     # 0 - 255
        
        self.PollutionSpeedCurrent -= 1
        if self.PollutionSpeedCurrent < 0:
            self.PollutionSpeedCurrent = self.PollutionSpeed

            self.UpdatePollution()
            
        self.UpdateTrees()
        self.UpdateFuzzyLimit(Year)
        
    def UpdatePollution(self):           
        # spread pollution
        for cellNumber, polution in enumerate(self.Grid):  
            x = math.trunc(cellNumber / self.Width)
            y = cellNumber % self.Width

            if random.random() < 0.7:
                continue
                
            nDelta = 1.05
            eDelta = 1.05
            wDelta = 1.05
            sDelta = 1.05

            if x > 0 and y > 0 and x < self.Width - 1 and y < self.Height - 1:   # simplifies the math if we offset by 1 against edges                
                north = self.getIndex(x + 0, y - 1)
                south = self.getIndex(x + 0, y + 1)
                west = self.getIndex(x - 1, y + 0)
                east = self.getIndex(x + 1, y + 0)
                
                self.Grid[north] *= nDelta
                self.Grid[south] *= sDelta
                self.Grid[west] *= wDelta
                self.Grid[east] *= eDelta

        # add pollution
        if False:
            #broken!
            foo = self.mapImage.get_at([450, 52])
            
            width, height = self.mapImage.get_size()
            Found = False
            for y in range(0, height):
                Found = False
                for x in range(0, width):
                    pixel = self.mapImage.get_at([x, y])
                    pixel = [pixel[0], pixel[1], pixel[2]]
                        
    #                for red, green, blue in ([255, 225, 104], [255, 255, 255]):
                    #red, green, blue = [255, 255, 255]
                    red, green, blue = [240, 237, 229]
                    #print(pixel)
                    #print (red,pixel[0], green, pixel[1], blue, pixel[2])
                    #print(red == pixel[0], green == pixel[1], blue == pixel[2])
                    #if red == pixel[0] and green == pixel[1] and blue == pixel[2]:
                    if red != pixel[0] and green != pixel[1] and blue != pixel[2]:
                        pos = self.getIndex(x, y)
                        if pos >= len(self.Grid):
                            continue
                        self.Grid[pos] = 0.5
                        Found = True
                        continue
                            
                    if Found: break
                    
    def UpdateTrees(self):
        for cellNumber, treeDensity in enumerate(self.GridTree):        
            # trees
            if treeDensity > 0:
                self.Grid[cellNumber] *= 1.0 - self.GridTree[cellNumber]
                
                self.GridTree[cellNumber] *= 0.01

    def UpdateFuzzyLimit(self, Year):
        for cellNumber, _ in enumerate(self.Grid):
            if Year > 1986:         #todo: should be based on real data
                currentMinPollution = random.uniform(0, 0.2)
            elif Year > 1987:
                currentMinPollution = random.uniform(0, 0.3)
            else: 
                currentMinPollution = random.uniform(0, 0.1)
                
            currentMaxPollution = random.uniform(self.maxPollution - 0.15, self.maxPollution)
            
            if self.Grid[cellNumber] < currentMinPollution:
                self.Grid[cellNumber] = currentMinPollution
                
            if self.Grid[cellNumber] > currentMaxPollution:
                self.Grid[cellNumber] = currentMaxPollution 
                
    def getIndex(self, x, y):
        return (y * self.Width) + x
        
    def PlantTree(self, x, y):
        index = self.getIndex(x, y)
        treeAdded = 0.5

        self.GridTree[index] += treeAdded
        if self.GridTree[index] > 1.0:
            self.GridTree[index] = 1.0            

        north = self.getIndex(x + 0, y - 1)
        south = self.getIndex(x + 0, y + 1)
        west = self.getIndex(x - 1, y + 0)
        east = self.getIndex(x + 1, y + 0)
        
        treeAdded = 0.3
        self.GridTree[north] += treeAdded
        self.GridTree[south] += treeAdded
        self.GridTree[west] += treeAdded
        self.GridTree[east] += treeAdded

        northwest = self.getIndex(x - 1, y - 1)
        southwest = self.getIndex(x - 1, y + 1)
        northeast = self.getIndex(x + 1, y - 1)
        southeast = self.getIndex(x + 1, y + 1)
    
        treeAdded = 0.1
        self.GridTree[northwest] += treeAdded
        self.GridTree[southwest] += treeAdded
        self.GridTree[northeast] += treeAdded
        self.GridTree[northwest] += treeAdded
        
    def Tax(Change = +1):
        pass

    def Activate_VehicleLaws():
        """ 
        Pass harsh laws penalizing vehicles.
         Odd-Even Coding Scheme
         Private cars are taxed    
        """    
        pass

    def Activate_PrivateBusiness():
        """
        Incentivize private businesses to be put up
        """
        pass
        
    def Activate_GreenAwareness():
        """
        Increase public awareness of green.
        Slow to increase EXCEPT during catatrophe
        """
        pass
        
