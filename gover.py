import sys
import pygame
import time

# game over function
def game_over(score, font, color, game_window, width, height, mainMenu):
    ret_time = 10
    g_over_time = time.time()

    # after 5 seconds we will quit the program
    while ret_time != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if time.time() - g_over_time > 1:
            ret_time -= 1
            g_over_time = time.time()

        # creating font object my_font
        my_font = font
        game_window.fill((0, 0, 0))

        # creating a text surface on which text
        # will be drawn
        game_over_surface = my_font.render(
            'Your Score is : ' + str(score), True, color)

        game_over_title = my_font.render(
                'game over ', True, color)

        # create a rectangular object for the text
        # surface object
        game_over_rect = game_over_surface.get_rect()
        game_over_title_rect = game_over_title.get_rect()

        # setting position of the text
        game_over_rect.midtop = (width / 2, height / 4)
        game_over_title_rect.midtop = (width / 2, height / 6)

        # blit will draw the text on screen
        game_window.blit(game_over_surface, game_over_rect)
        game_window.blit(game_over_title, game_over_title_rect)

        timer_surface = my_font.render(
            f"Return to menu in {ret_time}", True, color)

        timer_rect = timer_surface.get_rect()

        timer_rect.midtop = (width / 2, height / 2)

        game_window.blit(timer_surface, timer_rect)

        pygame.display.update()

    #time.sleep(5)
    #pygame.display.flip()

    # quit the program
    mainMenu()

