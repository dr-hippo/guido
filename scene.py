import pygame
from pygame import Vector2
import gamestate
import utilities as utils
import config as cfg
from snake import Snake
from leveldata import LevelData
from snakecharmer import SnakeCharmer
import sys
import os
import math


class Scene:
    """Base class for game scenes. Inherit and override the provided methods."""

    def __init__(self):
        self.time = 0
        self.font = utils.load_font("m6x11", 16)

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(os.path.join(utils.current_path, "audio", "bgm.mp3"))
            pygame.mixer.music.play(loops=-1)

        gamestate.timescale = 1

    def update(self, dt):
        raise NotImplementedError

    def render(self, window):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError


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
        self.titlefont = utils.load_font("m6x11", 48, align=pygame.FONT_CENTER)
        self.infofont = utils.load_font("m6x11", 32, align=pygame.FONT_CENTER)

    def render(self, window):
        self.draw_bg(window)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # quit if escape key pressed
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def draw_bg(self, window):
        bg_texture = utils.load_image("background")
        for x in range(math.ceil(cfg.RESOLUTION[0] / bg_texture.get_width())):
            for y in range(math.ceil(cfg.RESOLUTION[1] / bg_texture.get_height())):
                window.blit(bg_texture, pygame.Rect(x * bg_texture.get_width(), y * bg_texture.get_height(),
                                                    bg_texture.get_width(), bg_texture.get_height()))


class StartScreen(UIScene):
    def update(self, dt):
        # TODO: Text animations (maybe)
        self.time += dt

    def render(self, window):
        super().render(window)
        utils.render_text("Guido the\nSnake Charmer", self.titlefont,
                          (255, 0, 0), window, centery=100, centerx=window.get_rect().centerx)
        utils.render_text("-SPACE to start-", self.font,
                          (0, 0, 0), window, centery=180, centerx=window.get_rect().centerx)
        utils.render_text("-ESC to quit-", self.font,
                          (0, 0, 0), window, centery=200, centerx=window.get_rect().centerx)

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.load(Level(cfg.LEVELS[0]))


class DeathScreen(UIScene):
    def __init__(self, deathcause, from_level):
        super().__init__()
        self.deathcause = deathcause
        self.from_level = from_level

    def update(self, dt):
        # TODO: Text animations (maybe)
        self.time += dt

    def render(self, window):
        super().render(window)
        utils.render_text(f"RIP", self.titlefont,
                          (255, 0, 0), window, centery=75, centerx=window.get_rect().centerx)
        utils.render_text(self.deathcause, self.infofont,
                          "#444444", window, centery=130, centerx=window.get_rect().centerx)
        utils.render_text("-SPACE to try again-", self.font,
                          (0, 0, 0), window, centery=180, centerx=window.get_rect().centerx)

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.load(Level(self.from_level))


class WinScreen(UIScene):
    def update(self, dt):
        # TODO: Text animations (maybe)
        self.time += dt

    def render(self, window):
        super().render(window)
        utils.render_text(f"You've passed\nall {len(cfg.LEVELS)} levels!", self.titlefont,
                          "#efc636", window, centery=60, centerx=window.get_rect().centerx)
        utils.render_text(f"Visit\ndrhippo.itch.io/guido for\nnews and updates.", self.infofont,
                          (255, 0, 0), window, centery=160, centerx=window.get_rect().centerx)
        utils.render_text("-SPACE to play again-", self.font,
                          (0, 0, 0), window, centery=220, centerx=window.get_rect().centerx)

    def handle_events(self, events):
        super().handle_events(events)

        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
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
        gamestate.timescale = 0

    def update(self, dt):
        self.time += dt
        self.snake.update(dt)
        self.snakecharmer.update(dt)
        for group in self.data.groups.values():
            group.update(dt)

    def render(self, window):
        self.draw_bg(window)
        window.fblits(self.data.get_layout_to_render())
        self.snake.render(window)
        window.blit(self.snakecharmer.image, self.snakecharmer.rect)

        # show level index/name and controls hint for the first 4 seconds
        if self.time < 4:
            utils.render_text(f"{self.index + 1}/{len(cfg.LEVELS)}: {self.data.title}",
                              self.font, (255, 255, 255), window,
                              top=2, centerx=window.get_rect().centerx)
            utils.render_text("C to see controls",
                              self.font, (255, 255, 255), window,
                              bottom=window.get_rect().bottom + 2, centerx=window.get_rect().centerx)

        # if the player hasn't made any inputs yet, show prompt
        if self.time == 0:
            utils.render_text("Press any key to start level",
                              self.font, "#ffffff", window,
                              centerx=window.get_rect().centerx,
                              centery=window.get_rect().centery + 2)

        # show controls help text if C is pressed
        if pygame.key.get_pressed()[pygame.K_c]:
            controls_help = """Arrows: Snake
W, A, D: Guido
R: Restart level
ESC: Back to menu"""
            utils.render_text(controls_help,
                              self.font, (255, 255, 255), window,
                              top=2, left=2)

    def draw_bg(self, window):
        window.fill(pygame.Color("#bce0f5"))

    def handle_events(self, events):
        for event in events:
            # don't start game if player's just trying to look at controls
            if event.type == pygame.KEYDOWN and event.key != pygame.K_c:
                gamestate.timescale = 1
                if event.key == pygame.K_ESCAPE:
                    self.manager.load(StartScreen())

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
