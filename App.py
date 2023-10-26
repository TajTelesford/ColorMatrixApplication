from dataclasses import dataclass
from queue import PriorityQueue, Queue
from typing import Optional
import pygame
import random
from CustomQueue import CustomQueue
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
MATRIX_WIDTH = WIDTH // CELL_SIZE
MATRIX_HEIGHT = HEIGHT // CELL_SIZE
TRAIL_LENGTH = 20  
MAX_TRAILS = 150
FPS = 20
GREEN = (0, 255, 0)

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
            pygame.draw.rect(window, GREEN, rect, 1 )

SET_OF_TRAILS = set()

trails = CustomQueue([], MAX_TRAILS)


FONT = pygame.font.Font(None, 15)

@dataclass
class ListNode:
    value: str
    pos: tuple
    next: None
    maxed: Optional[bool] = False

def append_node(node):
    count = 1
    prev = None
    while node.next:
        node = node.next
        count += 1
    maxed = count == TRAIL_LENGTH - 1 #Append a node with the maxed flag  == TRUE
    node.next = ListNode(
            random.choice(ASCII_CHARACTERS),
            (node.pos[0], node.pos[1] - 10),
            None,
            maxed
        )
        


#This adds a Starting node for trails to grow
def add_trails():
    x = random.randint(0, WIDTH - 1)
    while x not in trails.xSet():
        x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT// 2)
    trails.addX(x)

    return ListNode(
        random.choice(ASCII_CHARACTERS),
        (x, y),
        None
    )
            

def draw_trails(trail: ListNode):
    while trail:
        char = FONT.render(trail.value, True, GREEN)
        screen.blit(char, trail.pos)
        trail = trail.next


def move_trails():

    for node in trails.Trails():
        temp = node
        append_node(temp)
        
        prev = None
        while temp:
            temp.pos = (temp.pos[0], temp.pos[1] + 15)
            prev = temp
            temp = temp.next
        if prev and prev.maxed:
            trails.dequeue()
            trails.enqueue(add_trails())

def update_trails():
        
    for node in trails.Trails():
        if node.pos[1] > HEIGHT: #If node is greater then Height we will delete it from the linked list
            new = trails.Pop(node, add_trails)
            trails.removeX(node.pos[0])
            trails.enqueue(new)
            trails.addX(node.pos[0])
            if node.next:
                node = node.next
        temp = node
        draw_trails(temp)
    move_trails()
    
def initialize_trails():
    for _ in range(MAX_TRAILS):
        x = random.randint(0, WIDTH)
        if x in trails.xSet():
            while x not in trails.xSet():
                x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        trails.enqueue(ListNode(
                random.choice(ASCII_CHARACTERS),
                (x, y),
                None
            ))
        trails.addX(x)

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
        #display_grid(screen)
        pygame.display.update()
        frame += 1
        clock.tick(FPS)  # Adjust the frame rate as needed

    pygame.quit()

if __name__ == "__main__":
    main()