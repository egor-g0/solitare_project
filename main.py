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


class EmptyCard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f"data/cards/empty.png")
        self.image = pygame.transform.smoothscale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

    def show(self):
        screen.blit(self.image, self.rect.topleft)


class Card:
    def __init__(self, suit, rank, x, y, face_up=False, column=None):
        self.column = column
        self.x = x
        self.y = y
        self.suit = suit
        self.rank = rank
        self.image = pygame.image.load(f"data/cards/{rank}{suit}.png")
        self.image = pygame.transform.smoothscale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.face_up = face_up
        self.rect = self.image.get_rect(topleft=(x, y))

    def show(self):
        if self.face_up:
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(BACK_IMAGE, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def is_opposite_color(self, other_card):
        return (self.suit in ['C', 'S'] and other_card.suit in ['D', 'H']) or \
            (self.suit in ['D', 'H'] and other_card.suit in ['C', 'S'])

    def is_one_rank_higher(self, other_card):
        return self.rank == other_card.rank - 1


class Foundation:
    def __init__(self, x, y, suit):
        self.x = x
        self.y = y
        self.suit = suit
        self.cards = []
        self.image = pygame.image.load(f"data/cards/empty.png")
        self.image = pygame.transform.smoothscale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))

    def show(self):
        screen.blit(self.image, self.rect.topleft)


def create_deck():
    suits = ['C', 'D', 'H', 'S']
    ranks = list(range(6, 15))
    deck = [Card(suit, rank, 20, 10, face_up=False, column=None) for suit in suits for rank in ranks]
    shuffle(deck)
    return deck


def distribute_cards(deck):
    columns = [[] for _ in range(7)]
    empty_cards = []
    index = 0
    rem_sp = []
    for i in range(7):
        empty_cards.append(EmptyCard(COLUMNS_START_X + i * COLUMN_SPACING, COLUMNS_START_Y))
        for j in range(i + 1):
            card = deck[index]
            rem_sp.append(card)
            x = card.x = COLUMNS_START_X + i * COLUMN_SPACING
            y = card.y = COLUMNS_START_Y + j * CARD_OFFSET_Y
            card.rect.topleft = (x, y)
            if i == j:
                card.face_up = True
            card.column = i
            columns[i].append(card)
            index += 1
    for i in rem_sp:
        deck.remove(i)
    return empty_cards, columns


pygame.init()
pygame.display.set_caption('Косынка')
fps = 120
clock = pygame.time.Clock()
card_sprites = pygame.sprite.Group()

if __name__ == '__main__':
    deck = create_deck()
    window = Window()
    size = width, height = window.x, window.y
    screen = pygame.display.set_mode(size, )
    running = True
    window.show()
    empty_cards, columns = distribute_cards(deck)
    selected_card = None
    start_x, start_y = None, None
    offset_x = 0
    offset_y = 0
    dragging = False

    foundations = []
    for i in range(4):
        foundations.append(
            Foundation((COLUMNS_START_X + 3 * COLUMN_SPACING) + i * COLUMN_SPACING, 10, None))

    while running:
        screen.blit(window.image, (0, 0))
        for i in foundations:
            i.show()
        for i in empty_cards:
            i.show()
        for i in deck:
            i.show()
        for i in columns:
            for j in i:
                j.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:  # начало перетаскивания
                selected_card = None
                mouse_pos = event.pos
                for column in columns:
                    for card in column:
                        if card.is_clicked(mouse_pos) and card.face_up:
                            selected_card = card
                            start_x, start_y = selected_card.x, selected_card.y
                            dragging = True
                            offset_x = selected_card.x - event.pos[0]
                            offset_y = selected_card.y - event.pos[1]

            elif event.type == pygame.MOUSEBUTTONUP and selected_card is not None:  # конец перетаскивания
                sp = []
                for column in columns:
                    sp.append(column[-1].rect if len(column) > 0 else True)
                spp = []
                for i in sp:
                    if i != True:
                        spp.append(selected_card.rect.colliderect(i))
                    else:
                        spp.append(False)

                empty_sp = []
                empty_counter = 0
                for column in columns:
                    empty_sp.append(empty_cards[empty_counter].rect if len(column) == 0 else True)
                    empty_counter += 1
                empty_spp = [selected_card.rect.colliderect(i) for i in empty_sp if i != True]
                len_empty_sp = len([x for x in empty_spp if x == True])

                len_sp = len([x for x in spp if x == True])

                if len_empty_sp >= 1 and selected_card.rank == 13:
                    start_column = selected_card.column
                    new_column = \
                        [i for i in range(len(empty_sp)) if empty_sp[i] != True and i != selected_card.column][0]

                    columns[new_column].append(selected_card)
                    columns[selected_card.column].remove(selected_card)
                    selected_card.column = new_column
                    if len(columns[start_column]) > 0:
                        columns[start_column][-1].face_up = True
                    selected_card.x = empty_cards[new_column].x
                    selected_card.y = COLUMNS_START_Y + (len(columns[new_column]) - 1) * CARD_OFFSET_Y
                elif len_sp > 1:
                    start_column = selected_card.column
                    clll = [i for i in range(len(spp)) if spp[i] == True and i != selected_card.column]
                    new_column = [i for i in range(len(spp)) if spp[i] == True and i != selected_card.column][0]

                    target_card = columns[new_column][-1]

                    # Проверка правил перемещения
                    if (selected_card.is_opposite_color(target_card) and selected_card.is_one_rank_higher(
                            target_card)):
                        columns[new_column].append(selected_card)
                        columns[selected_card.column].remove(selected_card)

                        if len(columns[selected_card.column]) > 0:
                            columns[selected_card.column][-1].face_up = True

                        selected_card.column = new_column
                        selected_card.x = columns[new_column][0].x
                        selected_card.y = COLUMNS_START_Y + (len(columns[new_column]) - 1) * CARD_OFFSET_Y
                    else:
                        selected_card.x = start_x
                        selected_card.y = start_y




                else:
                    selected_card.x = start_x
                    selected_card.y = start_y
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
