import pygame
from pygame import Vector2
import gamestate
import utilities as utils
import config as cfg
import time
from snake import Snake
from leveldata import LevelData
from snakecharmer import SnakeCharmer
import sys
import os


class Scene:
    """Base class for game scenes. Inherit and override the provided methods."""

    def __init__(self):
        self.inittime = time.time()
        self.font = utils.load_font("Nunito-SemiBold", 20)

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(utils.current_path, "audio", "bgm.wav"))
            pygame.mixer.music.play(loops=-1)

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

    def reload_level(self):
        if type(gamestate.current_scene) != Level:
            raise TypeError(f"Must be in a level to reload: Scene type is {type(gamestate.current_scene)}")

        self.load(Level(gamestate.current_scene.name))


class UIScene(Scene):
    def __init__(self):
        super().__init__()
        self.titlefont = utils.load_font("Nunito-SemiBold", 36, align=pygame.FONT_CENTER)
        self.infofont = utils.load_font("Nunito-SemiBold", 20, align=pygame.FONT_CENTER)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # quit if escape key pressed
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


class StartScreen(UIScene):
    def update(self, dt):
        # TODO: Text animations (maybe)
        pass

    def render(self, window):
        window.fill((255, 255, 255))
        utils.render_text("Guido the\nSnake Charmer", self.titlefont,
                          (255, 0, 0), window, top=50, centerx=window.get_rect().centerx)
        utils.render_text("-Any key to start-", self.font,
                          (0, 0, 0), window, top=180, centerx=window.get_rect().centerx)
        utils.render_text("-Esc to quit-", self.font,
                          (0, 0, 0), window, top=200, centerx=window.get_rect().centerx)

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.load(Level(cfg.LEVELS[0]))


class DeathScreen(UIScene):
    def __init__(self, deathcause, from_level):
        super().__init__()
        self.deathcause = deathcause
        self.from_level = from_level

    def update(self, dt):
        # TODO: Text animations (maybe)
        pass

    def render(self, window):
        window.fill((255, 255, 255))
        utils.render_text(f"RIP Guido + Snake", self.titlefont,
                          (255, 0, 0), window, top=60, centerx=window.get_rect().centerx)
        utils.render_text(self.deathcause, self.font,
                          (128, 128, 128), window, top=120, centerx=window.get_rect().centerx)
        utils.render_text("-Any key to respawn-", self.font,
                          (0, 0, 0), window, top=160, centerx=window.get_rect().centerx)

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.load(Level(self.from_level))


class WinScreen(UIScene):
    def update(self, dt):
        # TODO: Text animations (maybe)
        pass

    def render(self, window):
        window.fill((255, 255, 255))
        utils.render_text(f"Well done! You've\npassed all {len(cfg.LEVELS)} levels!", self.titlefont,
                          "#efc636", window, top=20, centerx=window.get_rect().centerx)
        utils.render_text(f"Visit\ndrhippo.itch.io/guido\nfor news and updates.", self.infofont,
                          (255, 0, 0), window, top=120, centerx=window.get_rect().centerx)
        utils.render_text("-Any key to go back to start-", self.font,
                          (0, 0, 0), window, top=210, centerx=window.get_rect().centerx)

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.load(StartScreen())


class Level(Scene):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.index = cfg.LEVELS.index(self.name)
        self.data = LevelData(self, name)
        self.snake = Snake(self)
        playerspawn_world_space = Vector2((self.data.playerspawn.x + 0.5) * cfg.GRIDSIZE,  # center of cell vertically
                                          (self.data.playerspawn.y + 1) * cfg.GRIDSIZE)  # bottom of cell horizontally
        self.snakecharmer = SnakeCharmer(self, playerspawn_world_space)

    def update(self, dt):
        self.snake.update(dt)
        self.snakecharmer.update(dt)
        for group in self.data.groups.values():
            group.update(dt)

    def render(self, window):
        self.draw_bg(window)
        window.fblits(self.data.get_layout_to_render())
        self.snake.render(window)
        window.blit(self.snakecharmer.image, self.snakecharmer.rect)

        if self.get_time() < 3:
            utils.render_text(f"{self.index + 1}: {self.data.title}",
                              utils.load_font("Nunito-SemiBold", 25), (255, 255, 255), window,
                              bottomleft=window.get_rect().bottomleft)

    def draw_bg(self, window):
        window.fill(pygame.Color("#bce0f5"))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # reload key
                if event.key == pygame.K_r:
                    self.manager.reload_level()

                # cheat key
                if event.key == pygame.K_k:
                    self.to_nextlevel()

            self.snake.handle_events(events)
            self.snakecharmer.handle_events(events)

    def to_nextlevel(self):
        if self.index == len(cfg.LEVELS) - 1:
            self.manager.load(WinScreen())

        else:
            self.manager.load(Level(cfg.LEVELS[self.index + 1]))

    def on_death(self, cause="Mystery Death"):
        self.manager.load(DeathScreen(cause, self.name))
