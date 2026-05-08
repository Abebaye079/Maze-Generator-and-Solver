    # Building & Solving Mazes with PyOpenGL

This project is a deep dive into computer graphics and algorithmic logic. Using Python, Pygame, and PyOpenGL, I’ve created a system that doesn't just show a finished maze, but brings the entire lifecycle of a maze to life—from its "birth" via a wandering mouse to its "solution" via a pathfinding dot.

    ## How the Maze is Born (The "Mouse" Logic)

Instead of just generating a static grid, I implemented a stack-based Depth-First Search (DFS) algorithm. Think of it as a "Mouse" that starts at a single point and begins eating through walls:

    -Exploration: The mouse looks for any neighbor it hasn't visited yet.

    -The Stack: When it moves to a new cell, it remembers where it came from by pushing the location onto a stack.

    -Backtracking: If the mouse gets stuck in a corner with no unvisited neighbors, it "pops" the stack to backtrack until it finds a new path to eat.

    ## Solving the Mystery (The "Red Dot")


Once the maze is built, the program switches gears to find a solution. It uses a second stack to track a Red Dot moving from the entrance to the exit.

    -Dead Ends: If the dot hits a dead end, it leaves behind a Blue Dot to mark that path as explored but incorrect.

    -The Result: You get to watch the trial-and-error process of the algorithm in real-time until the exit is reached.

    ## The Challenge (Adding Cycles)
To make things more interesting and fulfill the bonus challenge, I added a bit of chaos: there is a 1 in 20 chance that the mouse eats an extra wall. This creates "cycles" or loops in the maze, meaning there isn't just one unique path. This tests the solver's ability to navigate more complex, non-linear environments.

    ## Under the Hood: Data Representation
The project follows the assignment's specific data structure requirements:

    -The Walls: Two 2D arrays, northWall and eastWall, track every cell. A 1 means the wall is solid, and a 0 means it has been removed.

    -The Graphics: All rendering is done via OpenGL, using a 2D orthographic projection to map the logical grid to your screen pixels.

    ## Demo Link: https://www.loom.com/share/fd23de30696947eeadab0a4f16bda974

When you watch the Loom recording of this project, you’ll see the maze being "eaten" line-by-line. Once the grid is fully carved out, you'll see the Red Dot intelligently navigate toward the exit, backtracking and marking dead ends in blue along the way.