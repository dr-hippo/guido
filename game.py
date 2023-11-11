import pygame
# frequently used types
from pygame import Rect, Vector2
import sys
import config as cfg
import gamestate
import utilities as utils
import scene
import snake

# game initialisation
pygame.init()
window = pygame.display.set_mode(cfg.RESOLUTION, pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('Guido the Snake Charmer')
clock = pygame.time.Clock()
manager = scene.SceneManager()

# set timers
pygame.time.set_timer(snake.SNAKE_ADVANCE, cfg.SNAKE_ADVANCE_INTERVAL)

# main loop
while True:
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()

    gamestate.current_scene.handle_events(pygame.event.get())

    # game code
    gamestate.current_scene.update(clock.get_time() / 1000 * gamestate.timescale)
    gamestate.current_scene.render(window)

    pygame.display.update()
    clock.tick(cfg.TARGET_FPS)
