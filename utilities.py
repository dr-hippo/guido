import pygame
import sys
import os
import gamestate

if not pygame.get_init():
    pygame.init()

current_path = ""
if getattr(sys, 'frozen', False):  # PyInstaller adds this attribute
    # running in a bundle
    current_path = sys._MEIPASS
else:
    # running in normal python environment
    current_path = os.path.dirname(__file__)


def load_image(name, *subfolders, filetype="png"):
    """Load image and return image object"""
    if subfolders:
        fullname = os.path.join(current_path, "images",
                                os.path.join(*subfolders),
                                name + os.extsep + filetype)

    else:
        fullname = os.path.join(current_path, "images",
                                name + os.extsep + filetype)

    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        return image
    except FileNotFoundError:
        print(f"Cannot find image file at {fullname}")


def load_audio(name, *subfolders, filetype="mp3"):
    """Load audio and return pygame.mixer.Sound object"""
    if subfolders:
        fullname = os.path.join(current_path, "audio",
                                os.path.join(*subfolders),
                                name + os.extsep + filetype)

    else:
        fullname = os.path.join(current_path, "audio",
                                name + os.extsep + filetype)
    try:
        audio = pygame.mixer.Sound(fullname)
        return audio
    except FileNotFoundError:
        print(f"Cannot find audio file at {fullname}")


def load_font(name, size, align=pygame.FONT_LEFT, filetype="ttf"):
    """Load font and return font object"""
    if name:
        font = pygame.font.Font(os.path.join(current_path, "fonts", name + os.extsep + filetype), size)
    else:
        font = pygame.font.Font(None, size)

    font.align = align
    return font


def render_text(string, font, color, surface, **kwargs):
    """Render string in colored font on surface, and position it according to keyword arguments."""
    text = font.render(string, True, color)
    surface.blit(text, text.get_rect(**kwargs))
