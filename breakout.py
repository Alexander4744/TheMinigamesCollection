import time
import pygame
import random
import gover
import sys

def breakout(mainMenu, WIDTH, HEIGHT, font):
    # Initialize pygame
    # pygame.init()

    score = 0

    # Constants
    # WIDTH, HEIGHT = 800, 600
    BALL_SPEED = 5
    PADDLE_SPEED = 7
    BRICK_ROWS, BRICK_COLUMNS = 5, 10
    BRICK_WIDTH = WIDTH // BRICK_COLUMNS
    BRICK_HEIGHT = 30

    # Colors
    BLACK = (0, 0, 0)
    RED = (200, 0, 0)
    BLUE = (0, 0, 200)
    GREEN = (0, 200, 0)

    # Create screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout Clone")

    # Paddle
    paddle = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 30, 120, 10)

    # Ball
    ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2, 20, 20)
    ball_dx, ball_dy = BALL_SPEED, -BALL_SPEED

    # Bricks
    bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
              for row in range(BRICK_ROWS) for col in range(BRICK_COLUMNS)]

    start_time = time.time()

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-PADDLE_SPEED, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(PADDLE_SPEED, 0)

        # Ball movement
        ball.move_ip(ball_dx, ball_dy)

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_dx = -ball_dx
        if ball.top <= 0:
            ball_dy = -ball_dy
        if ball.bottom >= HEIGHT:
            ball_dy = -BALL_SPEED
            ball_dx = BALL_SPEED if random.choice([True, False]) else -BALL_SPEED

        # Ball collision with paddle
        if ball.colliderect(paddle):
            ball_dy = -BALL_SPEED
            ball_dx = BALL_SPEED if random.choice([True, False]) else -BALL_SPEED

        # Ball collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy = -ball_dy
                score += 10
                break

        for brick in bricks[:]:
            if brick.bottom >= HEIGHT:
                gover.game_over(score, font, RED, screen, WIDTH, HEIGHT, mainMenu)

        #Lose condition
        if ball.bottom >= HEIGHT:
            gover.game_over(score,font, RED, screen, WIDTH, HEIGHT, mainMenu)

        # Draw bricks
        for brick in bricks:
            pygame.draw.rect(screen, RED, brick)

        # Draw paddle and ball
        pygame.draw.rect(screen, BLUE, paddle)
        pygame.draw.ellipse(screen, GREEN, ball)

        if time.time() - start_time > 20:
            start_time = time.time()
            for brick in bricks:
                brick.y += brick.height + 2

            new_bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
                      for row in range(1) for col in range(BRICK_COLUMNS)]

            bricks.extend(new_bricks)

        # Score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 10))

        pygame.display.flip()
        clock.tick(60)

    time.sleep(3)
    mainMenu()
