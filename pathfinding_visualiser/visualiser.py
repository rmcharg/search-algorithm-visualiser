import pygame
from tkinter import messagebox
from .grid import Node, Grid
from .utils import get_mouse_pos
from .algorithms import BFS, DFS, DFS_recursive






def visualiser(algorithm=1, generate_maze=False):
    # Window Config Settings
    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = 800
    ROWS = 40
    COLUMNS = 40

    # Create pygame window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_WIDTH))
    screen.fill((0, 0, 0))

    Node.height = WINDOW_HEIGHT // ROWS
    Node.width = WINDOW_WIDTH // COLUMNS 

    grid = Grid(ROWS, COLUMNS)
    grid.create_grid(generate_maze)

    # Game loop
    running = True
    while running:
        grid.draw_grid(screen)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                break
            
            if grid.searching:
                continue
            
            # On left click assign start point, end point and walls
            if pygame.mouse.get_pressed() [0]:
                # Get node that mouse has clicked on
                row, col = get_mouse_pos(Node.height, Node.width)
                try:
                    node = grid.get_node(row, col)
                except:
                    pass
                # Assign state to node
                if not grid.start_node and node != grid.end_node:
                    node.make_start()
                    grid.start_node = node
                elif not grid.end_node and node != grid.start_node:
                    node.make_end()
                    grid.end_node = node
                elif node != grid.start_node and node != grid.end_node:
                    node.make_wall()
            
            # On right click reset the spot to default
            elif pygame.mouse.get_pressed()[2]:
                row, col = get_mouse_pos(Node.height, Node.width)
                node = grid.get_node(row, col)

                if node == grid.start_node:
                    grid.start_node = None
                if node == grid.end_node:
                    grid.end_node = None
                node.reset()

            
            elif event.type == pygame.KEYDOWN:
                # Clear Grid
                if event.key == pygame.K_c and not grid.searching:
                    grid = Grid(ROWS, COLUMNS)
                    grid.create_grid()
                # Reset Grid
                elif event.key == pygame.K_r and not grid.searching:
                    grid.reset_grid()
                # Start search
                elif (event.key == pygame.K_RETURN and not grid.searching 
                    and grid.start_node and grid.end_node):
                    for row in grid.nodes:
                        for node in row:
                            node.set_neighbours(grid)
                    grid.searching = True
                    if algorithm == 1:
                        print("Starting BFS Algorithm")
                        found = BFS(grid, screen)
                        if found is False:
                            print("Target node not found!")
                    elif algorithm == 2:
                        print("Starting DFS Algorithm")
                        found = DFS_recursive(grid.start_node, grid, screen)
                        if found is False:
                            print("Target node not found!")
                    grid.searching = False

    pygame.quit()









