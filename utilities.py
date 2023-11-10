import pygame
import sys
import os
import gamestate

if not pygame.get_init():
    pygame.init()

current_path = ""
if getattr(sys, 'frozen', False): # PyInstaller adds this attribute
    # running in a bundle
    current_path = sys._MEIPASS
else:
    # running in normal python environment
    current_path = os.path.dirname(__file__)

def load_image(name, filetype="png"):
    """Load image and return image object"""
    fullname = os.path.join(current_path, "images", name + os.extsep + filetype)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except FileNotFoundError:
        print(f"Cannot find image file at {fullname}")
    return image

def load_audio(name, filetype="mp3"):
    """Load audio and return pygame.mixer.Sound object"""
    fullname = os.path.join(current_path, "audio", name + os.extsep + filetype)
    try:
        audio = pygame.mixer.Sound(fullname)
    except FileNotFoundError:
        print(f"Cannot find audio file at {fullname}")
    return audio

def load_font(name, size, filetype="ttf"):
    """Load font and return font object"""
    return pygame.font.Font(os.path.join(current_path, "fonts", name + os.extsep + filetype), size)

def render_text(string, font, color, surface, rect=None):
    text = font.render(string, True, color)
    surface.blit(text, rect if rect != None else text.get_rect())