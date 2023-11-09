import pygame
import sys
import os
import gamestate

def load_image(filetype="png"):
    pass

def load_audio(filetype="mp3"):
    pass

def render_text(string, font, color, surface, rect=None):
    text = font.render(string, True, color)
    surface.blit(text, rect if rect != None else text.get_rect())