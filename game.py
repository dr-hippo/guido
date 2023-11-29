import pygame

# some code won't work if old pygame is used instead of pygame-ce
if not hasattr(pygame, "IS_CE"):
    raise ImportError("Pygame Community Edition (pygame-ce) is required to run this game.")

import sys
import os
import config as cfg
import gamestate
import utilities as utils
import scene

# game initialisation
pygame.mixer.pre_init(channels=16)  # get more channels so sounds don't get dropped
pygame.init()
pygame.display.set_caption('Guido the Snake Charmer')
icon = pygame.image.load(os.path.join(utils.current_path, "images", "topbar-icon.png"))
pygame.display.set_icon(icon)
window = pygame.display.set_mode(cfg.RESOLUTION, pygame.SCALED | pygame.FULLSCREEN)
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

    if cfg.SHOW_FPS:
        utils.render_text("FPS: " + str(round(clock.get_fps(), 2)),
                          utils.load_font("m6x11", 16, pygame.FONT_RIGHT),
                          (0, 0, 0), window, topright=window.get_rect().topright)

    pygame.display.update()
    clock.tick(cfg.TARGET_FPS)
