import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

ROWS = 20
COLS = 20
CELL_SIZE = 30 

# northWall[r][c] = 1 if solid upper wall, 0 if missing
northWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
# eastWall[r][c] = 1 if solid right wall, 0 if missing
eastWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]

visited_gen = [[False for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
visited_solve = [[False for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
dead_ends = []

def init_graphics():
    pygame.init()
    width = COLS * CELL_SIZE + 40
    height = ROWS * CELL_SIZE + 40
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    gluOrtho2D(0, width, 0, height)
    pygame.display.set_caption("Maze Generator & Solver")

def get_neighbors_gen(r, c):
    neighbors = []
    if r < ROWS - 1 and not visited_gen[r + 1][c]: neighbors.append((r + 1, c, 'N'))
    if r > 0 and not visited_gen[r - 1][c]: neighbors.append((r - 1, c, 'S'))
    if c < COLS - 1 and not visited_gen[r][c + 1]: neighbors.append((r, c + 1, 'E'))
    if c > 0 and not visited_gen[r][c - 1]: neighbors.append((r, c - 1, 'W'))
    return neighbors

def generate_maze_step():
    """Generator for the maze construction."""
    stack = []
    curr_r, curr_c = 0, 0
    visited_gen[curr_r][curr_c] = True
    while True:
        neighbors = get_neighbors_gen(curr_r, curr_c)
        if neighbors:
            nr, nc, direction = random.choice(neighbors)
            stack.append((curr_r, curr_c))
            if direction == 'N': northWall[curr_r][curr_c] = 0
            elif direction == 'S': northWall[nr][nc] = 0
            elif direction == 'E': eastWall[curr_r][curr_c] = 0
            elif direction == 'W': eastWall[nr][nc] = 0
            curr_r, curr_c = nr, nc
            visited_gen[curr_r][curr_c] = True
            yield
        elif stack:
            curr_r, curr_c = stack.pop()
            yield
        else: break

def solve_maze_step():
    """Generator for the 'Red Dot' solver with backtracking."""
    stack = []
    curr_r, curr_c = 0, 0
    visited_solve[curr_r][curr_c] = True
    path = [(curr_r, curr_c)]
    
    while curr_r != ROWS - 1 or curr_c != COLS - 1:
        options = []
        if curr_r < ROWS - 1 and northWall[curr_r][curr_c] == 0 and not visited_solve[curr_r+1][curr_c]:
            options.append((curr_r + 1, curr_c))
        if curr_r > 0 and northWall[curr_r-1][curr_c] == 0 and not visited_solve[curr_r-1][curr_c]:
            options.append((curr_r - 1, curr_c))
        if curr_c < COLS - 1 and eastWall[curr_r][curr_c] == 0 and not visited_solve[curr_r][curr_c+1]:
            options.append((curr_r, curr_c + 1))
        if curr_c > 0 and eastWall[curr_r][curr_c-1] == 0 and not visited_solve[curr_r][curr_c-1]:
            options.append((curr_r, curr_c - 1))

        if options:
            stack.append((curr_r, curr_c))
            curr_r, curr_c = random.choice(options)
            visited_solve[curr_r][curr_c] = True
            path.append((curr_r, curr_c))
        elif stack:
            dead_ends.append((curr_r, curr_c))
            path.pop()
            curr_r, curr_c = stack.pop()
        
        yield path
    yield path

def draw_maze():
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE + 20, r * CELL_SIZE + 20
            if northWall[r][c] == 1:
                glVertex2f(x, y + CELL_SIZE); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
            if eastWall[r][c] == 1:
                glVertex2f(x + CELL_SIZE, y); glVertex2f(x + CELL_SIZE, y + CELL_SIZE)
    # Boundaries
    for r in range(ROWS): 
        glVertex2f(20, r * CELL_SIZE + 20); glVertex2f(20, (r+1)*CELL_SIZE + 20)
    for c in range(COLS): 
        glVertex2f(c * CELL_SIZE + 20, 20); glVertex2f((c+1)*CELL_SIZE + 20, 20)
    glEnd()

def draw_dots(path):
    glPointSize(8)
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 1.0)
    for r, c in dead_ends:
        glVertex2f(c * CELL_SIZE + 20 + CELL_SIZE/2, r * CELL_SIZE + 20 + CELL_SIZE/2)
    
    if path:
        glColor3f(1.0, 0.0, 0.0)
        curr_r, curr_c = path[-1]
        glVertex2f(curr_c * CELL_SIZE + 20 + CELL_SIZE/2, curr_r * CELL_SIZE + 20 + CELL_SIZE/2)
    glEnd()

def main():
    init_graphics()
    gen = generate_maze_step()
    solver = None
    path = []
    generating = True
    solving = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_maze()
        
        if generating:
            try: next(gen)
            except StopIteration:
                generating = False
                solving = True
                solver = solve_maze_step()
        elif solving:
            try: path = next(solver)
            except StopIteration: solving = False
            draw_dots(path)

        pygame.display.flip()
        pygame.time.wait(15)
    pygame.quit()

if __name__ == "__main__":
    main()
