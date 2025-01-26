import os
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((900, 800))
fps = 60
clock = pygame.time.Clock()



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

class Window:
    def __init__(self):
        pass

    def show(self):
        image = pygame.image.load('fon.jpg')
        screen.blit(image, (0, 0))
        '''нужен код для показывания очков, набранных игроком'''

class Card:
    pass
def generate_cards():
    for i in range(1, 8):
        for j in range(i):
            pygame.draw.rect(screen, (100, 100, 100), (65 + 110 * (i - 1), 210 + 20 * j, 70, 120))
            '''вместо прямоугольников нужно реализовать генерацию карт'''

if __name__ == '__main__':
    window = Window()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 255, 255))
        window.show()
        generate_cards()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
