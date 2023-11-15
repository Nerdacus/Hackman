import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 520
BACKGROUND_COLOR = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
TERMINAL_COLOR = (0, 255, 0)
PROGRESS_BAR_COLOR = (0, 0, 255)
DOT_RADIUS = 5
TERMINAL_SIZE = 20
PROGRESS_BAR_HEIGHT = 20
HACKMAN_RADIUS = 15
GHOST_SIZE = 20
GRID_SIZE = 40
MAX_HACKING_TIME = 600

# Create a Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hack-Man")

clock = pygame.time.Clock()

# Hack-Man's initial position
hackman_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
hackman_y = ((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

# Ghost's initial position
ghost_x = random.randint(0, SCREEN_WIDTH)
ghost_y = random.randint(0, SCREEN_HEIGHT)

# Create a maze layout
# Define multiple maze layouts
initial_maze_layout = [
    "####################",
    "#..................#",
    "#.###.#####.#.####..#",
    "#.#...#.....#.#.....#",
    "#.#.#...#.#.#.#.#.#.#",
    "#...#.#.......#.#...#",
    "###.#.##....#.#.#...#",
    "#...#.#.....#.#.#...#",
    "#.###.#.###.#.#.###.#",
    "#.....#...#...#...#.#",
    "#.#####.#.#####.#.###",
    "#.................#",
    "####################"
]

hacked_maze_layout = [
    "####################",
    "#..................#",
    "#.###.#####.#.####..#",
    "#.#...#.....#.#.....#",
    "#.#.#...#.#.#.#.#.#.#",
    "#...#.#.......#.#...#",
    "###.#.##....#.#.#...#",
    "#...#.#.....#.#.#...#",
    "#.###.#.###.#.#.###.#",
    "#.....#...#...#...#.#",
    "#.#####.#.#####.#.###",
    "#.................#",
    "####.###########.###"
]

# Initializing current maze layout
current_maze_layout = initial_maze_layout

# Create a grid for dot positions in the maze path
grid = []

for row, line in enumerate(current_maze_layout):
    for col, char in enumerate(line):
        if char == '.':
            grid.append((col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))

# Define terminal positions aligned to the grid
terminals = [
    (360, 160)
]

for i in range(len(terminals)):
    terminals[i] = ((terminals[i][0] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2,
                    (terminals[i][1] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)

# Create a list to track hacked terminals
hacked_terminals = [False] * len(terminals)

# Main game loop
running = True
score = 0
frame_count = 0

# Initialize variables for tracking hacking progress
hacking = False
hacking_time = 0
spacebar_held = False

# Initialize variables to store the old position of Hack-Man
hackman_old_x = hackman_x
hackman_old_y = hackman_y


def setup_game_state(map_layout):
    global current_maze_layout, terminals, hacked_terminals, hackman_x, hackman_y, hackman_old_x, hackman_old_y

    # Initialize the game state based on the current maze layout
    current_maze_layout = map_layout

    # Reset Hack-Man's position
    hackman_old_x = hackman_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
    hackman_old_y = hackman_y = ((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

    # Reset terminal positions and hacked terminals
    terminals = [
        (360, 160)
    ]
    for i in range(len(terminals)):
        terminals[i] = ((terminals[i][0] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2,
                        (terminals[i][1] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)
    hacked_terminals = [False] * len(terminals)


def draw_game_screen():
    # Draw the background
    screen.fill(BACKGROUND_COLOR)

    # Draw the maze layout
    for row, line in enumerate(current_maze_layout):
        for col, char in enumerate(line):
            if char == '#':
                pygame.draw.rect(screen, (100, 100, 100), (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw dots
    for dot in grid:
        pygame.draw.circle(screen, WHITE, dot, DOT_RADIUS)

    # Draw terminals
    for i, terminal in enumerate(terminals):
        # Only draw the terminal if it hasn't been hacked
        if not hacked_terminals[i]:
            pygame.draw.rect(screen, TERMINAL_COLOR,
                             (terminal[0] - TERMINAL_SIZE // 2, terminal[1] - TERMINAL_SIZE // 2, TERMINAL_SIZE,
                              TERMINAL_SIZE))

    # Draw a progress bar when hacking
    if hacking:
        print("Hacking")
        progress_bar_width = (hacking_time / MAX_HACKING_TIME) * TERMINAL_SIZE
        pygame.draw.rect(screen, PROGRESS_BAR_COLOR,
                         (hackman_x - TERMINAL_SIZE // 2, hackman_y - TERMINAL_SIZE // 2 - PROGRESS_BAR_HEIGHT,
                          progress_bar_width, PROGRESS_BAR_HEIGHT))

    # Draw Hack-Man
    pygame.draw.circle(screen, YELLOW, (hackman_x, hackman_y), HACKMAN_RADIUS)

    # Draw Ghost
    pygame.draw.rect(screen, RED, (ghost_x, ghost_y, GHOST_SIZE, GHOST_SIZE))


def main():
    global hackman_x, hackman_y, hackman_old_x, hackman_old_y, terminals, hacked_terminals, current_maze_layout, grid
    # Main game loop

    last_movement_time = pygame.time.get_ticks()
    running = True
    score = 0
    frame_count = 0
    hacking = False
    hacking_time = 0
    spacebar_held = False

    # Initialize the game with the initial maze layout
    setup_game_state(initial_maze_layout)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                spacebar_held = True

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                spacebar_held = False

        # Check for collisions with dots
        for dot in grid[:]:
            if pygame.Rect(dot[0] - DOT_RADIUS, dot[1] - DOT_RADIUS, DOT_RADIUS * 2, DOT_RADIUS * 2).colliderect(
                    (hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2, HACKMAN_RADIUS * 2)):
                grid.remove(dot)
                score += 10

        # Update Hack-Man's position every 60 frames
        keys = pygame.key.get_pressed()

        # Store the current position
        hackman_old_x = hackman_x
        hackman_old_y = hackman_y


        # Update Hack-Man's position every 60 frames
        if clock.get_fps() > 0:  # Ensure the frame rate is not zero to avoid division by zero
            movement_speed = GRID_SIZE / clock.get_fps()  # Adjust the movement speed based on the frame rate

            if keys[pygame.K_LEFT]:
                hackman_x -= movement_speed
            if keys[pygame.K_RIGHT]:
                hackman_x += movement_speed
            if keys[pygame.K_UP]:
                hackman_y -= movement_speed
            if keys[pygame.K_DOWN]:
                hackman_y += movement_speed

        for row, line in enumerate(current_maze_layout):
            for col, char in enumerate(line):
                if char == '#':
                    wall_rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    if wall_rect.colliderect(
                            (hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2,
                             HACKMAN_RADIUS * 2)):
                        hackman_x = hackman_old_x
                        hackman_y = hackman_old_y

        # Check if Hack-Man collides with exits when all terminals are hacked
        if all(hacked_terminals):
            for row, line in enumerate(current_maze_layout):
                for col, char in enumerate(line):
                    if char == '.':
                        exit_rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                        if exit_rect.colliderect((
                                                 hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2,
                                                 HACKMAN_RADIUS * 2)):
                            hackman_x = hackman_old_x
                            hackman_y = hackman_old_y

            # Check if all terminals are hacked
            if all(hacked_terminals):
                # Switch to the hacked maze layout
                setup_game_state(hacked_maze_layout)
                pygame.time.delay(500)

        # Loop Hack-Man to the other side if it goes out of bounds
        if hackman_x < 0:
            hackman_x = SCREEN_WIDTH
        elif hackman_x > SCREEN_WIDTH:
            hackman_x = 0

        if hackman_y < 0:
            hackman_y = SCREEN_HEIGHT
        elif hackman_y > SCREEN_HEIGHT:
            hackman_y = 0

        # Ensure that Hack-Man stays within the maze boundaries
        if hackman_x < 0:
            hackman_x = SCREEN_WIDTH + 20
        elif hackman_x > SCREEN_WIDTH:
            hackman_x = HACKMAN_RADIUS

        if hackman_y < 0:
            hackman_y = SCREEN_HEIGHT + 20
        elif hackman_y > SCREEN_HEIGHT:
            hackman_y = HACKMAN_RADIUS

        if not hacking:
            for i, terminal in enumerate(terminals):
                terminal_rect = pygame.Rect(terminal[0] - TERMINAL_SIZE // 2, terminal[1] - TERMINAL_SIZE // 2,
                                            TERMINAL_SIZE, TERMINAL_SIZE)
                if terminal_rect.colliderect((
                                             hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2,
                                             HACKMAN_RADIUS * 2)):
                    if keys[pygame.K_SPACE]:
                        print("Space bar pressed - Initiating hacking")
                        hacking = True
                        hacking_time = 0
        else:
            # Increment hacking time
            hacking_time += 1
            print(f"Hacking time: {hacking_time}, Max Hacking Time: {MAX_HACKING_TIME}")
            if hacking_time >= MAX_HACKING_TIME:
                print("Executing hacking block")
                # "Hack" the terminal by removing it
                for i, terminal in enumerate(terminals):
                    terminal_rect = pygame.Rect(terminal[0] - TERMINAL_SIZE // 2, terminal[1] - TERMINAL_SIZE // 2,
                                                TERMINAL_SIZE, TERMINAL_SIZE)
                    if terminal_rect.colliderect((hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS,
                                                  HACKMAN_RADIUS * 2, HACKMAN_RADIUS * 2)):
                        terminals.remove(terminal)
                        hacked_terminals[i] = True
                        hacking = False

        # Draw the game screen
        draw_game_screen()

        # Update the display
        pygame.display.flip()

        clock.tick(60)

    # Game over
    print(f"Game over! Score: {score}")

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()