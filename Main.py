from copy import deepcopy

import pygame
import random
import copy
import button
import time

def deck():
    cards = []

    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    one_deck = 4 * cards
    decks = 1
    game_deck = deepcopy(decks * one_deck)
    random.shuffle(game_deck)
    clover = ['Clover/']
    diamond = ['Diamond/']
    heart = ['Heart/']
    spade = ['Spade/']
    clovers = 13 * clover
    diamonds = 13 * diamond
    hearts = 13 * heart
    spades = 13 * spade
    suit = clovers + diamonds + hearts + spades
    suits = deepcopy(13 * suit)
    random.shuffle(suits)
    return game_deck, suits


def deal_card(gamedeck, suits,hand, hand_suits ):
    card = gamedeck[0]
    hand.append(card)
    gamedeck.pop(0)
    suit = suits[0]
    hand_suits.append(suit)
    suits.pop(0)

def first_deal(gamedeck, player_hand, dealer_hand, suits, player_suit, dealer_suit):
    for _ in range(2):
        deal_card(gamedeck, suits,player_hand, player_suit)
        deal_card(gamedeck, suits,dealer_hand, dealer_suit)

def calculate_total(hand):
        total = 0
        face_cards = {'J': 10, 'Q': 10, 'K': 10}  # set facecards to 10
        ace_count = 0

        for card in hand:
            if isinstance(card, int):  # if its a number card add card value to total
                total += card
            elif card in face_cards:  # if its a face card add 10 to total
                total += face_cards[card]
            elif card == 'A':  # add ace to hand not a value yet (ace can be 1 or 11)
                ace_count += 1

        # ace can be 1 or 11 based on total hand value
        for _ in range(ace_count):
            if total + 11 > 21:
                total += 1
            else:
                total += 11

        return total


def draw_player_hand(hand, suits,surface):
    font = pygame.font.Font("resource/Comic_Sans_MS.ttf", 50)
    cardWidth , cardHeight = 75, 120
    cardGap = 72
    cardposX = 330
    cardposY = 370

    for x in range(len(hand)):
        drawCard = pygame.image.load("resource/cards/" + str(suits[x]) + str(hand[x]) + ".png").convert_alpha()
        drawCard = pygame.transform.smoothscale(drawCard, (cardWidth, cardHeight)).convert_alpha()
        surface.blit(drawCard, (cardposX, cardposY))
        cardposX += cardGap
    total = calculate_total(hand)
    print(total)
    draw_total = font.render(str(total), False, (255,255,255))
    rec_total = draw_total.get_rect(center = (250,400))
    surface.blit(draw_total, rec_total)


def draw_dealer_hand(hand, suits, surface, player_turn):
    font = pygame.font.Font("resource/Comic_Sans_MS.ttf", 50)
    cardWidth , cardHeight = 75, 120
    cardGap = 72
    cardposX = 330
    cardposY = 200

    if player_turn:
        for x in [0, 1]:
            if x == 1:
                drawCard = pygame.image.load("resource/back.png").convert_alpha()
            else:
                drawCard = pygame.image.load("resource/cards/" + str(suits[0]) + str(hand[0]) + ".png").convert_alpha()
                total = hand[0]
            drawCard = pygame.transform.smoothscale(drawCard, (cardWidth, cardHeight))
            surface.blit(drawCard, (cardposX, cardposY))
            cardposX += cardGap
    else:
        for x in range(len(hand)):
            drawCard = pygame.image.load("resource/cards/" + str(suits[x]) + str(hand[x]) + ".png").convert_alpha()
            drawCard = pygame.transform.smoothscale(drawCard, (cardWidth, cardHeight)).convert_alpha()
            surface.blit(drawCard, (cardposX, cardposY))
            cardposX += cardGap
            total = calculate_total(hand)
    print(total)
    draw_total = font.render(str(total), False, (255, 255, 255))
    rec_total = draw_total.get_rect(center=(250, 240))
    surface.blit(draw_total, rec_total)

def main():
    player_hand = []
    dealer_hand = []
    player_suit = []
    dealer_suit = []
    gamedeck, suits = deck()
    print(gamedeck)
    print(suits)
    first_deal(gamedeck, player_hand, dealer_hand, suits, player_suit, dealer_suit)
    print(player_hand)
    print(player_suit)
    print(dealer_hand)
    print(dealer_suit)
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Black Jack")
    fps = 60
    timer = pygame.time.Clock()
    font = pygame.font.Font("resource/Comic_Sans_MS.ttf", 25)
    bg = pygame.image.load("resource/table.jpg").convert_alpha()
    bg = pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))
    stand_image = pygame.image.load("resource/stand.png").convert_alpha()
    hit_image = pygame.image.load("resource/hit.png").convert_alpha()
    again_image = pygame.image.load("resource/again.png").convert_alpha()
    standbutton = button.Button(100, 496, stand_image, .85)
    hitbutton = button.Button(450, 500, hit_image, .9)
    againbutton = button.Button(285, 500, again_image, 0.7)
    screen.blit(bg, (0, 0))

    player_turn = True
    run = True
    game_start = True
    dealer_turn = False
    game_restart = False
    while run:
        timer.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
        if game_start:
            draw_player_hand(player_hand, player_suit, screen)
            draw_dealer_hand(dealer_hand, dealer_suit, screen, player_turn)
            game_start = False

        if dealer_turn:
            draw_dealer_hand(dealer_hand, dealer_suit, screen, player_turn)
            dealer_total = calculate_total(dealer_hand)
            if dealer_total < 17:
                deal_card(gamedeck, suits, dealer_hand, dealer_suit)
                draw_dealer_hand(dealer_hand, dealer_suit, screen, player_turn)
            elif dealer_total >= 17:
                dealer_turn = False
            screen.blit(bg, (0, 0))
            draw_dealer_hand(dealer_hand, dealer_suit, screen, player_turn)
            draw_player_hand(player_hand, player_suit, screen)

        if not player_turn and not dealer_turn and not game_restart:
            player_total = calculate_total(player_hand)
            dealer_total = calculate_total(dealer_hand)
            if player_total > 21 and dealer_total > 21:
                print("dealer and player bust")
                draw_total = font.render("Player Bust", False, (255, 255, 255))
                rec_total = draw_total.get_rect(center=(100, 400))
                screen.blit(draw_total, rec_total)
                draw_total = font.render("Dealer Bust", False, (255, 255, 255))
                rec_total = draw_total.get_rect(center=(140, 240))
                screen.blit(draw_total, rec_total)
            elif player_total == dealer_total:
                print("tie")
            elif player_total > 21:
                print("player bust")
                draw_total = font.render("Player Bust", False, (255, 255, 255))
                rec_total = draw_total.get_rect(center=(100, 400))
                screen.blit(draw_total, rec_total)
            elif dealer_total > 21:
                print("dealer bust")
                draw_total = font.render("Dealer Bust", False, (255, 255, 255))
                rec_total = draw_total.get_rect(center=(140, 240))
                screen.blit(draw_total, rec_total)
            elif player_total > dealer_total:
                print("player wins")
                draw_total = font.render("Player Wins", False, (255, 255, 255))
                rec_total = draw_total.get_rect(center=(100, 400))
                screen.blit(draw_total, rec_total)
            else:
                print("dealer wins")
                draw_total = font.render("Dealer Wins", False, (255, 255, 255))
                rec_total = draw_total.get_rect(center=(140, 240))
                screen.blit(draw_total, rec_total)
            game_restart = True

        if game_restart:
            if againbutton.draw(screen):
                game_start = True
                player_turn = True
                dealer_turn = False
                game_restart = False
                screen.blit(bg, (0, 0))
                player_hand = []
                dealer_hand = []
                player_suit = []
                dealer_suit = []
                first_deal(gamedeck, player_hand, dealer_hand, suits, player_suit, dealer_suit)
        if standbutton.draw(screen) and player_turn:
            player_turn = False
            dealer_turn = True
            print('stand')
        if hitbutton.draw(screen) and player_turn:
            screen.blit(bg, (0, 0))
            draw_dealer_hand(dealer_hand, dealer_suit, screen, player_turn)
            deal_card(gamedeck, suits,player_hand, player_suit)
            draw_player_hand(player_hand, player_suit, screen)
            print(player_hand)
            print(player_suit)
            print('hit')

        if player_turn:
            if calculate_total(player_hand) > 21:
                player_turn = False
                dealer_turn = True
            elif calculate_total(player_hand) == 21:
                player_turn = False
                dealer_turn = True

        pygame.display.update()
       # pygame.display.flip()


if __name__ == "__main__":
    main()