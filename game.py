import pygame

# some code won't work if old pygame is used instead of pygame-ce
if not getattr(pygame, "IS_CE", False):
    raise ImportError(
        """Pygame Community Edition (pygame-ce) is required for this game to run correctly from source.""")

import sys
import config as cfg
import gamestate
import utilities as utils
import scene

# game initialisation
pygame.init()
window = pygame.display.set_mode(cfg.RESOLUTION, pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('Guido the Snake Charmer')
pygame.display.set_icon(utils.load_image("topbar-icon"))
clock = pygame.time.Clock()
manager = scene.SceneManager()

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
