import pygame
import sys
from grid import Grid

# Set game

pygame.init()
pygame.font.init()


dark_blue = (44, 44, 127)
game_screen = Grid(3)

screen = pygame.display.set_mode((game_screen.width, game_screen.height))
pygame.display.set_caption("Hanoi Towers")

clock = pygame.time.Clock()

# At each iteration we perform three key steps
# * Checking for events
# * Updating position of game objects
# * Drawing game objects in new positions

over_disk = False
has_object_grabed = False
disk_grabed = None
won = False
while True:
    # Checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        font = pygame.font.SysFont('Arial', 30)
    if game_screen.HanoiTower.solved:
        game_screen.draw(screen)
        txtsurf = font.render("Challenge completed!", False, (255,255,255))
        screen.blit(txtsurf,(300, 50))

    txtsurf = font.render(f"Moves: {game_screen.HanoiTower.numberOfMoves}", False, (255,255,255))
    screen.blit(txtsurf,(840, 50))
    pygame.display.update()
    # Getting mouse coordinates
    xCoord, yCoord = pygame.mouse.get_pos()


    if has_object_grabed and not game_screen.HanoiTower.solved:
        over_disk = True

        # Set coordinates of grabed disk equal to mouse coordinates
        disk_grabed.center = (xCoord, yCoord)

        if not any(pygame.mouse.get_pressed()):
            has_object_grabed = False

            # Check if disk can be placed where mouse was released
            over_tower, destiny_tower = game_screen.over_tower(xCoord, yCoord)
            if over_tower:
                try:
                   game_screen.HanoiTower.makeMove(disk_grabed.diskSize, destiny_tower.towerNumber)
                except Exception as error:
                    print("error ", error)
                    disk_grabed.tower.insert(disk_grabed)
            else:
                print(disk_grabed.tower.towerNumber)
                disk_grabed.tower.insert(disk_grabed)

    elif not game_screen.HanoiTower.solved:
        over_disk = game_screen.over_disk(xCoord, yCoord)
        if any(pygame.mouse.get_pressed()) and over_disk:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            has_object_grabed = True
            disk_grabed = game_screen.get_grabed_disk(xCoord,yCoord)
            disk_grabed.tower.removeElement()


    

    if over_disk:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    # Drawing
    screen.fill(dark_blue)
    game_screen.draw(screen)
    
    clock.tick(60) # All code inside loop will run 60 times per second
