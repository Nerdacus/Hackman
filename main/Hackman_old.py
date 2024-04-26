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
BLUE = (0,0,255)
WHITE = (255, 255, 255)
TERMINAL_COLOR = (0, 255, 0)
PROGRESS_BAR_COLOR = (0, 0, 255)
DOT_RADIUS = 5
TERMINAL_SIZE = 20
PROGRESS_BAR_HEIGHT = 20
HACKMAN_RADIUS = 15
GHOST_SIZE = 20
GHOST_SPEED = 10
GRID_SIZE = 40
MAX_HACKING_TIME = 60

# Create a Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hack-Man")

clock = pygame.time.Clock()

# Hack-Man's initial position
hackman_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
hackman_y = ((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

# Ghost's initial position
# ghost_x = 330
# ghost_y = 130

font = pygame.font.SysFont(None, 36)

right_frames = []
left_frames = []
up_frames = []
down_frames = []

right_frame_paths = [
"right-frame-one.png",
"right-frame-two.png",
"right-frame-three.png",
"right-frame-four.png"
]

left_frame_paths = [
"left-frame-one.png",
"left-frame-two.png",
"left-frame-three.png",
"left-frame-four.png"
]

up_frame_paths = [
"up-frame-one.png",
"up-frame-two.png",
"up-frame-three.png",
"up-frame-four.png"
]

down_frame_paths = [
"down-frame-one.png",
"down-frame-two.png",
"down-frame-three.png",
"down-frame-four.png"
]

for path in right_frame_paths:
    image = pygame.image.load(path).convert_alpha()
    right_frames.append(image)

for path in left_frame_paths:
    image = pygame.image.load(path).convert_alpha()
    left_frames.append(image)

for path in up_frame_paths:
    image = pygame.image.load(path).convert_alpha()
    up_frames.append(image)

for path in down_frame_paths:
    image = pygame.image.load(path).convert_alpha()
    down_frames.append(image)

no_movement_image = pygame.image.load('no-movement.png').convert_alpha()
ghost1_up_image = pygame.image.load('ghost1-up.png').convert_alpha()
ghost1_down_image = pygame.image.load('ghost1-down.png').convert_alpha()
ghost1_left_image = pygame.image.load('ghost1-left.png').convert_alpha()
ghost1_right_image = pygame.image.load('ghost1-right.png').convert_alpha()

current_ghost1_image = ghost1_right_image
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

final_maze_layout = [
    "##########.#########",
    "#.#................#",
    "###................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "####################"
]

final_hacked_layout = [
    "##########.#########",
    "#.#................#",
    "#.#................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "#..................#",
    "####################"
]

# Define the ghost's spawn point and the predefined path for the ghost to follow
ghost_spawn_x, ghost_spawn_y = 360, 160

ghost_path = [
    (360, 220), (400, 160),
    (440, 100), (480, 160), (520, 220), (480, 280),(440, 340),
    (400, 280), (360, 220), (320, 160),(280, 100), (240, 160),
    (200, 220),  (240, 280), (280, 340), (320, 280),  (360, 220),
]

# Define path for the second ghost
ghost_2_path = [
    (620, 460), (660, 460), (700, 460), (700, 420), (700, 380), (660, 380), (620, 380), (620, 340),
    (620, 300), (620, 260), (620, 220), (620, 180), (620, 140), (660, 140), (700, 140), (700, 180),
    (700, 220), (700, 260), (700, 300), (740, 300), (780, 300), (780, 260), (780, 220), (780, 180),
    (780, 140), (740, 140), (700, 140), (660, 140), (620, 140), (620, 180), (620, 220), (620, 260),
    (620, 300), (620, 340), (620, 380), (620, 420), (620, 460)
]

# Initialize ghost's current position and path index
ghost_x, ghost_y = ghost_spawn_x, ghost_spawn_y
path_index = 1
ghost_2_x, ghost_2_y = ghost_2_path [0]
path_index_2 = 1



# Initializing current maze layout
current_maze_layout = initial_maze_layout

# Create a grid for dot positions in the maze path
initial_grid = []
final_grid = []

for row, line in enumerate(initial_maze_layout):
    for col, char in enumerate(line):
        if char == '.':
            initial_grid.append((col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))

for row, line in enumerate(final_maze_layout):
    for col, char in enumerate(line):
        if char == '.':
            final_grid.append((col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))


# Define terminal positions aligned to the grid
initial_terminals = [
    (360, 160)
]

final_terminals= [
    (380,140),
    (140, 140)
]

grid = initial_grid
terminals = initial_terminals

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
    global current_maze_layout, terminals, hacked_terminals, hackman_x, hackman_y, hackman_old_x, hackman_old_y, grid

    # Initialize the game state based on the current maze layout
    current_maze_layout = map_layout

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

    # Reset Hack-Man's position based on the center of the screen
    hackman_x = SCREEN_WIDTH // 2
    hackman_y = SCREEN_HEIGHT // 2

    # Adjust Hack-Man's position based on the grid
    hackman_x = ((hackman_x // GRID_SIZE) * GRID_SIZE) + GRID_SIZE // 2
    hackman_y = ((hackman_y // GRID_SIZE) * GRID_SIZE) + GRID_SIZE // 2

    if current_maze_layout == hacked_maze_layout:
        hackman_x = 380
        hackman_y = 180

    # Update terminals and grid based on the final layout
    if map_layout == final_maze_layout:
        # Adjust Hack-Man's position based on the final layout
        hackman_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
        hackman_y = ((SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2

        # Update terminals based on the final layout
        terminals = []
        for pos in final_terminals:
            terminals.append(
                ((pos[0] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2, (pos[1] // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)
            )

        # Update grid based on the final layout
        grid = []
        for row, line in enumerate(final_maze_layout):
            for col, char in enumerate(line):
                if char == '.':
                    grid.append((col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2))

        # Reset hacked terminals
        hacked_terminals = [False] * len(terminals)

    # Store the initial position as the old position
    hackman_old_x = hackman_x
    hackman_old_y = hackman_y

mrs_hackman_image = pygame.image.load('mrs-hackman-right-one.png').convert_alpha()
mrs_hackman_x = 60
mrs_hackman_y = 60

mrs_hackman_actived = False
mrs_hackman_direction = 'right'

def remove_wall():
    global current_maze_layout
    # Check if at least one terminal is hacked and the current maze layout is the final layout
    if current_maze_layout == final_maze_layout and any(hacked_terminals):
        print("Remove wall")
        wall_position_to_remove = (1,2)  # Define the position of the wall to remove
        if current_maze_layout[wall_position_to_remove[1]][wall_position_to_remove[0]] == '#':
            # Remove the wall at the specified position
            current_maze_layout[wall_position_to_remove[1]] = current_maze_layout[wall_position_to_remove[1]][
                                                              :wall_position_to_remove[0]] + '.' + \
                                                              current_maze_layout[wall_position_to_remove[1]][
                                                              wall_position_to_remove[0] + 1:]
def activate_mrs_hackman():
    global mrs_hackman_actived

    if current_maze_layout == final_maze_layout:
        mrs_hackman_actived = True

def move_mrs_hackman():
    global mrs_hackman_x, mrs_hackman_y, mrs_hackman_direction

    if current_maze_layout == final_hacked_layout and mrs_hackman_actived:
        if mrs_hackman_direction == 'right':
            mrs_hackman_x += GRID_SIZE
        elif mrs_hackman_direction == 'left':
            mrs_hackman_x -= GRID_SIZE
        elif mrs_hackman_direction == 'up':
            mrs_hackman_y -= GRID_SIZE
        elif mrs_hackman_direction == 'down':
            mrs_hackman_y += GRID_SIZE

        # Check for boundaries and adjust direction accordingly
        if mrs_hackman_x >= SCREEN_WIDTH - GRID_SIZE:
            mrs_hackman_y += GRID_SIZE
            mrs_hackman_direction = 'down'
        elif mrs_hackman_x < GRID_SIZE:
            mrs_hackman_y += GRID_SIZE
            mrs_hackman_direction = 'down'

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

        # Draw Ghost
    pygame.draw.rect(screen, RED, (ghost_x, ghost_y, GHOST_SIZE, GHOST_SIZE))
    # Draw the second ghost at its current position
    pygame.draw.rect(screen, BLUE, (ghost_2_x - GHOST_SIZE // 2, ghost_2_y - GHOST_SIZE // 2, GHOST_SIZE, GHOST_SIZE))

    # Drawing score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if current_maze_layout != hacked_maze_layout:
        # Draw terminals
        for i, terminal in enumerate(terminals):
            if i < len(hacked_terminals):
                # Only draw the terminal if it hasn't been hacked
                if not hacked_terminals[i]:
                    pygame.draw.rect(screen, TERMINAL_COLOR,
                             (terminal[0] - TERMINAL_SIZE // 2, terminal[1] - TERMINAL_SIZE // 2, TERMINAL_SIZE,
                              TERMINAL_SIZE))

    if mrs_hackman_actived:
        screen.blit(mrs_hackman_image, (mrs_hackman_x -20, mrs_hackman_y -20))


    # Draw a progress bar when hacking
    if hacking:
        print("Hacking")
        progress_bar_width = (hacking_time / MAX_HACKING_TIME) * TERMINAL_SIZE
        pygame.draw.rect(screen, PROGRESS_BAR_COLOR,
                         (hackman_x - TERMINAL_SIZE // 2, hackman_y - TERMINAL_SIZE // 2 - PROGRESS_BAR_HEIGHT,
                          progress_bar_width, PROGRESS_BAR_HEIGHT))

    keys = pygame.key.get_pressed()

    if not any(keys):

        screen.blit(no_movement_image, (hackman_x-20, hackman_y-20))

    else:
        # Draw Hack-Man
        if keys[pygame.K_LEFT]:
            frame_count = (pygame.time.get_ticks() // 100) % len(left_frames)
            current_image = left_frames[frame_count]
        elif keys[pygame.K_UP]:
            frame_count = (pygame.time.get_ticks() // 100) % len(up_frames)
            current_image = up_frames[frame_count]
        elif keys[pygame.K_DOWN]:
            frame_count = (pygame.time.get_ticks() // 100) % len(down_frames)
            current_image = down_frames[frame_count]
        else:
  #  pygame.draw.circle(screen, YELLOW, (hackman_x, hackman_y), HACKMAN_RADIUS)
            frame_count = (pygame.time.get_ticks() // 100) % len(right_frames)
            current_image = right_frames[frame_count]

        screen.blit(current_image, (hackman_x - 20, hackman_y - 20))

    pygame.display.flip()
    clock.tick(20)
    # Draw Ghost
    pygame.draw.rect(screen, RED, (ghost_x, ghost_y, GHOST_SIZE, GHOST_SIZE))

    #Drawing score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10,10))


def check_exit():
    global hackman_x, hackman_y, ghost_x, ghost_y

    if hackman_y > SCREEN_HEIGHT:
        setup_game_state(final_maze_layout)
        hackman_x = (((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)
        hackman_y = (((SCREEN_HEIGHT // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2)

def main():
    global hackman_x, hackman_y, hackman_old_x, hackman_old_y, terminals, hacked_terminals, current_maze_layout, grid, score, ghost_x, ghost_y, ghost_speed, path_index, ghost_2_x, ghost_2_y, path_index_2
    # Main game loop

    last_movement_time = pygame.time.get_ticks()
    running = True
    frame_count = 0
    hacking = False
    hacking_time = 0
    spacebar_held = False
    ghost_movement_timer = pygame.time.get_ticks()
    ghost_movement_interval = 700
    ghost_speed = 40

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

        if hackman_y > SCREEN_HEIGHT:
            setup_game_state(final_maze_layout)
            hackman_x = ((SCREEN_WIDTH // 2) // GRID_SIZE) * GRID_SIZE + GRID_SIZE // 2
            hackman_y = 20

        # Check for collisions with dots
        for dot in grid[:]:
            if pygame.Rect(dot[0] - DOT_RADIUS, dot[1] - DOT_RADIUS, DOT_RADIUS * 2, DOT_RADIUS * 2).colliderect(
                    (hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS, HACKMAN_RADIUS * 2, HACKMAN_RADIUS * 2)):
                grid.remove(dot)
                score += 100

        # Update Hack-Man's position every 60 frames
        keys = pygame.key.get_pressed()
        activate_mrs_hackman()
        move_mrs_hackman()

        # Store the current position
        hackman_old_x = hackman_x
        hackman_old_y = hackman_y

        # Update Hack-Man's position every 60 frames
        current_time = pygame.time.get_ticks()
        if current_time - last_movement_time >= 10:  # Ensure the frame rate is not zero to avoid division by zero
            movement_speed = GRID_SIZE
        if current_time - last_movement_time >= 350:

            if keys[pygame.K_LEFT]:
                hackman_x -= movement_speed
            if keys[pygame.K_RIGHT]:
                hackman_x += movement_speed
            if keys[pygame.K_UP]:
                hackman_y -= movement_speed
            if keys[pygame.K_DOWN]:
                hackman_y += movement_speed

            if current_time - last_movement_time >= 350:
                print(f"Hack-Man Coordinates: ({hackman_x}, {hackman_y})")

            last_movement_time = current_time

        # Move the ghost along the predefined path
        if (ghost_x, ghost_y) != ghost_path[path_index]:
            # Calculate direction towards the next point in the path
            dx = ghost_path[path_index][0] - ghost_x
            dy = ghost_path[path_index][1] - ghost_y

            # Normalize the direction to maintain constant speed
            norm = max(abs(dx), abs(dy))
            move_x = dx / norm
            move_y = dy / norm

            # Update ghost's position
            ghost_x += move_x * GHOST_SPEED
            ghost_y += move_y * GHOST_SPEED

        else:
            # If the ghost reached the next point in the path, move to the next point
            path_index = (path_index + 1) % len(ghost_path)


        if (ghost_2_x,ghost_2_y) != ghost_2_path[path_index_2]:
            # Calculate direction towards the next point in the path for ghost 2
            dx = ghost_2_path[path_index_2][0] - ghost_2_x
            dy = ghost_2_path[path_index_2][1] - ghost_2_y
            norm = max(abs(dx), abs(dy))
            move_x = dx / norm
            move_y = dy / norm
            ghost_2_x += move_x * GHOST_SPEED
            ghost_2_y += move_y * GHOST_SPEED
        else:
            path_index_2 = (path_index_2 + 1) % len(ghost_2_path)

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
                            if hacked_terminals[0] and final_terminals[0] not in terminals:
                                current_maze_layout = final_hacked_layout
                            else:
                                current_maze_layout = final_maze_layout

            # Check if all terminals are hacked in the final layout
            if all(hacked_terminals) and all(terminal in terminals for terminal in final_terminals):
                # If the current map layout is the final layout, end the game
                if current_maze_layout == final_maze_layout:
                    print("You Win! Game Over")
                    print(f"Final Score: {score}")
                    running = False  # Set running to False to exit the game loop
                    break
                else:
                    # Switch to the hacked maze layout
                    setup_game_state(hacked_maze_layout)
                    pygame.time.delay(500)

            check_exit()
            # Switch to the hacked maze layout
            setup_game_state(hacked_maze_layout)
            pygame.time.delay(500)

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
                        # Draw a progress bar when hacking


        else:
            # Increment hacking time
            hacking_time += 1
            print(f"Hacking time: {hacking_time}, Max Hacking Time: {MAX_HACKING_TIME}")
            # Check if the player is still on the terminal
            terminal_rect = pygame.Rect(terminals[i][0] - TERMINAL_SIZE // 2, terminals[i][1] - TERMINAL_SIZE // 2,
                                        TERMINAL_SIZE, TERMINAL_SIZE)
            if not terminal_rect.colliderect((hackman_x - HACKMAN_RADIUS, hackman_y - HACKMAN_RADIUS,
                                              HACKMAN_RADIUS * 2, HACKMAN_RADIUS * 2)):
                # Player moved away from the terminal, reset hacking process
                hacking = False
                hacking_time = 0
                print("Player moved away - Hacking reset")
            if hacking_time >= MAX_HACKING_TIME:
                print("Executing hacking block")
                # "Hack" the terminal by removing it
                terminals.remove(terminal)
                hacked_terminals[i] = True
                hacking = False
        if current_maze_layout == final_maze_layout:
            remove_wall()
            if len(terminals) <= 0:
                print("you win")
                print(f"Final score: {score}")
                running = False

        # Draw the game screen
        draw_game_screen()

        clock.tick(60)

    # Game over
    print(f"Game over! Score: {score}")

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
