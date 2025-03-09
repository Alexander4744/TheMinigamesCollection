import pygame
import random
import time
import gover
import sys


def spaceInvaders(mainMenu, WIDTH, HEIGHT, my_font):
    # Initialize pygame
    pygame.init()

    # Constants
    CANNON_STEP = 10
    LASER_SPEED = 10
    LASER_LENGTH = 20
    ALIEN_SPEED = 2.5
    ALIEN_SPAWN_INTERVAL = 1.2
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BACKGROUND_COLOR = (0, 0, 0)

    # Screen setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Space Invaders")
    clock = pygame.time.Clock()

    # Cannon setup

    cannon = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 50, 40, 20)
    cannon_nozzle_1 = pygame.Rect(cannon.x + cannon.width/2 - 10, cannon.y - 10, 5, 15)
    cannon_nozzle_2 = pygame.Rect(cannon.x + cannon.width / 2 + 5, cannon.y - 10, 5, 15)
    cannon_movement = 0

    # Lists to hold lasers and aliens
    lasers = []
    aliens = []

    # Fonts
    font = my_font

    game_timer = time.time()
    alien_timer = 0
    score = 0
    game_running = True

    left_pressed = 0
    right_pressed = 0

    sample_time = time.time()

    while game_running:
        screen.fill(BACKGROUND_COLOR)
        time_elapsed = time.time() - game_timer

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lasers.append(pygame.Rect(cannon.centerx - 10, cannon.top, 5, 10))
                    lasers.append(pygame.Rect(cannon.centerx + 5, cannon.top, 5, 10))
                if event.key == pygame.K_LEFT:
                    left_pressed = 1
                    cannon_movement = -CANNON_STEP
                if event.key == pygame.K_RIGHT:
                    right_pressed = 1
                    cannon_movement = CANNON_STEP

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right_pressed = 0

                if event.key == pygame.K_LEFT:
                    left_pressed = 0

                if left_pressed == 1 and right_pressed == 0:
                    cannon_movement = -CANNON_STEP

                if right_pressed == 1 and left_pressed == 0:
                    cannon_movement = CANNON_STEP

                if left_pressed == 0 and right_pressed == 0:
                    cannon_movement = 0

        # Move cannon
        cannon.x += cannon_movement
        cannon.x = max(0, min(WIDTH - cannon.width, cannon.x))

        cannon_nozzle_1.x = cannon.x + cannon.width / 2 - 10
        cannon_nozzle_2.x = cannon.x + cannon.width / 2 + 5

        # Move lasers
        for laser in lasers[:]:
            laser.y -= LASER_SPEED
            if laser.bottom < 0:
                lasers.remove(laser)

        # Spawn new aliens
        if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
            aliens.append(pygame.Rect(random.randint(20, WIDTH - 20), 0, 30, 30))
            alien_timer = time.time()

        # Move aliens
        for alien in aliens[:]:
            alien.y += ALIEN_SPEED
            if alien.bottom >= HEIGHT:
                game_running = False

        # Check for collisions
        for laser in lasers[:]:
            for alien in aliens[:]:
                if laser.colliderect(alien):
                    lasers.remove(laser)
                    aliens.remove(alien)
                    score += 1
                    break

        # Draw elements
        pygame.draw.rect(screen, WHITE, cannon)
        pygame.draw.rect(screen, WHITE, cannon_nozzle_1)
        pygame.draw.rect(screen, WHITE, cannon_nozzle_2)
        for laser in lasers:
            pygame.draw.rect(screen, RED, laser)
        for alien in aliens:
            pygame.draw.rect(screen, GREEN, alien)

        # Display score
        time_text = font.render(f"Time: {time_elapsed:.1f}s", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)

        screen.blit(time_text, (20, 10))
        screen.blit(score_text, (20, 40))

        if time.time() - sample_time > 10 and ALIEN_SPAWN_INTERVAL > 0.3:
            sample_time = time.time()
            ALIEN_SPAWN_INTERVAL -= 0.1

        if time.time() - sample_time > 10 and ALIEN_SPEED < 5:
            sample_time = time.time()
            ALIEN_SPEED += 0.1


        pygame.display.flip()
        clock.tick(30)

    # Game over screen
    gover.game_over(score,font, RED, screen, WIDTH, HEIGHT, mainMenu)


