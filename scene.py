import pygame
from pygame import Vector2
import utilities as utils
import config as cfg
import time
from snake import Snake, SnakeBlock

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

    def get_time(self):
        return time.time() - self.inittime


class TestScene(Scene):
    """Test scene."""

    def __init__(self):
        super().__init__()
        self.font = utils.load_font("Nunito-SemiBold", 32)
        self.dt = 0
        self.snake = Snake(
            [SnakeBlock(Vector2(0, 0)), SnakeBlock(Vector2(1, 0)), SnakeBlock(Vector2(1, 1)), SnakeBlock(Vector2(2, 1)),
             SnakeBlock(Vector2(2, 2))])

    def update(self, dt):
        self.dt = dt
        # self.snake.advance()

    def render(self, window):
        window.fill((255, 0, 0))
        utils.render_text("hello world", self.font, (255, 255, 255), window)
        utils.render_text("Delta time: " + str(self.dt), self.font, (0, 255, 255), window, (50, 100))
        self.snake.render(window)

    def handle_events(self, events):
        self.snake.handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mouse down")
