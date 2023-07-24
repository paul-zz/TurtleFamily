import sys
import pygame
import yaml

class AssetsLoader:
    def __init__(self):
        self.font_dict = {}
        self.image_dict = {}
        self.sound_dict = {}

    def loadFont(self, name : str, font_dir : str, pointsize : int):
        # Load font from local file as pygame Font object
        self.font_dict[name] = pygame.font.Font(font_dir, pointsize)

    def loadSystemFont(self, name : str, font_name : str, pointsize : int):
        # Load font from system font as pygame Font object
        self.font_dict[name] = pygame.font.SysFont(font_name, pointsize)

    def loadImage(self, name : str,  image_dir : str, mode : str = "alpha"):
        # Load image from local file as pygame image object
        im = pygame.image.load(image_dir)
        if mode == "alpha":
            im.convert_alpha()
        self.image_dict[name] = im
    

    def loadSound(self, name : str, sound_dir : str):
        # Load sound from local file as pygame mixer sound object
        self.sound_dict[name] = pygame.mixer.Sound(sound_dir)

    def loadAllFromList(self, asset_list_dir : str):
        # Load all the resources from a asset list (yaml file)
        with open(asset_list_dir, "r") as f:
            asset_dict = yaml.safe_load(f)
            font_list = asset_dict['fonts']
            image_list = asset_dict['images']
            sound_list = asset_dict['sounds']
            for font in font_list:
                for k, v in font.items():
                    self.loadFont(k, v[0], v[1])
            for image in image_list:
                for k, v in image.items():
                    self.loadImage(k, v)
            for sound in sound_list:
                for k, v in sound.items():
                    self.loadSound(k, v)

    def getFont(self, name : str):
        return self.font_dict[name]
    
    def getImage(self, name : str):
        return self.image_dict[name]
    
    def getSound(self, name : str):
        return self.sound_dict[name]