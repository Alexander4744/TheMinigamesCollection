import sys
import pygame
import time
import random
import gover

#Snake Code

# displaying Score function
def show_score(choice, color, font, size, score, game_window):
    # creating font object score_font
    score_font = font

    # create the display surface object
    # score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # create a rectangular object for the text
    # surface object
    score_rect = score_surface.get_rect()

    # displaying text
    game_window.blit(score_surface, score_rect)

def snakeGame(mainMenu, width, height, font):
    snake_speed = 5

    # Grid block pixel size
    grid_block = 40

    # defining colors
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    dgreen = pygame.Color(0, 100, 0)
    blue = pygame.Color(0, 0, 255)

    # Initialise game window
    pygame.display.set_caption('Snake')
    game_window = pygame.display.set_mode((width, height))

    # defining snake default position
    snake_x = 10*grid_block
    snake_y = 5*grid_block
    snake_position = [snake_x, snake_y]

    # defining first 4 blocks of snake body
    snake_body = [[snake_x, snake_y],
                  [snake_x - grid_block, snake_y],
                  [snake_x - 2*grid_block, snake_y],
                  [snake_x - 3*grid_block, snake_y]
                  ]
    # fruit position
    fruit_position = [random.randrange(1, (width // grid_block)) * grid_block,
                      random.randrange(1, (height // grid_block)) * grid_block]

    fruit_spawn = True

    # setting default snake direction towards
    # right
    direction = 'RIGHT'
    change_to = direction

    # initial score
    score = 0

    # Main Function
    while True:

        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= grid_block
        if direction == 'DOWN':
            snake_position[1] += grid_block
        if direction == 'LEFT':
            snake_position[0] -= grid_block
        if direction == 'RIGHT':
            snake_position[0] += grid_block

        # Snake body growing mechanism
        # if fruits and snakes collide then scores
        # will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_x = random.randrange(1, (width // grid_block)) * grid_block
            fruit_y = random.randrange(1, (height // grid_block)) * grid_block
            fruit_ok = True

            for body in snake_body:
                if body[0] == fruit_x and body[1] == fruit_y:
                    fruit_ok = False
                    break

            while fruit_ok == False:
                fruit_x = random.randrange(1, (width // grid_block)) * grid_block
                fruit_y = random.randrange(1, (height // grid_block)) * grid_block
                fruit_ok = True
                for body in snake_body:
                    if body[0] == fruit_x and body[1] == fruit_y:
                        fruit_ok = False
                        break

            fruit_position = [fruit_x, fruit_y]

        fruit_spawn = True
        game_window.fill(black)

        # Draw the snake
        for pos in snake_body:
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 5*grid_block/6, 5*grid_block/6))


        # Draw the fruit
        pygame.draw.rect(game_window, red, pygame.Rect(
            fruit_position[0], fruit_position[1], 5*grid_block/6, 5*grid_block/6))

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > width - grid_block:
            gover.game_over(score, font, red, game_window, width, height, mainMenu)
        if snake_position[1] < 0 or snake_position[1] > height - grid_block:
            gover.game_over(score, font, red, game_window, width, height, mainMenu)

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                gover.game_over(score, font, red, game_window, width, height, mainMenu)

        # displaying score continuously
        show_score(1, white, font, 20, score, game_window)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        pygame.time.Clock().tick(snake_speed)
