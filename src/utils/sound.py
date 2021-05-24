import time
import pygame


class Sound:
    def __init__(self, path) -> None:
        pygame.mixer.init()
        self.s = pygame.mixer.Sound(path)

    def play(self):
        self.s.play()
