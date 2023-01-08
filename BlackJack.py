# Mini-project #6 - Blackjack
import sys
import pygame
from pygame import *
import random

pygame.init()

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
RED = (255,0,0)
GREEN = (0,255,0)
MOSSGREEN = (61, 145, 64)
BLUE = (0,0,255)
LIGHTGRAY = (150, 150, 150)
DARKGRAY = (100, 100, 100)
SHADOW = '#354B5E'

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = pygame.image.load("Assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = ((36 + 72), 48)
card_back = pygame.image.load("Assets/card_jfitz_back.png")
card_back_blue = card_back.subsurface(0, 0, CARD_BACK_SIZE[0], CARD_BACK_SIZE[1])
card_back_red = card_back.subsurface(CARD_BACK_SIZE[0], 0, CARD_BACK_SIZE[0], CARD_BACK_SIZE[1])

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
font = pygame.font.SysFont("Arial", 25)

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


""" define card class """
class Card:
    # Card constructor
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print("Invalid card: ", suit, rank)

    # Card str method
    def __str__(self):
        return self.suit + self.rank

    # Card get_suit method
    def get_suit(self):
        return self.suit

    # Card get_rank method
    def get_rank(self):
        return self.rank

    # Card draw method
    def draw(self, canvas, pos):
        x = CARD_SIZE[0] * RANKS.index(self.rank)
        y = CARD_SIZE[1] * SUITS.index(self.suit)
        card_image = card_images.subsurface(x, y, CARD_SIZE[0], CARD_SIZE[1])
        canvas.blit(card_image, pos)

""" define hand class """
class Hand:
    # Hand constructor
    def __init__(self, name):
        self.name = name
        self.cards = []

    # Hand str method
    # String all cards in card list
    def __str__(self):
        string = "Hand contains "
        for i in range(len(self.cards)):
            string += str(self.cards[i]) + " "
        return string

    # Hand add_card method
    # Add card object to card list
    def add_card(self, card):
        self.cards.append(card)

    # Hand get_value method
    # Get value of cards in card list
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.value = 0
        self.aces = 0
        
        # Sum the values of the cards in card list
        for i in range(len(self.cards)):
            self.value += VALUES[self.cards[i].get_rank()]
            # check for Aces
            if self.cards[i].get_rank() == "A":
                self.aces += 1
        
        # set conditions for the value of hand
        if self.aces <= 0:
            self.value = self.value
        elif self.aces > 0:
            if ((self.value + 10) <= 21):
                self.value += 10
            elif ((self.value + 10) > 21):
                self.value = self.value
        
        return self.value

    # Hand draw method
    def draw(self, canvas, start_pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for c in self.cards:
            card_pos = (start_pos[0] + (i * (CARD_SIZE[0] + 25)), start_pos[1])
            """Add border (optional)"""
            coordinates = [(card_pos[0] - 3, card_pos[1] - 3),
                (card_pos[0] + 3 + CARD_SIZE[0], card_pos[1] - 3),
                (card_pos[0] + 3 + CARD_SIZE[0], card_pos[1] + CARD_SIZE[1] + 3),
                (card_pos[0] - 3, card_pos[1] + CARD_SIZE[1] + 3)]
            
            """draw border/ filler"""
            # canvas.draw_polygon(coordinates, 1, "dimgray", "beige")
            
            # draw card
            c.draw(canvas, card_pos)

            # move to next card
            i += 1
            
        """if round is still in play, draw card back on hole card"""
        if in_play and self.name is "dealer":
            canvas.blit(card_back_red, start_pos)
 
        
""" Define deck class """
class Deck:
    # Deck constructor
    def __init__(self):
        # create a Deck object
        self.deck_list = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_list.append(Card(suit, rank))

    # Deck shuffle method
    def shuffle(self):
        # shuffle the deck 
        return random.shuffle(self.deck_list)

    # Deck deal_card method
    # deal card from topmost of deck
    def deal_card(self):
        # deal a card object from the deck
        return self.deck_list.pop(-1)

    # Deck str method
    def __str__(self):
        # return a string representing the deck
        string = ""
        for i in range(len(self.deck_list)):
            string += str(self.deck_list[i]) + " "
        return string


""" Define button class """
class Button:
    # button constructor
    def __init__(self, text, width, height, position, elevation, function, is_conditional):
        # function to run
        self.function = function
        self.is_conditional = is_conditional

        # top rectangle
        self.top_rect = pygame.Rect(position, (width, height))
        self.top_color = DARKGRAY

        # bottom rectangle
        self.bottom_rect = pygame.Rect(position, (width, height))
        self.bottom_color = SHADOW

        # rectangle elevation
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y = position[1]

        # text
        self.text_surf = font.render(text, True, WHITE)
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        # button pressed boolean
        self.is_pressed = False

    # draw method
    def draw(self):
        # elevation
        self.top_rect.y = self.original_y - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        # button with shadow
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        # draw button and text
        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.is_enabled()

    # check if button is clicked
    def click_checker(self):
        mouse_position = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]

        # check if mouse pointer collides with button
        if self.top_rect.collidepoint(mouse_position):
            # change color of button when hovering
            self.top_color = LIGHTGRAY

            # register left click
            if left_click:
                self.dynamic_elevation = 0
                self.is_pressed = True
            # run the code once if button click is released
            else:
                self.dynamic_elevation = self.elevation
                if self.is_pressed:
                    self.function()
                    self.is_pressed = False

        # return original color after hovering
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = DARKGRAY

    # check if enabled
    def is_enabled(self):
        if not self.is_conditional:
            self.click_checker()
        else:
            if in_play:
                self.click_checker()
            else:
                self.top_color = BLACK


""" define event handlers for buttons """
""" Deal method """
def deal():
    global outcome, in_play, bust, score, win, my_deck, my_hand, dealer_hand
    outcome = "Hit or Stand?"
    bust = ""
    win = ""
    
    if in_play:
        score -= 1
    
    # your code goes here
    my_deck = Deck()
    my_deck.shuffle()
    
    dealer_hand = Hand("dealer")
    my_hand = Hand("player")
    
    # deal 2 cards each for player and dealer
    for i in range(2):
        dealer_hand.add_card(my_deck.deal_card())
        my_hand.add_card(my_deck.deal_card())

    # play is in session
    in_play = True
    

""" Hit method """
def hit():
    # replace with your code below
    global in_play, outcome, bust, score, win
 
    # if the hand is in play, hit the player
    if in_play:
        my_hand.add_card(my_deck.deal_card())
        
        # Allow to hit only if not yet busted
        if my_hand.get_value() > 21:
            in_play = False
            bust = "Player"
            score -= 1
            win = "House Wins!!!"
   
    # if busted, assign a message to outcome, update in_play and score
    if in_play:
        outcome = "Hit or Stand?"
    elif not in_play:
        outcome = "New Deal?"


""" Stand method """
def stand():
    # replace with your code below
    global in_play, outcome, bust, score, win
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        # loop to set dealer's final hand
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(my_deck.deal_card())
            
        # compare hands to see who wins
        if dealer_hand.get_value() > 21:
            in_play = False
            bust = "Dealer"
            score += 1
            win = "Player Wins!!!"
        elif (17 <= dealer_hand.get_value() <= 21):
            if my_hand.get_value() > dealer_hand.get_value():
                in_play = False
                score += 1
                win = "Player Wins!!!"
            elif my_hand.get_value() < dealer_hand.get_value():
                in_play = False
                score -= 1
                win = "House Wins!!!"
            elif my_hand.get_value() == dealer_hand.get_value():
                in_play = False
                win = "DRAW!!!"

    # assign a message to outcome, update in_play and score
    # assign message as guide/directions in UI
    if in_play:
        outcome = "Hit or Stand?"
    elif not in_play:
        outcome = "New Deal?"


""" Text Handler"""
def textHandler(text, position, font, size, color):
    textFont = pygame.font.SysFont(font, size)
    textLabel = textFont.render(text, True, color)
    screen.blit(textLabel, position)


""" Quit handler"""
def quit():
    pygame.quit()
    sys.exit()

""" Draw handler """
def draw(canvas):
    # bg color
    canvas.fill(MOSSGREEN)

    # Draw buttons
    dealButton.draw()
    hitButton.draw()
    standButton.draw()
    quitButton.draw()

    # Draw both Player's and Dealer's Hand
    dealer_hand.draw(canvas, (50, 200))
    my_hand.draw(canvas, (50, 400))

    # Draw labels
    # Draw BlackJack text
    textHandler("BlackJack", (50, 20), "Times New Roman", 70, BLACK)

    # Draw Dealer text
    textHandler("Dealer", (50, 125), "Comic Sans MS", 35, RED)


    # Draw Player text
    textHandler("Player", (50, 325), "Comic Sans MS", 35, GREEN)
    
    # Draw Score
    border = pygame.draw.rect(screen, LIGHTGRAY, (417, 32, 156, 56), 6, 6)
    scoreBoard = pygame.draw.rect(screen, BLACK, (420, 35, 150, 50), 0, 6)
    scoreFont = pygame.font.SysFont("Times New Roman", 35)
    scoreLabel = scoreFont.render("Score: " + str(score), True, WHITE)
    canvas.blit(scoreLabel, scoreLabel.get_rect(center=scoreBoard.center))
        
    # Draw next step guide
    textHandler(outcome, (220, 520), "Times New Roman", 35, BLACK)
    
    # Draw bust label
    if bust == "Player":
        textHandler("Bust!!!", (200, 325), "Comic Sans MS", 35, BLACK)
    elif bust == "Dealer":
        textHandler("Bust!!!", (200, 125), "Comic Sans MS", 35, BLACK)
        
    # Draw winner
    if win == "Player Wins!!!":
        textHandler("Player Wins!!!", (200, 325), "Comic Sans MS", 35, "#7FFF00")
    elif win == "House Wins!!!":
        textHandler("House Wins!!!", (200, 125), "Comic Sans MS", 35, RED)
    elif win == "DRAW!!!":
        textHandler("DRAW!!!", (200, 125), "Comic Sans MS", 35, BLACK)


def gameloop():
    # get things rolling
    deal()

    while True:
        # Draw screen
        draw(screen)

        # listener loop
        for event in pygame.event.get():

            # quit listener
            if event.type == QUIT:
                quit()


        pygame.display.update()


if __name__ == "__main__":
    # initialization frame
    screen = pygame.display.set_mode((600, 650))
    pygame.display.set_caption("BlackJack")

    # create buttons
    dealButton = Button("Deal", 130, 40, (30, 600), 6, deal, False)
    hitButton = Button("Hit", 130, 40, (170, 600), 6, hit, True)
    standButton = Button("Stand", 130, 40, (310, 600), 6, stand, True)
    quitButton = Button("Quit", 130, 40, (450, 600), 6, quit, False)

    gameloop()


# remember to review the gradic rubric