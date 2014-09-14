import random
import math

class Simulation:
    def __init__(self):
        self.Vehicle = 0.0       # by the thousands
        self.Population = 0.0    # by the thousands

        self.Width, self.Height = 50, 50
#        self.Width, self.Height = 200, 200
        self.Grid = [0] * self.Width * self.Height          # this is the pollution grid (todo: variable name will be refactored later)
        self.GridTree = [0] * self.Width * self.Height      # what position has trees

        self.PollutionSpeed = 10
        self.PollutionSpeedCurrent = 3

        self.maxPollution = 1.0

        self.PollutionDensity = 100     # 0 - 255. Affected by current date
        self.PollutionDensity = 180
                
    def update(self):
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
        self.UpdateFuzzyLimit()
        
    def UpdatePollution(self):           
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

    
    def UpdateTrees(self):
        for cellNumber, treeDensity in enumerate(self.GridTree):        
            # trees
            if treeDensity > 0:
                self.Grid[cellNumber] *= 1.0 - self.GridTree[cellNumber]

    def UpdateFuzzyLimit(self):
        for cellNumber, _ in enumerate(self.Grid):
            currentMinPollution = random.uniform(0, 0.3)
            #currentMinPollution = 0.1
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
        
