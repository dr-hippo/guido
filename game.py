import pygame
# frequently used types
from pygame import Rect, Vector2
import sys
import config as cfg
import gamestate
import utilities as utils

# game initialisation
pygame.init()
window = pygame.display.set_mode(cfg.RESOLUTION, pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('Guido the Snake Charmer')
clock = pygame.time.Clock()
font = utils.load_font("Nunito-SemiBold", 32)

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # game code here

    window.fill((255, 0, 0))
    utils.render_text("hello world", font, (255, 255, 255), window)

    pygame.display.update()
    clock.tick(cfg.TARGET_FPS)
