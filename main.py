import os
import sys
import pygame
from random import shuffle

CARD_WIDTH, CARD_HEIGHT = 120, 175
COLUMNS_START_X = 20
COLUMNS_START_Y = 250
COLUMN_SPACING = 150
CARD_OFFSET_Y = 30
BACK_IMAGE = pygame.image.load("data/cards/back.png")
BACK_IMAGE = pygame.transform.smoothscale(BACK_IMAGE, (CARD_WIDTH, CARD_HEIGHT))


class Window:
    def __init__(self):
        self.image = pygame.image.load('data/fon2.jpg')
        self.x = self.image.get_width()
        self.y = self.image.get_height()

    def show(self):
        screen.blit(self.image, (0, 0))


class Card:
    def __init__(self, suit, rank, x, y, face_up=False):
        self.x = x
        self.y = y
        self.suit = suit
        self.rank = rank
        self.image = pygame.image.load(f"data/cards/{rank}{suit}.png")
        self.image = pygame.transform.smoothscale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.face_up = face_up
        self.rect = self.image.get_rect(topleft=(x, y))

    def show(self):
        # print(self.rect)
        if self.face_up:
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(BACK_IMAGE, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def create_deck():
    suits = ['C', 'D', 'H', 'S']
    ranks = list(range(6, 15))
    deck = [Card(suit, rank, 20, 10, face_up=False) for suit in suits for rank in ranks]
    shuffle(deck)
    return deck


def distribute_cards(deck):
    columns = [[] for _ in range(7)]
    index = 0
    for i in range(7):
        for j in range(i + 1):
            card = deck[index]
            x = card.x = COLUMNS_START_X + i * COLUMN_SPACING
            y = card.y = COLUMNS_START_Y + j * CARD_OFFSET_Y
            card.rect.topleft = (x, y)
            if i == j:
                card.face_up = True
            columns[i].append(card)
            index += 1
    return columns


pygame.init()
pygame.display.set_caption('Косынка')
fps = 120
clock = pygame.time.Clock()
card_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    deck = create_deck()
    window = Window()
    size = width, height = window.x, window.y
    screen = pygame.display.set_mode(size)
    running = True
    window.show()
    columns = distribute_cards(deck)
    selected_card = None
    offset_x = 0
    offset_y = 0
    dragging = False

    while running:

        screen.blit(window.image, (0, 0))
        for i in deck:
            i.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:  # начало перетаскивания
                mouse_pos = event.pos
                for column in columns:
                    for card in reversed(column):
                        if card.is_clicked(mouse_pos) and card.face_up:
                            selected_card = card
                            dragging = True
                            offset_x = selected_card.x - event.pos[0]
                            offset_y = selected_card.y - event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP:  # конец перетаскивания
                dragging = False

            elif event.type == pygame.MOUSEMOTION:  # перетаскивание
                if dragging:
                    selected_card.x = event.pos[0] + offset_x
                    selected_card.y = event.pos[1] + offset_y

        if selected_card is not None:
            selected_card.rect.x = selected_card.x
            selected_card.rect.y = selected_card.y
            screen.blit(selected_card.image, selected_card.rect.topleft)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
