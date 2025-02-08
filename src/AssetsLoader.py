import sys
from typing import Optional, Union
import pygame
import pygame.freetype
from pygame.surface import Surface
import yaml

class PygameFontAdapter(pygame.font.Font):
    def __init__(self, freetype_font : pygame.freetype.Font):
        self.freetype_font = freetype_font
        self.freetype_size = freetype_font.size

    def get_linesize(self) -> int:
        return self.freetype_font.get_sized_height(self.freetype_size)
    
    def render(self, text: str | bytes | None, antialias: bool, color, background = None) -> Surface:
        return self.freetype_font.render(text, color, background)[0]


class AssetsLoader:
    font_dict = {}
    image_dict = {}
    sound_dict = {}

    def loadFont(name : str, font_dir : str, pointsize : int):
        # Load font from local file as pygame Font object
        if font_dir.endswith("ttf"):
            AssetsLoader.font_dict[name] = pygame.font.Font(font_dir, pointsize)
        elif font_dir.endswith("otf"):
            AssetsLoader.font_dict[name] = PygameFontAdapter(pygame.freetype.Font(font_dir, pointsize))

    def loadSystemFont(name : str, font_name : str, pointsize : int):
        # Load font from system font as pygame Font object
        AssetsLoader.font_dict[name] = pygame.font.SysFont(font_name, pointsize)

    def loadImage(name : str,  image_dir : str, mode : str = "alpha"):
        # Load image from local file as pygame image object
        im = pygame.image.load(image_dir)
        if mode == "alpha":
            im.convert_alpha()
        AssetsLoader.image_dict[name] = im
    

    def loadSound(name : str, sound_dir : str):
        # Load sound from local file as pygame mixer sound object
        AssetsLoader.sound_dict[name] = pygame.mixer.Sound(sound_dir)

    def setSoundVolume(vol : float):
        # Set sound volume for all sounds in the dict
        for k,v in AssetsLoader.sound_dict.items():
            v.set_volume(vol)

    def loadAllFromList(asset_list_dir : str):
        # Load all the resources from a asset list (yaml file)
        with open(asset_list_dir, "r") as f:
            asset_dict = yaml.safe_load(f)
            font_list = asset_dict['fonts']
            image_list = asset_dict['images']
            sound_list = asset_dict['sounds']
            for font in font_list:
                for k, v in font.items():
                    AssetsLoader.loadFont(k, v[0], v[1])
            for image in image_list:
                for k, v in image.items():
                    AssetsLoader.loadImage(k, v)
            for sound in sound_list:
                for k, v in sound.items():
                    AssetsLoader.loadSound(k, v)

    def getFont(name : str) -> pygame.font.Font:
        return AssetsLoader.font_dict[name]
    
    def getImage(name : str) -> pygame.Surface:
        return AssetsLoader.image_dict[name]
    
    def getSound(name : str) -> pygame.mixer.Sound:
        return AssetsLoader.sound_dict[name]