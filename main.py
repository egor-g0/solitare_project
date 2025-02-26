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
        self.back_image = BACK_IMAGE
        self.face_up = face_up
        self.rect = self.image.get_rect(topleft=(x, y))

    def show(self):
        if self.face_up:
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(self.back_image, self.rect.topleft)

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
        self.image = pygame.image.load(f"data/cards/foundation_empty.png")
        self.image = pygame.transform.smoothscale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))

    def show(self):
        screen.blit(self.image, self.rect.topleft)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


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
    for i in deck:
        i.back_image = pygame.image.load(f"data/cards/column_card.png")
        i.back_image = pygame.transform.smoothscale(i.back_image, (CARD_WIDTH, CARD_HEIGHT))
    selected_card = None
    selected_cards = []
    start_x, start_y = None, None
    offset_x = 0
    offset_y = 0
    dragging = False
    flag = False
    f_num = False

    foundations = []
    for i in range(4):
        foundations.append(
            Foundation((COLUMNS_START_X + 3 * COLUMN_SPACING) + i * COLUMN_SPACING, 10, None))

    while running:
        screen.blit(window.image, (0, 0))
        for i in foundations:
            i.show()
            for j in i.cards:
                screen.blit(j.image, j.rect.topleft)

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
                selected_cards = []
                mouse_pos = event.pos
                for column in columns:
                    for card in reversed(column):
                        if card.is_clicked(mouse_pos) and card.face_up:
                            selected_card = card
                            if columns[selected_card.column].index(selected_card) != len(
                                    columns[selected_card.column]) - 1:
                                flag = True
                                selected_cards = columns[selected_card.column][
                                                 columns[selected_card.column].index(selected_card):]

                            start_x, start_y = selected_card.x, selected_card.y
                            dragging = True
                            offset_x = selected_card.x - event.pos[0]
                            offset_y = selected_card.y - event.pos[1]
                            break
                if selected_card is None:
                    for i in foundations:
                        if len(i.cards) > 0:
                            if i.is_clicked(mouse_pos):
                                selected_card = i.cards[-1]
                                if selected_card.rank == 14:
                                    selected_card = None
                                    break
                                f_num = foundations.index(i)
                                print(selected_card.rank)
                                start_x, start_y = selected_card.x, selected_card.y
                                dragging = True
                                offset_x = selected_card.x - event.pos[0]
                                offset_y = selected_card.y - event.pos[1]
                                selected_card.column = None
                                break


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

                if selected_card.column is None:
                    clll = [i for i in range(len(spp)) if spp[i] == True]
                    new_column = [i for i in range(len(spp)) if spp[i] == True][0]

                    target_card = columns[new_column][-1]

                    # Проверка правил перемещения
                    if (selected_card.is_opposite_color(target_card) and selected_card.is_one_rank_higher(
                            target_card) and target_card.rank != 14):
                        columns[new_column].append(selected_card)
                        foundations[f_num].cards.remove(selected_card)
                        selected_card.column = new_column
                        selected_card.x = columns[new_column][0].x
                        selected_card.y = COLUMNS_START_Y + (len(columns[new_column]) - 1) * CARD_OFFSET_Y
                    pass

                elif len_empty_sp >= 1 and selected_card.rank == 13:
                    start_column = selected_card.column
                    new_column = \
                        [i for i in range(len(empty_sp)) if empty_sp[i] != True and i != selected_card.column][0]
                    if len(columns[selected_card.column]) > 0:
                        columns[selected_card.column][
                            columns[selected_card.column].index(selected_card) - 1].face_up = True

                    columns[new_column].append(selected_card)
                    columns[selected_card.column].remove(selected_card)

                    if len(columns[start_column]) > 0:
                        columns[start_column][-1].face_up = True
                    selected_card.column = new_column
                    selected_card.x = empty_cards[new_column].x
                    selected_card.y = COLUMNS_START_Y + (len(columns[new_column]) - 1) * CARD_OFFSET_Y
                    if flag:
                        j = 0
                        for i in selected_cards[1:]:
                            columns[new_column].append(i)
                            columns[i.column].remove(i)
                            i.column = new_column
                            i.x = columns[new_column][0].x
                            i.y = selected_card.y + CARD_OFFSET_Y * (1 + j)
                            j += 1

                elif len_sp > 1:
                    start_column = selected_card.column
                    clll = [i for i in range(len(spp)) if spp[i] == True and i != selected_card.column]
                    new_column = [i for i in range(len(spp)) if spp[i] == True and i != selected_card.column][0]

                    target_card = columns[new_column][-1]

                    # Проверка правил перемещения
                    if (selected_card.is_opposite_color(target_card) and selected_card.is_one_rank_higher(
                            target_card) and target_card.rank != 14):
                        if len(columns[selected_card.column]) > 0:
                            columns[selected_card.column][
                                columns[selected_card.column].index(selected_card) - 1].face_up = True

                        columns[new_column].append(selected_card)
                        columns[selected_card.column].remove(selected_card)

                        selected_card.column = new_column
                        selected_card.x = columns[new_column][0].x
                        selected_card.y = COLUMNS_START_Y + (len(columns[new_column]) - 1) * CARD_OFFSET_Y
                        if flag:
                            j = 0
                            for i in selected_cards[1:]:
                                columns[new_column].append(i)
                                columns[i.column].remove(i)
                                i.column = new_column
                                i.x = columns[new_column][0].x
                                i.y = target_card.y + CARD_OFFSET_Y + CARD_OFFSET_Y * (1 + j)
                                j += 1



                    else:
                        selected_card.x = start_x
                        selected_card.y = start_y
                        for j, i in enumerate(selected_cards[1:]):
                            i.x = start_x
                            i.y = start_y + CARD_OFFSET_Y * (j + 1)


                else:
                    g = False
                    if columns[selected_card.column].index(selected_card) == len(columns[selected_card.column]) - 1:
                        for i in foundations:
                            if selected_card.rect.colliderect(i.rect):
                                if len(i.cards) == 0 and selected_card.rank != 14:
                                    continue
                                if (len(i.cards) == 0 and selected_card.rank == 14) or (selected_card.suit == i.cards[
                                    -1].suit and selected_card.rank == i.cards[-1].rank + 1) or (
                                        i.cards[-1].rank == 14 and selected_card.rank == 6 and selected_card.suit ==
                                        i.cards[-1].suit):
                                    if len(columns[selected_card.column]) > 0:
                                        columns[selected_card.column][
                                            columns[selected_card.column].index(selected_card) - 1].face_up = True
                                    i.cards.append(selected_card)
                                    columns[selected_card.column].remove(selected_card)
                                    selected_card.x = i.x
                                    selected_card.y = i.y
                                    selected_card.column = False
                                    g = True
                                    break

                    if not g:
                        selected_card.x = start_x
                        selected_card.y = start_y
                        for j, i in enumerate(selected_cards[1:]):
                            i.x = start_x
                            i.y = start_y + CARD_OFFSET_Y * (j + 1)
                dragging = False


            elif event.type == pygame.MOUSEMOTION:  # перетаскивание
                if dragging:
                    selected_card.x = event.pos[0] + offset_x
                    selected_card.y = event.pos[1] + offset_y

                    for j, i in enumerate(selected_cards[1:]):
                        i.x = event.pos[0] + offset_x
                        i.y = event.pos[1] + offset_y + (j + 1) * CARD_OFFSET_Y

        if selected_card is not None:
            selected_card.rect.x = selected_card.x
            selected_card.rect.y = selected_card.y
            screen.blit(selected_card.image, selected_card.rect.topleft)
            for i in selected_cards[1:]:
                i.rect.x = i.x
                i.rect.y = i.y
                screen.blit(i.image, i.rect.topleft)

        pygame.display.flip()

        clock.tick(fps)

    pygame.quit()
