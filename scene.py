import pygame
import utilities as utils
import config as cfg
import time

class Scene:
    """Base class for game scenes. Inherit and override the provided methods."""
    def __init__(self):
        self.inittime = time.time()

    def update(self, window, dt):
        raise NotImplementedError

    def render(self, window):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

class TestScene(Scene):
    """Test scene."""
    def __init__(self):
        super().__init__()
        self.font = utils.load_font("Nunito-SemiBold", 32)
        self.dt = 0

    def update(self, dt):
        self.dt = dt

    def render(self, window):
        window.fill((255, 0, 0))
        utils.render_text("hello world", self.font, (255, 255, 255), window)
        utils.render_text("Delta time: " + str(self.dt / 1000), self.font, (0, 255, 255), window, (50, 100))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse down")
