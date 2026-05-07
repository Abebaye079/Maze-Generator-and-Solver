import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# --- CONSTANTS ---
ROWS = 20
COLS = 20
CELL_SIZE = 30 

# --- DATA STRUCTURES ---
# northWall[r][c] = 1 if solid upper wall, 0 if missing (eaten)
northWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
# eastWall[r][c] = 1 if solid right wall, 0 if missing (eaten)
eastWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]

# Track visited cells for the generation algorithm
visited = [[False for _ in range(COLS + 1)] for _ in range(ROWS + 1)]

def init_graphics():
    pygame.init()
    width = COLS * CELL_SIZE + 40
    height = ROWS * CELL_SIZE + 40
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    gluOrtho2D(0, width, 0, height)
    pygame.display.set_caption("Maze Generator & Solver")

def get_neighbors(r, c):
    """Finds unvisited adjacent cells."""
    neighbors = []
    # Check North
    if r < ROWS - 1 and not visited[r + 1][c]:
        neighbors.append((r + 1, c, 'N'))
    # Check South
    if r > 0 and not visited[r - 1][c]:
        neighbors.append((r - 1, c, 'S'))
    # Check East
    if c < COLS - 1 and not visited[r][c + 1]:
        neighbors.append((r, c + 1, 'E'))
    # Check West
    if c > 0 and not visited[r][c - 1]:
        neighbors.append((r, c - 1, 'W'))
    return neighbors

def generate_maze(start_r, start_c):
    """The 'Mouse' logic: uses a stack to eat through walls and create a path."""
    stack = []
    current_r, current_c = start_r, start_c
    visited[current_r][current_c] = True
    
    while True:
        neighbors = get_neighbors(current_r, current_c)
        
        if neighbors:
            # Pick a random neighbor
            next_r, next_c, direction = random.choice(neighbors)
            stack.append((current_r, current_c))
            
            # Remove the wall between current and next
            if direction == 'N':
                northWall[current_r][current_c] = 0
            elif direction == 'S':
                northWall[next_r][next_c] = 0
            elif direction == 'E':
                eastWall[current_r][current_c] = 0
            elif direction == 'W':
                eastWall[next_r][next_c] = 0
                
            current_r, current_c = next_r, next_c
            visited[current_r][current_c] = True
        elif stack:
            # Backtrack
            current_r, current_c = stack.pop()
        else:
            break

def draw_maze():
    """Renders the maze based on northWall and eastWall arrays."""
    glColor3f(1.0, 1.0, 1.0) # White walls
    glLineWidth(2)
    
    glBegin(GL_LINES)
    # The assignment notes the 0th row/column are boundaries
    for r in range(ROWS):
        for c in range(COLS):
            x = c * CELL_SIZE + 20
            y = r * CELL_SIZE + 20
            
            # Draw North Wall
            if northWall[r][c] == 1:
                glVertex2f(x, y + CELL_SIZE)
                glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
                
            # Draw East Wall
            if eastWall[r][c] == 1:
                glVertex2f(x + CELL_SIZE, y)
                glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
                
    # Draw Left and Bottom boundaries (as per assignment logic)
    for r in range(ROWS): # Left boundary
        glVertex2f(20, r * CELL_SIZE + 20)
        glVertex2f(20, (r + 1) * CELL_SIZE + 20)
    for c in range(COLS): # Bottom boundary
        glVertex2f(c * CELL_SIZE + 20, 20)
        glVertex2f((c + 1) * CELL_SIZE + 20, 20)
    glEnd()

def main():
    init_graphics()
    
    # Generate the maze once before starting the loop
    generate_maze(0, 0)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_maze()
        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
