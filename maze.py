import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

ROWS, COLS = 20, 20
CELL_SIZE = 30 

# northWall[r][c] = 1 if solid upper wall; 0 if missing [cite: 15]
northWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
# eastWall[r][c] = 1 if solid right wall; 0 if missing [cite: 17]
eastWall = [[1 for _ in range(COLS + 1)] for _ in range(ROWS + 1)]

visited_gen = [[False for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
visited_solve = [[False for _ in range(COLS + 1)] for _ in range(ROWS + 1)]
dead_ends = [] 

def init_graphics():
    pygame.init()
    width, height = COLS * CELL_SIZE + 40, ROWS * CELL_SIZE + 40
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
    """Stack-based DFS 'mouse' logic[cite: 72, 96]."""
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
            
            # 1 in 20 chance to eat an extra random wall to create a cycle
            if random.random() < 0.05:
                extra_r, extra_c = random.randint(0, ROWS-1), random.randint(0, COLS-1)
                if random.choice([True, False]): northWall[extra_r][extra_c] = 0
                else: eastWall[extra_r][extra_c] = 0
            
            curr_r, curr_c = nr, nc
            visited_gen[curr_r][curr_c] = True
            yield
        elif stack:
            curr_r, curr_c = stack.pop()
            yield
        else: break
    
    eastWall[ROWS-1][0] = 0
    eastWall[0][COLS-1] = 0

def solve_maze_step():
    """Backtracking solver with red/blue dots[cite: 81, 84, 102]."""
    stack = []
    curr_r, curr_c = ROWS-1, 0
    visited_solve[curr_r][curr_c] = True
    path = [(curr_r, curr_c)]
    while curr_r != 0 or curr_c != COLS - 1:
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
            path.pop(); curr_r, curr_c = stack.pop()
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
    for r in range(ROWS):
        if eastWall[r][0] == 1:
            glVertex2f(20, r * CELL_SIZE + 20); glVertex2f(20, (r+1)*CELL_SIZE + 20)
    for c in range(COLS):
        glVertex2f(c * CELL_SIZE + 20, 20); glVertex2f((c+1)*CELL_SIZE + 20, 20)
    glEnd()

def draw_dots(path):
    glPointSize(10)
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 1.0)
    for r, c in dead_ends:
        glVertex2f(c * CELL_SIZE + 20 + CELL_SIZE/2, r * CELL_SIZE + 20 + CELL_SIZE/2)
    if path:
        glColor3f(1.0, 0.0, 0.0)
        cr, cc = path[-1]
        glVertex2f(cc * CELL_SIZE + 20 + CELL_SIZE/2, cr * CELL_SIZE + 20 + CELL_SIZE/2)
    glEnd()

def main():
    init_graphics()
    gen, solver, path = generate_maze_step(), None, []
    generating, solving = True, False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_maze()
        if generating:
            try: next(gen)
            except StopIteration: generating, solving = False, True; solver = solve_maze_step()
        elif solving:
            try: path = next(solver)
            except StopIteration: solving = False
            draw_dots(path)
        pygame.display.flip()
        pygame.time.wait(15)

if __name__ == "__main__": main()
