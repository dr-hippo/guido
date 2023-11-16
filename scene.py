import pygame
from pygame import Vector2
import gamestate
import utilities as utils
import config as cfg
import time
from snake import Snake, SnakeBlock
from leveldata import LevelData
from snakecharmer import SnakeCharmer
import json


class Scene:
    """Base class for game scenes. Inherit and override the provided methods."""

    def __init__(self):
        self.inittime = time.time()
        self.font = utils.load_font("Nunito-SemiBold", 18)

    def update(self, dt):
        raise NotImplementedError

    def render(self, window):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

    def get_time(self):
        return time.time() - self.inittime


class SceneManager:
    def __init__(self):
        self.load(gamestate.current_scene)

    def load(self, scene):
        """Loads the given scene."""
        gamestate.current_scene = scene
        scene.manager = self


class TestScene(Scene):
    """Test scene."""

    def __init__(self):
        super().__init__()
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
        utils.render_text("Delta time: " + str(self.dt), self.font, (0, 255, 255), window,
                          center=window.get_rect().center)
        self.snake.render(window)

    def handle_events(self, events):
        self.snake.handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.load(StartScreen())


class StartScreen(Scene):
    def __init__(self):
        super().__init__()
        # TODO: Instantiate title text and start button
        self.titlefont = utils.load_font("Nunito-SemiBold", 36, align=pygame.FONT_CENTER)

    def update(self, dt):
        # TODO: Text animations (maybe)
        pass

    def render(self, window):
        # TODO: Render title text and button
        window.fill((255, 255, 255))
        utils.render_text("Guido the\nSnake Charmer", self.titlefont,
                          (255, 0, 0), window, top=50, centerx=window.get_rect().centerx)
        utils.render_text("-Click anywhere to start-", self.font,
                          (0, 0, 0), window, top=180, centerx=window.get_rect().centerx)
        pass

    def handle_events(self, events):
        # TODO: Pipe mousedown events to button(s) so they can be triggered
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.load(Level())


class Level(Scene):
    def __init__(self):
        super().__init__()
        self.data = LevelData("tutorial")
        self.snake = Snake(
            [SnakeBlock(Vector2(0, 0)), SnakeBlock(Vector2(1, 0)), SnakeBlock(Vector2(1, 1)), SnakeBlock(Vector2(2, 1)),
             SnakeBlock(Vector2(2, 2))])
        self.snakecharmer = SnakeCharmer(self.data.playerspawn)

    def update(self, dt):
        # TODO: Update snake and snakecharmer
        pass

    def render(self, window):
        # TODO: Render snake and player
        window.fill(pygame.Color("skyblue"))
        self.draw_bg()
        window.fblits(self.data.get_layout_to_render())
        self.snake.render(window)
        window.blit(self.snakecharmer.image, self.snakecharmer.rect)

    def draw_bg(self):
        pass

    def handle_events(self, events):
        for event in events:
            self.snake.handle_events(events)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.load(TestScene())
