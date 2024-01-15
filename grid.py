from algorithm import HanoiTower
from algorithm import Tower
import pygame

class Grid:

    def __init__(self, towers):
        self.HanoiTower = HanoiTower(towers)
        self.disks = self.HanoiTower.disks
        self.towers = self.HanoiTower.towers 
        self.tower_specs = Tower(2)
        self.width = 1000
        self.height = 600
    
    def draw(self, screen):
        for tower in self.towers:
            tower_rect = pygame.Rect(tower.get_tower_rect())
            pygame.draw.rect(screen, self.tower_specs.color, tower_rect)
        
        for disk in self.disks:
            disk_rect = pygame.Rect(disk.get_disk_rect())
            pygame.draw.rect(screen, disk.color, disk_rect)
    
    def over_disk(self, xCoord, yCoord):
        for tower in self.towers:
            top_disk = tower.topElement()
            if not top_disk:
                continue
            if self.cursor_inside_rect(xCoord, yCoord, top_disk.center[0] - top_disk.diskSize * 50 /2, top_disk.center[1] - top_disk.diskHeight /2,
                                        top_disk.center[0] + top_disk.diskSize * 50 /2, top_disk.center[1] + top_disk.diskHeight /2):
                return True
        return False
    
    def cursor_inside_rect(self, x, y, x1, y1, x2, y2):
        return x >= x1 and x <= x2 and y >= y1 and y <= y2
    
    def get_grabed_disk(self, xCoord, yCoord):
        for tower in self.towers:
            top_disk = tower.topElement()
            if not top_disk:
                continue
            # Send coordinates of top left corner and right lower corner
            if self.cursor_inside_rect(xCoord, yCoord, top_disk.center[0] - top_disk.diskSize * 50 /2, top_disk.center[1] - top_disk.diskHeight /2,
                                        top_disk.center[0] + top_disk.diskSize * 50 /2, top_disk.center[1] + top_disk.diskHeight /2):
                return top_disk
            
    def over_tower(self, xCoord, yCoord):
        for tower in self.towers:
            if self.cursor_inside_rect(xCoord, yCoord, tower.center[0] - tower.width /2, tower.center[1] - tower.height /2,
                                        tower.center[0] + tower.width /2, tower.center[1] + tower.height /2):
                return True, tower
        return  False, None
