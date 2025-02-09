import os
import sys
import pygame
import random

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

pygame.init()
pygame.display.set_caption('Косынка')
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
fps = 50
clock = pygame.time.Clock()
cards = []
fon = load_image('fon.jpg')
card_sprites = pygame.sprite.Group()
class Window:
    def __init__(self):
        pass

    def show(self):
        image = pygame.image.load('fon.jpg')
        screen.blit(image, (0, 0))

cards = []

class Card(pygame.sprite.Sprite):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image = load_image("cards/" + str(rank) + '.' + str(suit) + ".jpg")
        self.rect = self.image.get_rect()

    def show(self, a, b):
        self.rect.x = a
        self.rect.y = b
        print(self.rect)



def generate_cards():
    for i in range(1, 13):
        for j in range(1, 4):
            card = Card(j, i)
            cards.append(card)
    k = 0
    for i in range(1, 8):
        for j in range(i):

            cards[k].show(65 + 110 * (i - 1), 210 + 20 * j)
            k += 1

if __name__ == '__main__':
    window = Window()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 255, 255))
        generate_cards()
        window.show()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
