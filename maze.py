import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Maze dimensions
ROWS = 20
COLS = 20
CELL_SIZE = 30

# northWall[r][c] = 1 if solid upper wall, 0 if missing
northWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
# eastWall[r][c] = 1 if solid right wall, 0 if missing
eastWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]

def init_graphics():
    pygame.init()
    # Calculate window size based on maze size
    width = COLS * CELL_SIZE + 40
    height = ROWS * CELL_SIZE + 40
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    gluOrtho2D(0, width, 0, height)
    pygame.display.set_caption("Maze Generator & Solver")

def draw_grid():
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)
    
    glBegin(GL_LINES)
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            x = c * CELL_SIZE + 20
            y = r * CELL_SIZE + 20
            
            if northWall[r][c] == 1:
                glVertex2f(x, y + CELL_SIZE)
                glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
                
            if eastWall[r][c] == 1:
                glVertex2f(x + CELL_SIZE, y)
                glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
    glEnd()

def main():
    init_graphics()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_grid()
        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()