from dataclasses import dataclass
from typing import Optional
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
MATRIX_WIDTH = WIDTH // CELL_SIZE
MATRIX_HEIGHT = HEIGHT // CELL_SIZE
TRAIL_LENGTH = 10  # Number of frames a character stays visible
MAX_TRAILS = 20

WHITE = (255, 255, 255)

# ASCII characters
ASCII_CHARACTERS = "023456789!@#$%^&*abcdefghijklmnopABCDEEFGHIJKLMNOP"

# Create the Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASCII Matrix Generator")
clock = pygame.time.Clock()

def display_grid(window):
    for i in range(0, WIDTH, CELL_SIZE):
        for j in range(0, HEIGHT, CELL_SIZE):
            rect = pygame.Rect(i, j, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, WHITE, rect, 1 )

SET_OF_TRAILS = set()
TRAILS = []

FONT = pygame.font.Font(None, 15)

@dataclass
class ListNode:
    value: str
    pos: tuple
    next: None
    maxed: Optional[bool] = False

def append_node(node):
    count = 0
    prevPos = None
    if not node.next:
        
        node.next = ListNode(
            random.choice(ASCII_CHARACTERS),
            (node.pos[0], node.pos[1] - 10),
            None
        )
        return
    while node.next:
        count += 1
        prevPos = node.pos
        
        node = node.next
    if count < TRAIL_LENGTH:
        node.next = ListNode(
            random.choice(ASCII_CHARACTERS),
            (prevPos[0], prevPos[1] - 10),
            None
        )

    elif count == TRAIL_LENGTH:
        node.maxed = True
        
    return None

#This adds a Starting node for trails to grow
def add_trails():
    if len(SET_OF_TRAILS) < MAX_TRAILS:
        x = random.randint(0, WIDTH)
        while x in SET_OF_TRAILS:
            x = random.randint(0, WIDTH)
            if x not in SET_OF_TRAILS:
                node = ListNode(
                    random.choice(ASCII_CHARACTERS),
                    (x, random.randint(0, HEIGHT)),
                    None
                )
                SET_OF_TRAILS.add(node.pos[0]) #Adds the x value into the set so we won't have overlapping trails
                TRAILS.append(node) #adds the node so we could start appending nodes to this trail

def draw_trails(trail: ListNode):
    while trail:
        
        char = FONT.render(trail.value, True, WHITE)
        screen.blit(char, trail.pos)
        trail = trail.next

def move_trails():
    idx = 0
    for node in TRAILS:
        if not node.next and node.maxed: #if their next node is null, we will remove the x position from the set and add the start of a new trail
            print("max")
            SET_OF_TRAILS.remove(node.pos[0])
            TRAILS.pop(idx)
            add_trails()
            continue
        elif node.pos[1] > HEIGHT: #If node is greater then Height we will delete it from the linked list
            #print("HERE")
            SET_OF_TRAILS.remove(node.pos[0])
            if node.next:
                SET_OF_TRAILS.add(node.next.pos[0])
                #print("HERE")
                node = node.next
        idx += 1
        n = None
        temp = node
        if temp:
            n = append_node(temp)
        if n:
            node.next = n
        temp = node
        while temp:
            temp.pos = (temp.pos[0], temp.pos[1] + 5)
            temp = temp.next

def update_trails():
    for node in TRAILS:
        temp = node
        draw_trails(temp)
    move_trails()
    
def initialize_trails():
    for _ in range(MAX_TRAILS):
        x = random.randint(0, WIDTH)
        while x not in SET_OF_TRAILS:
            x = random.randint(0, WIDTH)
            if x not in SET_OF_TRAILS:
                break
        y = random.randint(0, HEIGHT)
        TRAILS.append(
            ListNode(
                random.choice(ASCII_CHARACTERS),
                (x, y),
                None
            )
        )
        SET_OF_TRAILS.add(x)

def main():
    frame = 0  # Frame counter
    initialize_trails()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 0, 0))  
       
        update_trails()
        pygame.display.update()
        print(SET_OF_TRAILS)
        #print(TRAILS)
        frame += 1
        clock.tick(30)  # Adjust the frame rate as needed

    pygame.quit()

if __name__ == "__main__":
    main()