
# Colors for disks
colors = [
    (255, 0, 0),      # Red
    (255, 165, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 128, 0),      # Green
    (0, 0, 255)       # Blue
]

# Class representing the hole system
class HanoiTower:

    disks = []
    towers = []
    historyOfMoves = []
    def __init__(self, numberOfDisks):
        self.numberOfDisks = numberOfDisks
        self.solved = False
        self.numberOfMoves = 0

        for i in range(3):
            self.towers.append( Tower ( i + 1 ) )
        
        for i in range(numberOfDisks):
            self.disks.append(Disk(i + 1, self.towers[0]))
        
        for i in range(numberOfDisks - 1, -1, -1):
            self.towers[0].insert(self.disks[i])
    
    def makeMove( self , disk , tower ):
        if self.disks[disk - 1].tower.towerNumber == tower:
            self.disks[disk - 1].tower.insert(self.disks[disk - 1])
            return 
        self.historyOfMoves.append( (self.disks[ disk - 1 ], self.disks[ disk - 1 ].tower ) )
        self.disks[ disk-1 ].moveTo( self.towers[ tower - 1 ], self.numberOfMoves)
        self.numberOfMoves += 1

        if tower == 3 and self.towers[tower-1].size == self.numberOfDisks:
            self.solved = True
            print(f"Congratulations! You solved the Hanoi Tower in {self.numberOfMoves} number of moves")
    
    # Function that solves the game
    def solve(self):
        # Undo all moves done
        while self.numberOfMoves != 0:
            self.undoMove()
        self.algorithm(self.numberOfDisks, 1, 3)

    # Recursive algorithm
    def algorithm(self, amountFromTop, originTowerNumber, destinyTowerNumber):
        # If there is only one disk to move then that disk is explicitly moved to that tower
        if amountFromTop == 1:
            print("Move disk {} located at tower {} to tower {}".format(self.towers[originTowerNumber - 1].topElement().diskSize,originTowerNumber, destinyTowerNumber))
            self.makeMove(self.towers[originTowerNumber - 1].topElement().diskSize, destinyTowerNumber)
            return
        self.algorithm(amountFromTop - 1, originTowerNumber, 6 - originTowerNumber - destinyTowerNumber)
        self.algorithm(1, originTowerNumber, destinyTowerNumber)
        self.algorithm(amountFromTop - 1, 6 - originTowerNumber - destinyTowerNumber, destinyTowerNumber)
        


    def undoMove(self):
        if self.numberOfMoves == 0:
            return
        disk, towerDestiny= self.historyOfMoves[-1]
        self.historyOfMoves.pop()
        disk.moveTo(towerDestiny)
        self.numberOfMoves -= 1
        
        

    def print_disks(self):
        for i in range(3):
            print("Disks in tower {}: ".format(i+1))
            for j in self.towers[i].stack:
                print(j.diskSize)
        print("end")


# Class representing a single tower
class Tower:

    def __init__(self, towerNumber):
        self.towerNumber = towerNumber
        self.stack = []
        self.size = 0
        self.width = 50
        self.height = 450
        self.color = (100, 42, 42) # Brown
        self.center = (160 + 300 * (towerNumber - 1) + self.width / 2,50 + self.height / 2)

    
    def insert(self, disk):
        disk.center = self.get_new_coordinates(disk)
        self.stack.append(disk)
        self.size += 1


    def topElement(self):
        if self.size == 0:
            return None
        
        return self.stack[-1]
    
    def removeElement(self):
        self.stack.pop()
        self.size -= 1

    def get_new_coordinates(self, disk):
        return (self.center[0], self.center[1] + self.height / 2 - 50 * self.size - disk.diskHeight/2)
    
    def get_tower_rect(self):
        return (self.center[0] - self.width /2, self.center[1] - self.height/2, self.width, self.height)
        


# Class representing a single disk
class Disk:
    def __init__(self, diskSize, tower_one):
        self.diskSize = diskSize
        self.tower = tower_one
        self.color = colors[diskSize - 1]
        self.center = (0,0)
        self.disksBelow = 0
        self.diskHeight = 50

    def moveTo(self, tower: Tower, numberOfMoves):
        topElementAtTower = tower.topElement()
        if topElementAtTower and topElementAtTower.diskSize < self.diskSize:
            raise Exception("Not a possible move")
        elif self.tower == tower:
            pass
        else:
            self.tower = tower
            tower.insert(self)
    
    def get_disk_rect(self):
        return (self.center[0] - self.diskSize * 50 / 2, self.center[1] - self.diskHeight / 2, self.diskSize * 50, self.diskHeight)



    
