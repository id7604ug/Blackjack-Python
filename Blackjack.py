# This program is a recreation of a blackjack game created in python

# Imports
import itertools, random, math



# todo Make read from config file
playerNumber = 1

# This class handles the creation of player, the dealer and handles the turn options
class BlackjackGame:
    def __init__(self, playerNumber, startChips, playerNames):
        self.playerAmount = playerNumber # Sets the player
        self.chipCount = int(startChips) # Sets the start amout of chips
        self.deck = Deck() # Creates the deck object
        self.playerList = [] # Creates a list to store all player info
        self.playerNames = playerNames
        self.chipList = [] # Tracks the amount bet each round for each player
        self.playerChips = [] # Tracks the amount of chips each player has

    def test(self): # Method used duirng tests
        for i in range(20):
            print(self.deck.getCard(i).displayCard())
        print('Test run')

    # Method to initialize players with their hand and chips
    def initializePlayers(self, playerNumber, startChips): # todo Set up for more than one player
        self.dealer = Dealer() # Dealer object
        self.playerList.append(Player(self.chipCount, self.playerNames[0])) # Player object list
        self.playerChips.append(int(startChips))

    def dealCards(self):
        for x in range(0, 2): # Deal 2 cards
            self.dealer.dealCard(self.deck.drawCard())
            self.playerList[0].dealCard(self.deck.drawCard())

    def clearGame(self): # Method to clear game info
        self.chipList = []
        self.deck.clear()
        self.dealer.hand = []
        self.playerList[0].hand = []

    # Method to handle one round of blackjack
    def turn(self):
        # Validation #
        while True: # Checks the type of the input made by the player
            try:
                print(self.playerList[0].getName() + ' you have ' + str(self.playerChips[0])) # Displays amount of chips player can bet
                bet = input(self.playerList[0].getName() + ' how much would you like to bet? ')
                if (int(bet) > 0 and int(bet) <= self.playerChips[0]):
                    break
                else:
                    print('Choose a positive integer that is less than or equal to how much you have')
            except ValueError:
                print('Please choose an intiger number')

        self.chipList.append(int(bet))
        self.playerChips[0] -= int(self.chipList[0]) # Subtract bet

        if self.playerList[0].calcHandValue() != 21 and self.dealer.calcHandValue() == 21: # Check if dealer has blackjack
            print('Dealer has blackjack')
            print('Sorry ' + self.playerList[0].getName() + ' you lose')
        elif self.playerList[0].calcHandValue() == 21:
            print(self.playerList[0].getName() + ' you got blackjack!')
            # Handle divisions of chips
            # http://www.tutorialspoint.com/python/number_floor.htm
            self.chipList[0] += math.floor(self.chipList[0] * 2.5)
        else:
            self.dealer.showHand()
            while self.playerList[0].calcHandValue() < 21: # Continues until player busts
                self.playerList[0].showHand()
                if input('Would you like to hit or stay? H/S: ') in {'H', 'h', 'hit', 'Hit'}: # Hit or stay
                    self.playerList[0].dealCard(self.deck.drawCard())
                else:
                    break # Break because user chose not to continue
            while self.dealer.calcHandValue() < 17: # Handles dealer draws
                self.dealer.dealCard(self.deck.drawCard())
            self.dealer.dealerShowHand()
            if self.playerList[0].calcHandValue() > 21: # Bust
                print('You bust!')
            elif self.playerList[0].calcHandValue() > self.dealer.calcHandValue() or self.dealer.calcHandValue() > 21: # Win
                print('You win!')
                self.playerChips[0] += (self.chipList[0] * 2)
            elif self.playerList[0].calcHandValue() == self.dealer.calcHandValue(): # Push
                self.playerChips[0] += (self.chipList[0])


# This class handles each action the dealer can preform
class Dealer:
    def __init__(self):
        self.hand = [] # List to store cards for the players hand
        self.name = 'Dealer'

    def dealCard(self, card):
        self.hand.append(card) # Add card from deck

    def calcHandValue(self):
        value = 0
        for card in self.hand:
            value += card.getValue()
        return value

    def showHand(self):
        print('----')
        value = 0
        print(self.name + ' has: ')
        if self.name != 'Dealer': # Handles the properly shown cards if its the dealer
            for card in self.hand:
                card.displayCard()
            print('With a value of: ' + str(self.calcHandValue()))
        else:
            print('One face down')
            self.hand[1].displayCard()

    def dealerShowHand(self):
        print('----')
        value = 0
        print(self.name + ' has: ')
        for card in self.hand:
            card.displayCard()
        print('With a value of: ' + str(self.calcHandValue()))


    def getName(self):
        return self.name

# This class handles each action a player can do and the information stored for each player
class Player (Dealer):
    def __init__(self, playerChips, playerName):
        self.chips = playerChips
        self.name = playerName
        self.hand = [] # List to store cards for the players hand
    pass



# This class hold information for each card
class Card:
    # Converts the input numbers into cards with suit and face value
    def __init__(self, v, s):
        self.isAce = False
        if s == 1:
            self.suit = 'Spades'
        if s == 2:
            self.suit = 'Clubs'
        if s == 3:
            self.suit = 'Diamonds'
        if s == 4:
            self.suit = 'Hearts'
        if (v < 11) and (v > 1):
            self.value = v
            self.face = str(v)
        if v == 1:
            self.value = 11
            self.isAce = True
            self.face = 'Ace'
        if v > 10:
            self.value = 10
        if v == 11:
            self.face = 'Jack'
        if v == 12:
            self.face = 'Queen'
        if v == 13:
            self.face = 'King'

    # Prints the card
    def displayCard(self):
        print(self.face + ' of ' + self.suit)
    # Returns the value of the card
    def getValue(self):
        return self.value

# This class holds information and methods for the deck
class Deck:
    def __init__(self):
        self.deck = []

    # https://www.programiz.com/python-programming/examples/shuffle-card
    # I origionally used this source code to help create the deck of cards
    # I am now using something different because that didn't support how I wanted the cards to be made
    def createDeck(self):
        # Make deck
        for i in range(1, 14):
            for x in range(1, 5):
                self.deck.append(Card(i, x))

    # Shuffle deck
    def shuffleDeck(self):
        random.shuffle(self.deck)

    # Returns Card object in "place"
    def getCard(self, place):
        return self.deck[place]

    # Retrun the card on top of the deck
    def drawCard(self):
        return self.deck.pop()
    def clear(self):
        self.deck = []

# Function to get player names
def getNames(playerNumber):
    nameList = []
    for i in range(playerNumber):
        nameList.append(input('Enter your name: '))
    # print(nameList)
    return nameList

# Function to get the startChips from the chips.txt file
# http://www.tutorialspoint.com/python/python_files_io.htm
def getStartChips():
    chipsFile = open("chips.txt", "r")
    text = chipsFile.read()
    chipsFile.close()
    return text.split(':')[1]

# Function to set the new chips amount into the chips.txt file
def setChipsFile(name, newChipsAmount):
    chipsFile = open("chips.txt", "w")
    chipsFile.write(name + ':' + str(newChipsAmount))
    chipsFile.close()
    print("File written, Chip amount saved")

# Main function of program
def main():
    try:
        startChips = getStartChips() # Get start chips amount

        game = BlackjackGame(playerNumber, startChips, getNames(playerNumber))
        game.deck.createDeck() # Create deck
        game.deck.shuffleDeck() # Shuffle deck
        game.initializePlayers(playerNumber, startChips) # Initialize player information
        game.dealCards()
        while True:
            game.turn()
            if game.playerChips[0] == 0:
                print('You ran out of chips refilling to 100')
                game.playerChips[0] = 100
            print('Would you like to play another round?')
            print('Or cash out your current amount: ' + str(game.playerChips[0]))
            playAgain = input('Play/Cash Out: ')
            if playAgain not in {'play', 'Play', 'p', 'P'}:
                break
            game.clearGame()
            game.deck.createDeck()
            game.deck.shuffleDeck()
            game.dealCards()
        setChipsFile(game.playerList[0].getName(), game.playerChips[0])
    except FileNotFoundError:
        file = open("chips.txt", "w")
        file.close()
# Executes the main function
main()
