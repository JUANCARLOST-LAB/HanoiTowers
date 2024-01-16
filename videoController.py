import mediapipe as mp
import cv2
import numpy as np
import os
import pygame
import sys
from grid import Grid

# Set up
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Video Capture
cap = cv2.VideoCapture(0)

def hand_closed(landmark_coordinates, mp_hands) -> bool:
    wrist = landmark_coordinates.landmark[mp_hands.HandLandmark.WRIST]
    finger = landmark_coordinates.landmark[mp_hands.HandLandmark.PINKY_TIP]
    return distance(wrist, finger) <= 0.32

def distance(coord_0, coord_1):
    difference = np.array([coord_0.x - coord_1.x, coord_0.y - coord_1.y, coord_0.z - coord_1.z])
    return np.sqrt(difference.dot(difference))

def get_hand_center(landmark_coordinates, mp_hands):
    wrist =  landmark_coordinates.landmark[mp_hands.HandLandmark.WRIST]
    return wrist.x, wrist.y


# Set game

pygame.init()
pygame.font.init()

# Video capture
cap = cv2.VideoCapture(0)

# Set up drawings and hands
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Information for fame
initial_disks = 3
counter = 0
dark_blue = (44, 44, 127)
game_screen = Grid(initial_disks)
smallfont = pygame.font.SysFont('Corbel',60)
font = pygame.font.SysFont('Arial', 30)
xCoord, yCoord = (0,0)

# Buttons for adding and decreasing number of disks
plus_button = pygame.Rect(840, 100, 50, 50)
minus_button = pygame.Rect(840, 150, 50, 50)


# Set game screen and caption
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
r = None
with mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5, max_num_hands = 1) as hands:
    while True:
        # Checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check if mouse is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:

                pos = pygame.mouse.get_pos()

                # Check if plus button was pressed
                if plus_button.collidepoint(pos) and initial_disks < 5:
                    initial_disks += 1
                    del game_screen
                    game_screen = Grid(initial_disks)
                
                # Check if minus button was pressed
                if minus_button.collidepoint(pos) and initial_disks > 1:
                    initial_disks -= 1
                    del game_screen
                    game_screen = Grid(initial_disks)
        
        ret, frame = cap.read()

        # Detections
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if not ret:
            pygame.quit()
            sys.exit()
        # Iterate over hands
        if results.multi_hand_landmarks:
            r = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(image, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
            xCoord, yCoord = get_hand_center(results.multi_hand_landmarks[0], mp_hands)
            xCoord = 1 - xCoord
            xCoord *= 1000
            yCoord *= 600

        if cv2.waitKey(10) and 0XFF == ord('q'):
            break

        image = cv2.flip(image, 1)
        
        # cv2.imshow("Video captured ", image)

        # Check if it has a disk grabed and the game still hasn't been solved
        if has_object_grabed and not game_screen.HanoiTower.solved:
            # Mouse is over a disk so over_disk is set to True
            over_disk = True

            # Set coordinates of grabed disk equal to mouse coordinates
            disk_grabed.center = (xCoord, yCoord)


            # Check if it stopped grabbing the disk
            if r and not hand_closed(r, mp_hands):
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
            if r and hand_closed(r, mp_hands) and over_disk:
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
        game_screen.draw_cursor(screen, xCoord, yCoord)
        txtsurf = font.render(f"Moves: {game_screen.HanoiTower.numberOfMoves}", False, (255,255,255))
        screen.blit(txtsurf,(840, 50))
        pygame.draw.rect(screen,(0, 255, 0) ,plus_button)
        screen.blit(smallfont.render("+", True, (0,0,0)), (852,103))

        pygame.draw.rect(screen, (255, 0, 0), minus_button)
        screen.blit(smallfont.render("-", True, (0,0,0)), (857,154))

        if game_screen.HanoiTower.solved:
            txtsurf = font.render("Challenge completed!", False, (255,255,255))
            screen.blit(txtsurf,(300, 50))

        pygame.display.update()
        clock.tick(60) # All code inside loop will run 60 times per second


cap.release()
cv2.destroyWindow()

