import pygame, sys, random

# Initializing game display and fps
pygame.init()
screen = pygame.display.set_mode((576, 1024))
FPS = 60
FramePerSecond = pygame.time.Clock()

# create score counter
font = pygame.font.SysFont("comicsansms", 48)
counter = 0

# Create the start screen
startScreen = pygame.image.load("assets/message.png").convert_alpha()
startScreen = pygame.transform.scale2x(startScreen)

# Creating background and scaling it to screen size
background = pygame.image.load("assets/background-night.png").convert()
background = pygame.transform.scale(background, screen.get_size())
background_x = 0

# Creating ground and scaling it to screen width
ground = pygame.image.load("assets/base.png").convert()
ground = pygame.transform.scale(ground, (screen.get_width(), ground.get_height()))
ground_x = 0.0

# Import all bird images for animation
bird_down = pygame.transform.scale2x(pygame.image.load("assets/redbird-downflap.png").convert())
bird_mid = pygame.transform.scale2x(pygame.image.load("assets/redbird-midflap.png").convert())
bird_up = pygame.transform.scale2x(pygame.image.load("assets/redbird-upflap.png").convert())
bird_all_images = [bird_up, bird_mid, bird_down]

# Creating bird
bird = bird_all_images[0]
bird_rect = bird.get_rect(center=(100, screen.get_height() / 2))
bird_move = 0

# Create event to animate bird
BIRDEVENT = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDEVENT, 200)
bird_counter = 0

# Creating pipe
pipe = pygame.image.load("assets/pipe-green.png")
pipe = pygame.transform.scale2x(pipe)
pipe_choices = [750, 850, 950, 1050, 1150]

# Create the event of a pipe spawning every 1 second
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2000)
pipes = []

# Create collision boolean
collision = True


# define function to increase score
def add_score(counter, pipes):
    # create text to show
    text = str(int(counter / 2))
    # create score render
    text = font.render(text, True, (255, 255, 255))
    # remder the score
    screen.blit(text, (screen.get_width() / 2, 100))

    # Go over pipes to check if score is added
    for pipe_i in pipes:
        if bird_rect.centerx == pipe_i.centerx:
            # Increase counter
            counter += 1

    return counter

# Create function to check for collision
def check_collision():
    # Check for collision with sky or ground
    if bird_rect.centery < 15 or bird_rect.centery > screen.get_height() - ground.get_height():
        return True
    # Check for collision with pipe
    for pipe_i in pipes:
        if bird_rect.colliderect(pipe_i):
            return True
    return False


# Define the function to crete new pipes
def create_pipe():
    pipe_height = random.choice(pipe_choices)
    pipe_rect_normal = pipe.get_rect(center=(700, pipe_height))
    pipe_rect_flip = pipe.get_rect(center=(700, pipe_height - 1000))
    return pipe_rect_normal, pipe_rect_flip


# Draw pipes to the screen
def draw_pipes(pipes):
    for pipe_i in pipes:
        if pipe_i.bottom >= 1024:
            screen.blit(pipe, pipe_i)
        else:
            new_pipe = pygame.transform.flip(pipe, False, True)
            screen.blit(new_pipe, pipe_i)


def move_pipes(pipes):
    for pipe_i in pipes:
        pipe_i.centerx -= 3


# main game loop
while True:
    # executing every event
    for event in pygame.event.get():
        # Close button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Check for input
        if event.type == pygame.KEYDOWN:
            # Check for spacebar
            if event.key == pygame.K_SPACE:
                bird_move = 0
                bird_move -= 15
                collision = False
        # Check for left click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                bird_move = 0
                bird_move -= 15
                collision = False
        # Check to spawn a pipe
        if event.type == SPAWNPIPE and collision is not True:
            # Call the function to spawn a pipe
            pipes.extend(create_pipe())
        # Check to animate bird
        if event.type == BIRDEVENT:
            bird = bird_all_images[bird_counter % 3]
            bird_counter += 1

    # Clear the screen
    screen.fill((0, 0, 0))

    # add background to view
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + screen.get_width(), 0))

    # Make the background move left
    background_x -= 0.3

    # put the background back to the very left
    if abs(background_x) >= screen.get_width():
        background_x = 0

    # Check for collision
    if collision is not True:
        # Draw bird to screen
        screen.blit(bird, bird_rect)

        # Draw pipes to the screen
        draw_pipes(pipes)

        # Move pipes to the left
        move_pipes(pipes)

        # Call the check collision function
        collision = check_collision()

        # Make the bird fall down
        bird_move += 1
        bird_rect.centery += bird_move

        # increase score
        counter = add_score(counter, pipes)

    # Otherwise reset the game
    else:

        # reset score
        counter = 0

        # remove all the pipes
        pipes = []

        # reset the birds position
        bird_rect.centery = screen.get_height() / 2

        # Add the start screen
        screen.blit(startScreen, ((screen.get_width() / 2) - (startScreen.get_width() / 2),
                                  (screen.get_height() / 2) - (startScreen.get_height() / 2)))

    # add ground to view
    screen.blit(ground, (ground_x, screen.get_height() - ground.get_height()))
    screen.blit(ground, (ground_x + screen.get_width(), screen.get_height() - ground.get_height()))

    # Make the ground move left
    ground_x -= 3

    # Put the ground back to the very right to make animation smooth
    if abs(ground_x) == screen.get_width():
        ground_x = 0

    # Progress in game loop
    FramePerSecond.tick(FPS)
    pygame.display.update()
