import os
import csv
import random
import datetime
import pandas as pd
import webbrowser
import math

def instruction():
    # Instructions discussing object of the game
    instructions = 'This game is called Blackjack Deviations and it will be used in conjunction with notepad \n' \
                "file 'deviations_summary.csv'.  First, the program will present you with values for number \n" \
                "of card decks, decks played, and a Running Count.  Your job is to input the True Count \n" \
                "(TC = RC / Decks Remaining) and the program will inform you if your response is correct \n" \
                "or not. Next, the program will present you with a player hand and a dealer hand.  Your job\n" \
                "is to input the correct play based on Blackjack Basic Strategy and True Count Deviations:" \
                "\n\t[H]it\n\t[S]tand\n\t[DH] double otherwise (o/w) hit\n\t[DS] double o/w stand\n\ts[P]lit" \
                "\n\t[RH] surrender o/w hit\n\t[RS] surrender o/w stand\n\t[I]nsurance.\nPossible correct" \
                " responses are the letters shown in the brackets above.\n" \
                "For example: if the correct decision is [H]it, input 'H'. User inputs are not case sensitive.\n" \
                "The object of the game is to answer as accurately and as quickly as possible.   " \
                "\n\n**Enter 'q' at any time to end the program.**\n"
    print('\n*****     *****     *****     *****\n')
    print(instructions)

    # For those unfamiliar with deviations from perfect blackjack basic strategy, view this video
    deviations_video = 'https://www.blackjackapprenticeship.com/blackjack-deviations/'
    watch_video = input('If you would like to watch a quick video to further explain deviations, type "Y".\n'
                        'Otherwise, press "enter" to continue or press [q]uit.\n\n')
    if watch_video == 'Y':
        webbrowser.open(deviations_video)
    # Quit program
    if watch_video == 'q':
        print('\nHope to see see you again soon...\n\n')
        exit()
def time_current():
    # Records the current time
    time = datetime.datetime.now()
    return time
def elapsed_game_time(game_time_start, game_time_end):
    # Output the total time the user has played the game for
    delta_time = game_time_end - game_time_start
    total_time = round((delta_time.total_seconds()), 2)
    return total_time

def deviation_hands():
    # A list of the hands that may trigger deviation from blackjack basic strategy
    # PH: Player Hand; DH: Dealer Hand; BS: Basic Strategy; TC: True Count; RC: Running Count; o/w: otherwise
        # `+` after the TC indicates the deviation happens at that true count and above
        # `-` after the TC indicates the devation happens at the true count and below
        # 0- TC indicates the deviation happens at any negative running count
        # 0+ TC indicates the deviation occurs at any positive running count

    dev_hands = [
        # PH: 8  DH: 6  BS: [H]it  Deviation: [DH] double if TC 2+ o/w hit
        [2, 6, 6], [3, 5, 6],
        [6, 2, 6], [5, 3, 6],
        # PH: 9  DH: 2  BS: [H]it  Deviation: [DH] double if TC 1+ o/w hit
        [2, 7, 2], [3, 6, 2], [4, 5, 2],
        [7, 2, 2], [6, 3, 2], [5, 4, 2],
        # PH: 9  DH: 7  BS: [H]it  Deviation: [DH] double if TC 3+ o/w hit
        [2, 7, 7], [3, 6, 7], [4, 5, 7],
        [7, 2, 7], [6, 3, 7], [5, 4, 7],
        # PH: 10  DH: 10  BS: [H]it  Deviation: [DH] double if TC 4+ o/w hit
        [2, 8, 10], [3, 7, 10], [4, 6, 10], [5, 5, 10],
        [8, 2, 10], [7, 3, 10], [6, 4, 10], [5, 5, 10],
        # PH: 10  DH: A  BS: [H]it  Deviation: [DH] double if TC 3+ o/w hit
        [2, 8, 'A'], [3, 7, 'A'], [4, 6, 'A'], [5, 5, 'A'],
        [8, 2, 'A'], [7, 3, 'A'], [6, 4, 'A'], [5, 5, 'A'],
        # PH: 12  DH: 2  BS: [H]it  Deviation: [S]tand if TC 3+
        [2, 10, 2], [2, 10, 2], [2, 10, 2], [2, 10, 2], [3, 9, 2], [4, 8, 2], [5, 7, 2],
        [10, 2, 2], [10, 2, 2], [10, 2, 2], [10, 2, 2], [9, 3, 2], [8, 4, 2], [7, 5, 2],
        # PH: 12  DH: 3  BS: [H]it  Deviation: [S]tand if TC 2+
        [2, 10, 3], [2, 10, 3], [2, 10, 3], [2, 10, 3], [3, 9, 3], [4, 8, 3], [5, 7, 3],
        [10, 2, 3], [10, 2, 3], [10, 2, 3], [10, 2, 3], [9, 3, 3], [8, 4, 3], [7, 5, 3],
        # PH: 12  DH: 4  BS: [S]tand  Deviation: [H]it if TC 0-
        [2, 10, 4], [2, 10, 4], [2, 10, 4], [2, 10, 4], [3, 9, 4], [4, 8, 4], [5, 7, 4],
        [10, 2, 4], [10, 2, 4], [10, 2, 4], [10, 2, 4], [9, 3, 4], [8, 4, 4], [7, 5, 4],
        # PH: 12  DH: 5  BS: [S]tand  Deviation: [H]it if TC -2-
        [2, 10, 5], [2, 10, 5], [2, 10, 5], [2, 10, 5], [3, 9, 5], [4, 8, 5], [5, 7, 5],
        [10, 2, 5], [10, 2, 5], [10, 2, 5], [10, 2, 5], [9, 3, 5], [8, 4, 5], [7, 5, 5],
        # PH: 12  DH: 6  BS: [S]tand  Deviation: [H]it if TC -1-
        [2, 10, 6], [2, 10, 6], [2, 10, 6], [2, 10, 6], [3, 9, 6], [4, 8, 6], [5, 7, 6],
        [10, 2, 6], [10, 2, 6], [10, 2, 6], [10, 2, 6], [9, 3, 6], [8, 4, 6], [7, 5, 6],
        # PH: 13  DH: 2  BS: [S]tand  Deviation: [H]it if TC -1-
        [3, 10, 2], [3, 10, 2], [3, 10, 2], [3, 10, 2], [4, 9, 2], [5, 8, 2], [6, 7, 2],
        [10, 3, 2], [10, 3, 2], [10, 3, 2], [10, 3, 2], [9, 4, 2], [8, 5, 2], [7, 6, 2],
        # PH: 13  DH: 3  BS: [S]tand  Deviation: [H]it if TC -2-
        [3, 10, 3], [3, 10, 3], [3, 10, 3], [3, 10, 3], [4, 9, 3], [5, 8, 3], [6, 7, 3],
        [10, 3, 3], [10, 3, 3], [10, 3, 3], [10, 3, 3], [9, 4, 3], [8, 5, 3], [7, 6, 3],
        # PH: 14  DH: 10  BS: [H]it  Deviation: [RH] surrender if TC 3+ o/w hit
        [4, 10, 10], [4, 10, 10], [4, 10, 10], [4, 10, 10], [5, 9, 10], [6, 8, 10], [7, 7, 10],
        [10, 4, 10], [10, 4, 10], [10, 4, 10], [10, 4, 10], [9, 5, 10], [8, 6, 10], [7, 7, 10],
        # PH: 15  DH: 9  BS: [H]it  Deviation: [RH] surrender if TC 2+ o/w hit
        [5, 10, 9], [5, 10, 9], [5, 10, 9], [5, 10, 9], [6, 9, 9], [7, 8, 9],
        [10, 5, 9], [10, 5, 9], [10, 5, 9], [10, 5, 9], [9, 6, 9], [8, 7, 9],
        # PH: 15  DH: 10  BS: [RH] surrender if 0<=TC<4 o/w hit  Deviation: [H]it if TC 0-; [RS] surrender if TC 4+ o/w stand
        [5, 10, 10], [5, 10, 10], [5, 10, 10], [5, 10, 10], [6, 9, 10], [7, 8, 10],
        [10, 5, 10], [10, 5, 10], [10, 5, 10], [10, 5, 10], [9, 6, 10], [8, 7, 10],
        # PH: 15  DH: A  BS: [RH] surrender if -1<=TC<5 o/w hit Deviation: [H]it if TC -1-; [RS] surrender if TC 5+ o/w stand
        [5, 10, 'A'], [5, 10, 'A'], [5, 10, 'A'], [5, 10, 'A'], [6, 9, 'A'], [7, 8, 'A'],
        [10, 5, 'A'], [10, 5, 'A'], [10, 5, 'A'], [10, 5, 'A'], [9, 6, 'A'], [8, 7, 'A'],
        # PH: 16  DH: 8  BS: [H]it  Deviation: [RH] surrender if TC 4+ o/w hit
        [6, 10, 8], [6, 10, 8], [6, 10, 8], [6, 10, 8], [7, 9, 8],
        [10, 6, 8], [10, 6, 8], [10, 6, 8], [10, 6, 8], [9, 7, 8],
        # PH: 16  DH: 9  BS: [RH] surrender if -1<TC<4 o/w hit Deviation: [H]it if TC -1-; [RS] surrender if TC 4+ o/w stand
        [6, 10, 9], [6, 10, 9], [6, 10, 9], [6, 10, 9], [7, 9, 9],
        [10, 6, 9], [10, 6, 9], [10, 6, 9], [10, 6, 9], [9, 7, 9],
        # PH: 16  DH: 10  BS: [RH] surrender TC<=0 o/w hit  Deviation: [RS] surrender if TC 0+ o/w stand
        [6, 10, 10], [6, 10, 10], [6, 10, 10], [6, 10, 10], [7, 9, 10],
        [10, 6, 10], [10, 6, 10], [10, 6, 10], [10, 6, 10], [9, 7, 10],
        # PH: 16  DH: A  BS: [RH] surrender TC<3 o/w hit  Deviation: [RS] surrender if TC 3+ o/w stand
        [6, 10, 'A'], [6, 10, 'A'], [6, 10, 'A'], [6, 10, 'A'], [7, 9, 'A'],
        [10, 6, 'A'], [10, 6, 'A'], [10, 6, 'A'], [10, 6, 'A'], [9, 7, 'A'],
        # PH: A,6 (soft 17)  DH: 2  BS: [H]it  Deviation: [DH] double if TC 1+ o/w hit
        [6, 'A', 2],
        ['A', 6, 2],
        # PH: A,8 (soft 19)  DH: 4  BS: [S]tand  Deviation: [DS] double if TC 3+ o/w stand
        [8, 'A', 4],
        ['A', 8, 4],
        # PH: A,8 (soft 19)  DH: 5  BS: [S]tand  Deviation: [DS] double if TC 1+ o/w stand
        [8, 'A', 5],
        ['A', 8, 5],
        # PH: A,8 (soft 19)  DH: 6  BS: [DS] double o/w stand  Deviation: [S]tand if TC 0-
        [8, 'A', 6],
        ['A', 8, 6],
        # PH: T,T  DH: 4  BS: [S]tand  Deviation: s[P]lit if TC 6+
        [10, 10, 4], [10, 10, 4], [10, 10, 4], [10, 10, 4],
        # PH: T,T  DH: 5  BS: [S]tand  Deviation: s[P]lit if TC 5+
        [10, 10, 5], [10, 10, 5], [10, 10, 5], [10, 10, 5],
        # PH: T,T  DH: 6  BS: [S]tand  Deviation: s[P]lit if TC 4+
        [10, 10, 6], [10, 10, 6], [10, 10, 6], [10, 10, 6],
        # PH: X,X  DH: A  BS: basic strategy  Deviation: [I]nsurance if TC 3+
        # Insurance at a TC 3+ causes issues with PH totals 8-10, 12-16, S17, S19 and 20 vs DH: A.  This is because
        # Insurance would take precedent on the first 2 cards, but after a 3rd card is dealt, the decisions written in
        # the comments above dictate the proper playing decisions. Therefore, not all possible insurance situations are
        # listed in the following scenarios; only PH totals of 4-7 and 18 are provided.
        [2, 2, 'A'], [2, 3, 'A'], [2, 4, 'A'], [2, 5, 'A'], [3, 3, 'A'], [3, 4, 'A'], [9, 9, 'A'], [10, 8, 'A'],
        [2, 2, 'A'], [3, 2, 'A'], [4, 2, 'A'], [5, 2, 'A'], [3, 3, 'A'], [4, 3, 'A'], [9, 9, 'A'], [8, 10, 'A'],
    ]
    return dev_hands
class Deal():
    # Pop a random list from method 'def deviation_hands():'
    # Assign the first two items to the player_hand and add up the player_total
    # Assign the last item to the dealer_hand and add up the dealer_total

    def __init__(self, dev_hands):
        # Define variables
        self.dev_hands = dev_hands
        self.cards_dealt = None
        self.player_hand = None
        self.player_total = 0
        self.dealer_hand = None
        self.dealer_total = 0

    def deal(self):
        # Pop one list (each list contains 3 items) from the 'dev_hands' list (method: def deviation_hands():)
        # The first two items in the popped list represent the player cards; the third item represents the dealer card
        if len(self.dev_hands) >= 1:
            random.shuffle(self.dev_hands)
            self.cards_dealt = self.dev_hands.pop()

    def deal_to_player(self):
        # Assign the first two items from the popped 'dev_hands' list to the player_hand
        self.player_hand = self.cards_dealt[0:2]

        # Add first and second card to player total
        for z in range(0, 2):
            # Aces: since this program only handles 2 player cards at a time, an Ace is valued at 11 and never valued
            # at 1
            if self.player_hand[z] == 'A':
                self.player_total += 11
            # Tens: add 10 to the player total and then re-assign 10 card to a 10 or face card
            elif self.player_hand[z] == 10:
                self.player_total += self.player_hand[z]
                tens_assignment = [10, 'J', 'Q', 'K']
                self.player_hand[z] = tens_assignment[random.randint(0, 3)]
            # If item is not a 10 or A, then add the integer to the player total
            else:
                self.player_total += self.player_hand[z]

    def deal_to_dealer(self):
        # Assign the third item from the popped 'dev_hands' list to the dealer_hand
        self.dealer_hand = self.cards_dealt[2]

        # Add card to the dealer total
        # Aces: an Ace is valued at 11; never 1
        if self.dealer_hand == 'A':
            self.dealer_total += 11
        # Tens: add 10 to the dealer total and then re-assign 10 card to a 10 or face card
        elif self.dealer_hand == 10:
            self.dealer_total += self.dealer_hand
            tens_assignment = [10, 'J', 'Q', 'K']
            self.dealer_hand = tens_assignment[random.randint(0, 3)]
        # If item is not a 10 or A, then add the integer to the player total
        else:
            self.dealer_total += self.dealer_hand

    def deal_instance(self):
        Deal.deal(self)
        Deal.deal_to_player(self)
        Deal.deal_to_dealer(self)

        return self.player_hand, self.player_total, self.dealer_hand, self.dealer_total

class Running_count():
    # PH: Player Hand; DH: Dealer Hand; BS: Basic Strategy; TC: True Count; RC: Running Count; o/w: otherwise
    # Rounding: 'floor' method for positive +TC and 'ceiling' method for negative -TC
    # A TC at -1<TC<1 will not be rounded
    # A random running count, decks played, and total decks are provided and the user will mentally calculate the TC

    def __init__(self, true_count_streak_list):
        self.game_decks_total = None
        self.game_running_count = None
        self.game_decks_played = None
        self.game_true_count_user = None
        self.game_true_count = None
        self.game_true_count_score = None
        self.game_true_count_streak_tally = [0]
        self.true_count_streak_list = true_count_streak_list

    def decks_total(self):
        # Determine the type of Blackjack game (i.e. 2 deck, 8 decks, etc)
        possible_no_decks = [2, 4, 6, 8]
        self.game_decks_total = possible_no_decks[random.randint(0, 3)]

    def running_count_range(self):
        # A random RC is calculated
        tc_per_deck = 10
        self.game_running_count = random.randint(-(self.game_decks_total * tc_per_deck), self.game_decks_total * tc_per_deck)

    def decks_played(self):
        # Make a list for possible DP (decks played) values
        # For a two deck game, the list looks like [1.5, 1.0, 0.5, 0.0]
        possible_decks_played = []
        x = .5
        for increment in range(0, 2 * self.game_decks_total):
            possible_decks_played.append(self.game_decks_total - x)
            # Increase DP at 1/2 deck increments
            x += .5
        self.game_decks_played = possible_decks_played[random.randint(0, 2 * self.game_decks_total - 1)]

    def prompt_for_true_count(self):
        # Message to be displayed showing the Number of Decks, Decks Player, and Running Count
        deck_str = '\nDecks: ' + str(self.game_decks_total)
        decks_played_str = 'DP: ' + str(self.game_decks_played)
        running_count_str = 'RC: ' + str(self.game_running_count)

        print(deck_str.ljust(13), end='')
        print(decks_played_str.ljust(10), end='')
        print(running_count_str.ljust(10), end='')

        # User to input the True Count as an integer
        # For TC>=1 round to nearest integer using the floor method (math.floor())
        # For TC<=-1 round to nearest integer using the ceiling method (math.ceil())
        # For -1<TC<1: 0 is the correct answer
        self.game_true_count_user = input('What is the running count? ')

    def bad_user_input(self):
        # Handle non-integer inputs or the [q]uit input
        while True:
            try:
                if self.game_true_count_user == 'q':
                    print('\nYou will need to enter "q" one more time to quit.\n')
                    break
                int(self.game_true_count_user)
                break
            except ValueError:
                print((' ' * 32) + 'You did not enter a number.')
                print(' ' * 32, end='')
                self.game_true_count_user = input('What is the true count? ')
                continue
    def calculate_true_count(self):
        # The program calculates the True Count
        self.game_true_count = self.game_running_count / (self.game_decks_total - self.game_decks_played)

        # The calculated TC is rounded (as needed)
        # Ceiling method for negative TC
        if self.game_true_count <= -1:
            self.game_true_count = math.ceil(self.game_true_count)

        # No rounding if -1<TC<1
        # This reasoning may be confusing.  For specific scenarios:
            # PH: 12  DH: 4   BS: [S]tand  Deviation: [H]it if TC 0-
                # The above deviation reads as: Hit on any negative count
            # PH: 15  DH: 10  BS: [RH] surrender if 0<=TC<4 o/w hit  Deviation: [H]it if TC 0-
                # The above deviation reads as: Hit on any negative count
            # PH: 16  DH: 10, BS: [RH] surrender if TC<=0 o/w hit; Deviation: [RS] surrender if TC 0+ o/w stand
                # The above deviation reads as: Surrender/stand on any positive count
        # These scenarios are unique. A True Count of 0.25 and -0.25 would round to TC = 0, but should not be handled
        # the same. Therefore, if the absolute value of the difference between the user's input and the true count
        # is <1 (not <=1), then the user's input will be considered correct.
        elif self.game_true_count > -1 and self.game_true_count < 1:
            self.game_true_count = round((self.game_running_count / (self.game_decks_total - self.game_decks_played)), 2)

        # Floor method for positive TC
        elif self.game_true_count >= 1:
            self.game_true_count = math.floor(self.game_true_count)
        else:
            self.game_true_count = 0

    def true_count_message_correct_incorrect(self):
        # Print a message telling the user if they were correct or not
        # Add a tally to the TC streak and total correct true counts

        # [q]uit command
        if self.game_true_count_user == 'q':
            self.game_true_count_score = False

        # User input was correct
        elif abs(self.game_true_count - int(self.game_true_count_user)) < 1:
            print((' ' * 32) + 'Correct.')
            self.game_true_count_score = 1

        # User input was incorrect
        else:
            print((' ' * 32) + 'Incorrect')
            self.game_true_count_score = 0

    def true_count_streak_tally(self):
        # Update the user's TC streak of correct answers
        # User input was correct; streak: +1
        if self.game_true_count_score == 1:
            self.true_count_streak_list[-1] += 1
        # User input was incorrect; streak back to 0; record the streak into the streak list
        elif self.game_true_count_score == 0 or self.game_true_count_score == False:
            self.true_count_streak_list.append(0)
        # The TC decision tree logic did not execute as expected
        else:
            print('check method "streak_tally"')

    def running_count_instance(self):
        # Run an instance for the running count
        Running_count.decks_total(self)
        Running_count.running_count_range(self)
        Running_count.decks_played(self)
        Running_count.prompt_for_true_count(self)
        Running_count.bad_user_input(self)
        Running_count.calculate_true_count(self)
        Running_count.true_count_message_correct_incorrect(self)
        Running_count.true_count_streak_tally(self)

        # Return variables to be used for evaluating performance of the user
        return self.game_true_count, self.true_count_streak_list, self.game_true_count_score,

def deviation_game(player_hand, dealer_hand, count):
    # A single round of the game is presented to the user and they are asked to provide the correct decision
    # PH: Player Hand; DH: Dealer Hand; BS: Basic Strategy; TC: True Count; RC: Running Count; o/w: otherwise

    # String formatting and printing of the cards for a single round of the game
    str_player_hand = 'PH: ' + str(player_hand[0]) + ' ' + str(player_hand[1])
    str_dealer_hand = 'DH: ' + str(dealer_hand)
    str_tc = 'TC: ' + str(count)
    print(str_player_hand.ljust(12), end='')
    print(str_dealer_hand.ljust(10), end='')
    print(str_tc.ljust(10), end='')

    # Given PH, DH and TC (or user calculated RC), ask the player what the correct decision is.
    # Possible correct inputs are the letter(s) within the brackets:
        # [H]it
        # [S]tand
        # [DH] double o/w hit
        # [DS] double o/w stand
        # s[P]lit
        # [RH] surrender o/w hit
        # [RS] surrender o/w stand
        # [I]nsurance
    decision = input('What is the correct decision? ')
    return decision
class Deviations_decision_tree():
    """Decision tree to determine if user input was correct based on the PH, DH, and TC"""
    # PH: Player Hand; DH: Dealer Hand; BS: Basic Strategy; TC: True Count; RC: Running Count; o/w: otherwise
        # `+` after the TC indicates the deviation happens at that true count and above
        # `-` after the TC indicates the devation happens at the true count and below
        # 0- TC indicates the deviation happens at any negative running count
        # 0+ TC indicates the deviation occurs at any positive running count
    def __init__(self, player_total, dealer_total, count, decision, deviation_streak):
        self.result = None
        # player[0] = list of two player cards (2-10,J,K or A); player[1] = player total as an integer
        self.player = player_total
        # dealer[0] = dealer card (2-10,J,K or A); dealer[1] = dealer total as an integer
        self.dealer = dealer_total
        # count = integer used to decide deviations from basic strategy
        self.count = count
        # decision = user input (H, S, DH, DS, P, RH, RS, or I)
        self.decision = decision
        # streak = number correct in a row
        self.deviation_streak = deviation_streak
        # Strings to be used to communicate to the user if they answered correcly or not
        self.h = '[H]it '
        self.s = '[S]tand '
        self.dh = '[DH] double o/w hit '
        self.ds = '[DS] double o/w stand '
        self.p = 's[P]lit '
        self.rh = '[RH] surr. o/w hit '
        self.rs = '[RS] surr. o/w stand '
        self.i = '[I]nsurance '
        # Spelling variations for accepted decisions (e.g. accepted user inputs are not case sensitive)
        self.action_h = ['H', 'h']
        self.action_s = ['S', 's']
        self.action_dh = ['DH', 'Dh', 'dH', 'dh']
        self.action_ds = ['DS', 'Ds', 'dS', 'ds']
        self.action_p = ['P', 'p']
        self.action_rh = ['RH', 'Rh', 'rH', 'rh']
        self.action_rs = ['RS', 'Rs', 'rS', 'rs']
        self.action_i = ['I', 'i']
        # Self testing: this will print when deviation decision logic executed as expected
        self.check_program = 'WARNING: Check logic in: class Deviation_decision_tree, method def '
    def eight(self):
        # PH: 8  DH: 6
        # PH: 8  DH: 6  BS: [H]it
        if self.dealer == 6 and self.count < 2:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '8 vs. 6 @ TC < 2'
        # PH: 8  DH: 6  BS: [H]it  Deviation: [DH] double if TC 2+ o/w hit
        elif self.dealer == 6 and self.count >= 2:
            if self.decision in self.action_dh:
                return 1
            if self.decision not in self.action_dh:
                return 0, self.dh, '8 vs. 6 @ TC 2+'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'eight')
    def nine(self):
        # PH: 9  DH: 2 or 7
        # PH: 9  DH: 2 or 7  BS: [H]it
        if self.dealer == 2 and self.count < 1 or self.dealer == 7 and self.count < 3:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '9 vs. {2 @ TC < 1 // 7 @ TC < 3}'
        # PH: 9  DH: 2 or 7  BS: [H]it  Deviation: [DH] double if TC 1+ or 3+ o/w hit
        elif self.dealer == 2 and self.count >= 1 or self.dealer == 7 and self.count >= 3:
            if self.decision in self.action_dh:
                return 1
            if self.decision not in self.action_dh:
                return 0, self.dh, '9 vs. {2 @ TC 1+ // 7 @ TC 3+}'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'nine')
    def ten(self):
        # PH: 10  DH: 10 or A
        # PH: 10  DH: 10 or A  BS: [H]it
        if self.dealer == 10 and self.count < 4 or self.dealer == 11 and self.count < 3:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '10 vs. {10 @ TC < 4 // A @ TC < 3}'
        # PH: 10  DH: 10 or A  BS: [H]it  Deviation: [DH] double if TC 4+ or 3+ o/w hit
        elif self.dealer == 10 and self.count >= 4 or self.dealer == 11 and self.count >= 3:
            if self.decision in self.action_dh:
                return 1
            if self.decision not in self.action_dh:
                return 0, self.dh, '10 vs. {10 @ TC 4+ // A @ TC 3+}'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'ten')
    def twelve(self):
        # PH: 12  DH: 2 or 3
        # PH: 12  DH: 2 or 3  BS: [H]it
        if self.dealer == 2 and self.count < 3 or self.dealer == 3 and self.count < 2:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h,  '12 vs. {2 @ TC < 3 // 3 @ TC < 2}'
        # PH: 12  DH: 2 or 3  BS: [H]it  Deviation: [S]tand if TC 3+ or 2+
        elif self.dealer == 2 and self.count >= 3 or self.dealer == 3 and self.count >= 2:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s,  '12 vs. {2 @ TC 3+ // 3 @ TC 2+}'

        # PH: 12  DH: 4, 5 or 6
        # PH: 12  DH: 4, 5 or 6  BS: [S]tand
        elif self.dealer == 4 and self.count >= 0 or self.dealer == 5 and self.count > -2 or self.dealer == 6 and self.count > -1:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, '12 vs. {4 @ TC >=0 // 5 @ TC >-2 // 6 @ TC >-1}'
        # PH: 12  DH: 4, 5 or 6  BS: [S]tand  Deviation: [H]it if TC 0-, -2-, or -1-
        elif self.dealer == 4 and self.count < 0 or self.dealer == 5 and self.count <= -2 or self.dealer == 6 and self.count <= -1:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '12 vs. {4 @ TC 0- // 5 @ TC -2- // 6 @ TC -1-}'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'twelve')
    def thirteen(self):
        # PH: 13  DH: 2 or 3
        # PH: 13  DH: 2 or 3  BS: [S]tand
        if self.dealer == 2 and self.count > -1 or self.dealer == 3 and self.count > -2:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, '13 vs. {2 @ TC > -1 // 3 @ TC > -2}'
        # PH: 13  DH: 2 or 3  BS: [S]tand  Deviation: [H]it if TC -1- or -2-
        elif self.dealer == 2 and self.count <= -1 or self.dealer == 3 and self.count <= -2:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '13 vs. {2 @ TC -1- // 3 @ TC -2-}'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'thirteen')
    def fourteen(self):
        # PH: 14  DH: 10
        # PH: 14  DH: 10  BS: [H]it
        if self.dealer == 10 and self.count < 3:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '14 vs. 10 @ TC < 3'
        # PH: 14  DH: 10  BS: [H]it  Deviation: [RH] surrender if TC 3+ o/w hit
        elif self.dealer == 10 and self.count >= 3:
            if self.decision in self.action_rh:
                return 1
            if self.decision not in self.action_rh:
                return 0, self.rh, '14 vs. 10 @ TC 3+'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'fourteen')
    def fifteen(self):
        # PH: 15  DH: 9
        # PH: 15  DH: 9  BS: [H]it
        if self.dealer == 9 and self.count < 2:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '15 vs. 9 @ TC < 2'
        # PH: 15  DH: 9  BS: [H]it  Deviation: [RH] surrender if TC 2+ o/w hit
        elif self.dealer == 9 and self.count >= 2:
            if self.decision in self.action_rh:
                return 1
            if self.decision not in self.action_rh:
                return 0, self.rh, '15 vs. 9 @ TC 2+'

        # PH: 15  DH: 10 or A
        # PH: 15  DH: 10 or A  BS: [RH] surrender if 0<=TC<4 or -1<=TC<5 o/w hit
        elif self.dealer == 10 and 0 <= self.count < 4 or self.dealer == 11 and -1 <= self.count < 5:
            if self.decision in self.action_rh:
                return 1
            if self.decision not in self.action_rh:
                return 0, self.rh, '15 vs. {10 @ 0 <= TC < 4 // A @ -1 <= TC < 5}'
        # PH: 15  DH: 10 or A  BS: [RH] surrender if 0<=TC<4 or -1<=TC<5 o/w hit  Deviation: [H]it if TC 0- or -1-
        elif self.dealer == 10 and self.count < 0 or self.dealer == 11 and self.count < -1:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '15 vs. {10 @ TC 0- // A @ TC -1-}'
        # PH: 15  DH: 10 or A  BS: [RH] surrender if 0<=TC<4 or -1<=TC<5 o/w hit  Deviation: [RS] surrender if TC 4+ or 5+ o/w stand
        elif self.dealer == 10 and self.count >= 4 or self.dealer == 11 and self.count >= 5:
            if self.decision in self.action_rs:
                return 1
            if self.decision not in self.action_rs:
                return 0, self.rs, '15 vs. {10 @ TC 4+ // A @ TC 5+}'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'fifteen')
    def sixteen(self):
        # PH: 16  DH: 8
        # PH: 16  DH: 8  BS: [H]it
        if self.dealer == 8 and self.count < 4:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '16 vs. 8 @ TC < 4'
        # PH: 16  DH: 8  BS: [H]it  Deviation: [RH] surrender if TC 4+ o/w hit
        elif self.dealer == 8 and self.count >= 4:
            if self.decision in self.action_rh:
                return 1
            if self.decision not in self.action_rh:
                return 0, self.rh, '16 vs. 8 @ TC 4+'

        # PH: 16  DH: 9, 10 or A
        # PH: 16  DH: 9, 10 or A  BS: [RH] surrender if -1<TC<4 or TC<=0 or TC<3 o/w hit
        elif self.dealer == 9 and -1 < self.count < 4 or self.dealer == 10 and self.count <= 0 or self.dealer == 11 and self.count < 3:
            if self.decision in self.action_rh:
                return 1
            if self.decision not in self.action_rh:
                return 0, self.rh, '16 vs. {9 @ -1 < TC < 4 // 10 @ TC <= 0 // A @ TC <3}'
        # PH: 16  DH: 9  BS: BS: [RH] surrender if -1<TC<4 o/w hit  Deviation: [H]it if TC -1-
        elif self.dealer == 9 and self.count <= -1:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '16 vs. 9 @ TC <= -1'
        # PH: 16  DH: 9, 10 or A  BS: [RH] surrender if -1<TC<4 or TC<=0 or TC<3 o/w hit  Deviation: [RS] surrender if TC 4+, 0+ or 3+ o/w stand
        elif self.dealer == 9 and self.count >= 4 or self.dealer == 10 and self.count > 0 or self.dealer == 11 and self.count >= 3:
            if self.decision in self.action_rs:
                return 1
            if self.decision not in self.action_rs:
                return 0, self.rs, '16 vs. {9 @ TC 4+ // 10 @ TC 0+ // A @ TC 3+}'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'sixteen')
    def seventeen_soft(self):
        # PH: A,6 (soft 17)  DH: 2
        # PH: A,6 (soft 17)  DH: 2  BS: [H]it
        if self.dealer == 2 and self.count < 1:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, 'A,6 vs. 2 @ TC < 1'
        # PH: A,6 (soft 17)  DH: 2  BS: [H]it  Deviation: [DH] double if TC 1+ o/w hit
        elif self.dealer == 2 and self.count >= 1:
            if self.decision in self.action_dh:
                return 1
            if self.decision not in self.action_dh:
                return 0, self.dh, 'A,6 vs. 2 @ TC 1+'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'seventeen_soft')
    def nineteen_soft(self):
        # PH: A,8 (soft 19)  DH: 4 or 5
        # PH: A,8 (soft 19)  DH: 4 or 5  BS: [S]tand
        if self.dealer == 4 and self.count < 3 or self.dealer == 5 and self.count < 1:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, 'A,8 vs. {4 @ TC < 3 // 5 @ TC < 1}'
        # PH: A,8 (soft 19)  DH: 4 or 5  BS: [S]tand  Deviation: [DS] double if TC 3+ or 1+ o/w stand
        elif self.dealer == 4 and self.count >= 3 or self.dealer == 5 and self.count >= 1:
            if self.decision in self.action_ds:
                return 1
            if self.decision not in self.action_ds:
                return 0, self.ds, 'A,8 vs. {4 @ TC 3+ // 5 @ TC 1+}'

        # PH: A,8 (soft 19)  DH: 6
        # PH: A,8 (soft 19)  DH: 6  BS: [DS] double o/w stand
        elif self.dealer == 6 and self.count >= 0:
            if self.decision in self.action_ds:
                return 1
            if self.decision not in self.action_ds:
                return 0, self.ds, 'A,8 vs. 6 @ TC >= 0'
        # PH: A,8 (soft 19)  DH: 6  BS: [DS] double o/w stand  Deviation: [S]tand if TC 0-
        elif self.dealer == 6 and self.count < 0:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, 'A,8 vs. 6 @ TC 0-'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'nineteen_soft')
    def pair_tens(self):
        # PH: 10,10  DH: 4, 5 or 6
        # PH: 10,10  DH: 4, 5 or 6  BS: [S]tand
        if self.dealer == 4 and self.count < 6 or self.dealer == 5 and self.count < 5 or self.dealer == 6 and self.count < 4:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, '10 vs. {4 @ TC < 6 // 5 @ TC < 5 // 6 @ TC < 4}'
        # PH: 10,10  DH: 4, 5 or 6  BS: [S]tand  Deviation: s[P]it if TC 6+, 5+ or 4+
        elif self.dealer == 4 and self.count >= 6 or self.dealer == 5 and self.count >= 5 or self.dealer == 6 and self.count >= 4:
            if self.decision in self.action_p:
                return 1
            if self.decision not in self.action_p:
                return 0, self.p, '10 vs. {4 @ TC 6+ // 5 @ TC 5+ // 6 @ TC 4+}'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'pair_tens')
    def insurance(self):
        # PH: X,X  DH: A (4, 5, 6, 7 or 18 for this game, o/w it will interfere with above methods)
        # PH: totals 4, 5, 6 or 7 DH: A  BS: [H]it
        if self.dealer == 11 and self.count < 3 and self.player in range(4,8):
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '4 thru 7 vs. A @ TC < 3 (basic strategy)'
        # PH: 18 DH: A  BS: [S]tand
        elif self.dealer == 11 and self.count < 3 and self.player == 18:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, '18 vs. A @ TC < 3 (basic strategy)'
        # PH: totals 4, 5, 6, 7 or 18  DH: A  BS: basic strategy  Deviation: [I]nsurance if TC 3+
        elif self.dealer == 11 and self.count >= 3:
            if self.decision in self.action_i:
                return 1
            if self.decision not in self.action_i:
                return 0, self.i, 'X,X vs. A @ TC 3+'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'insurance')
    def message_to_user(self):
        # Method to display message to user if they answered correctly or not; if not, the correct answer is provided
        correct = 'Correct'.rjust(19)
        incorrect = 'Incorrect: '.rjust(23)
        # Print message to user about whether their answer was correct
        # The scenario was answered correctly
        if self.result == 1:
            print(correct)
            print('\n')
        # The scenario was answered incorrectly
        elif self.result[0] == 0:
            print(incorrect + self.result[1] + self.result[2])
            print('\n')
        # The deviation decision tree logic did not execute as expected
        elif self.result[0] == 1000:
            print(self.result[1])
            print('\n')
        # The deviation decision tree logic did not execute as expected
        else:
            print('check method "message_to_user"')
            return 1000

    def deviation_correct_answer_tally(self):
        # Tally up correct Deviation answers
        # User input was correct; +1
        if self.result == 1:
            return 1
        # User input was incorrect; +0
        elif self.result[0] == 0:
            return 0
        # The deviation decision tree logic did not execute as expected; +1000`
        elif self.result[0] == 1000:
            return 1000
        # The method's logic did not execute as expected; +1000
        else:
            print('check method "tally"')
            return 1000

    def deviation_streak_tally(self):
        # Update the user's streak of correct answers
        # User input was correct; streak: +1
        if self.result == 1:
            self.deviation_streak[-1] += 1
        # User input was incorrect; streak back to 0; record the streak into the streak list
        elif self.result[0] == 0 or self.result[0] == 1000:
            self.deviation_streak.append(0)
        # The deviation decision tree logic did not execute as expected
        else:
            print('check method "streak_tally"')

    def run_decision_tree(self):
        # Runs through method based on player total (player[1])
        # Quit option for user input 'q'
        if self.decision == 'q':
            self.result = 'q'
        elif self.player == 8:
            self.result = Deviations_decision_tree.eight(self)
        elif self.player == 9:
            self.result = Deviations_decision_tree.nine(self)
        elif self.player == 10:
            self.result = Deviations_decision_tree.ten(self)
        elif self.player == 12:
            self.result = Deviations_decision_tree.twelve(self)
        elif self.player == 13:
            self.result = Deviations_decision_tree.thirteen(self)
        elif self.player == 14:
            self.result = Deviations_decision_tree.fourteen(self)
        elif self.player == 15:
            self.result = Deviations_decision_tree.fifteen(self)
        elif self.player == 16:
            self.result = Deviations_decision_tree.sixteen(self)
        elif self.player == 17:
            self.result = Deviations_decision_tree.seventeen_soft(self)
        elif self.player == 19:
            self.result = Deviations_decision_tree.nineteen_soft(self)
        elif self.player == 20:
            self.result = Deviations_decision_tree.pair_tens(self)
        elif self.player in range(4,8) or self.player == 18:
            self.result = Deviations_decision_tree.insurance(self)
        else:
            self.result = 1000, (self.check_program + 'run_decision_tree')

        Deviations_decision_tree.message_to_user(self)
        Deviations_decision_tree.deviation_streak_tally(self)
        deviation_correct = Deviations_decision_tree.deviation_correct_answer_tally(self)

        # Return variables to be used for evaluating performance of the user
        return self.deviation_streak, deviation_correct

def summary_file_check():
    # Check directory for file 'deviations_summary.csv' and create file if it does not exist.
    summary_file = 'deviations_summary.csv'
    if not os.path.isfile(summary_file):
            header = ["Date", "Time", "Rounds", "Average Time", "RC Mistakes", "RC Success Rate", "RC Streak",
                      "Dev Mistakes", "Dev Success Rate", "Dev Streak"]
            # open the file in the write mode
            f = open(summary_file, 'w', newline='')
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow(header)
            # close the file
            f.close()
    return summary_file
def record(summary_file):
    # Record the session performance
    today_date = datetime.datetime.now().strftime("%Y" + '.' + "%m" + '.' + "%d")

    # Calculate the total number of mistakes
    true_count_incorrect_answers = game_round - deviation_correct - 1
    deviation_incorrect_answers = game_round - deviation_correct - 1

    # If 0 games were played, cannot divide by 0; certain variables will be left undefined
    if game_round - 1 != 0:
        average_time = round(total_time / (game_round - 1), 2)

        true_count_success_rate = round(true_count_correct / (game_round - 1) * 100, 2)
        true_count_streak_ordered = sorted(true_count_streak)
        true_count_streak_best = true_count_streak_ordered[-1]

        deviation_success_rate = round(deviation_correct / (game_round - 1) * 100, 2)
        deviation_streak_ordered = sorted(deviation_streak)
        deviation_streak_best = deviation_streak_ordered[-1]

    else:
        average_time = 0

        true_count_success_rate = 0
        true_count_streak_best = 0

        deviation_success_rate = 0
        deviation_streak_best = 0
    try:
        with open(summary_file, 'a') as file:
            # Write the user's stats to a csv file
            file.writelines(
                # Date
                today_date + ', ' +
                # Time
                str(total_time) + ', ' +
                # Rounds
                str(game_round - 1) + ', ' +
                # Average Time
                str(average_time) + ', ' +
                # True Count Mistakes
                str(true_count_incorrect_answers) + ', ' +
                # True Count Success Rate
                str(true_count_success_rate) + ', ' +
                # True Count Streak
                str(true_count_streak_best) + ', ' +
                # Deviation Mistakes
                str(deviation_incorrect_answers) + ', ' +
                # Deviation Success Rate
                str(deviation_success_rate) + ', ' +
                # Deviation Streak
                str(deviation_streak_best) + ', \n' )
        return average_time, true_count_success_rate, true_count_streak_best, deviation_success_rate, deviation_streak_best
    except PermissionError:
        print("\n\nYou have the csv file open so it cannot be written to. This round's performance will not be saved "
              "or output.")
        exit()
def recent_performance(single_game_info):
    # Outputs the performance of the game that was just played
    print('\nPerformance')
    print('Total Time: ' + str(total_time) + ' seconds.')
    print('Total Hands: ' + str(game_round-1) + ' rounds.')
    print('Average Time Per Hand: ' + str(single_game_info[0]) + ' seconds.')
    print('True Count Success Rate: ' + str(single_game_info[1]) + '% answered correctly.')
    print('Deviation Success Rate: ' + str(single_game_info[3]) + '% answered correctly.')
    # If 0 games were played, variable 'update_streak' is not defined
    if game_round - 1 != 0:
        print('Best True Count Streak: ' + str(single_game_info[2]) + ' in a row.')
        print('Best Deviation Streak: ' + str(single_game_info[4]) + ' in a row.')
    else:
        pass
class Historical_performance():
    #
    def __init__(self, summary_file):
        self.summary_file = summary_file
        # Outputs all time high performance for accuracy, average time and streak
        self.df = pd.read_csv(summary_file, index_col=False)
            # CSV header = ["Date", "Time", "Rounds", "Average Time", "RC Mistakes", "RC Success Rate", "RC Streak",
            # "Dev Mistakes", "Dev Success Rate", "Dev Streak"]
        self.personal_best_avg_time = 1000
        self.personal_best_accuracy = 0
        self.no_rounds = 0
        self.time = 0
        self.x = 0

    def time_per_round(self):
    # Average time, minimum 25 rounds; no mistakes
        for entry in self.df['Rounds']:
            if entry >= 25 and self.df['Average Time'][self.x] < self.personal_best_avg_time and \
                    self.df['RC Mistakes'][self.x] == 0 and self.df['Dev Mistakes'][self.x] == 0:
                    self.personal_best_avg_time = self.df['Average Time'][self.x]
                    self.no_rounds = self.df['Rounds'][self.x]
            self.x += 1
        # Number of rounds initially 0; this will only print if the number of rounds is no longer 0
        if self.no_rounds != 0:
            print('P.B. avg. time (>25 rounds, 0 mistakes): %s rounds at %s seconds per round.' % \
                      (self.no_rounds, self.personal_best_avg_time))

    def true_count_accuracy(self):
        # Top Running Count accuracy, minimum 25 rounds
        for entry in self.df['Rounds']:
            if entry >= 25 and self.df['RC Success Rate'][self.x] > self.personal_best_accuracy:
                self.personal_best_accuracy = self.df['RC Success Rate'][self.x]
                self.no_rounds = self.df['Rounds'][self.x]
                self.time = self.df['Average Time'][self.x]
            self.x += 1
        if self.no_rounds != 0:
            print('P.B. top RC accuracy (>25 rounds): %s percent, %s rounds at %s seconds per round.' % \
                  (self.personal_best_accuracy, self.no_rounds, self.time))

    def deviation_accuracy(self):
        # Top Deviation accuracy, minimum 25 rounds
        for entry in self.df['Rounds']:
            if entry >= 25 and self.df['Dev Success Rate'][self.x] > self.personal_best_accuracy:
                    self.personal_best_accuracy = self.df['Dev Success Rate'][self.x]
                    self.no_rounds = self.df['Rounds'][self.x]
                    self.time = self.df['Average Time'][self.x]
            self.x += 1
        if self.no_rounds != 0:
            print('P.B. top Dev. accuracy (>25 rounds): %s percent, %s rounds at %s seconds per round.' % \
                  (self.personal_best_accuracy, self.no_rounds, self.time))

    def best_running_count_streak(self):
        # Best Running Count streak
        print('P.B. Running Count streak: ' + str(self.df['RC Streak'].max()) + ' rounds in a row.')

    def best_deviation_streak(self):
    # Best Deviation streak
        print('P.B. Deviation streak: ' + str(self.df['Dev Streak'].max()) + ' rounds in a row.')

# Begin the program!!
# Print instructions
instruction()

# Mark the start time for the game
game_time_start = time_current()

# Create object to store the list of deviation hands
dev_hands = deviation_hands()

# Game starts at Round 1 and will increment with every iteration of the game
game_round = 1

# The number of correct answers and the user's best streak start at 0
true_count_correct = 0
true_count_streak = [0]
deviation_correct = 0
deviation_streak = [0]

# Run this loop as long as the number of items in the dev_hands list is greater than zero
while len(dev_hands)>=1:
    print(('Round  ' + str(game_round)).ljust(11), end='')

    # Perform Running Count exercise; evaluate the user's submission for True Count
    running_count = Running_count(true_count_streak).running_count_instance()
    # Calculate the True Count
    count = running_count[0]
    # Update the true_count_streak list
    true_count_streak = running_count[1]
    # Increment for correct True Count answers
    true_count_correct += running_count[2]

    # Get a player hand and a dealer hand
    player_hand, player_total, dealer_hand, dealer_total = Deal(dev_hands).deal_instance()

    # Perform Deviation exercise; present the player hand, dealer hand and count to the user
    decision = deviation_game(player_hand, dealer_hand, count)
    # [q]uit command
    if decision == 'q':
        break

    # Evaluate the user's submission for Deviation
    deviation = Deviations_decision_tree(player_total, dealer_total, count, decision, deviation_streak).run_decision_tree()
    # Update the deviation_streak list
    deviation_streak = deviation[0]
    # Increment for correct Deviation answers
    deviation_correct += deviation[1]

    # Increment the game round
    game_round += 1
    # Print this message if all of the items from the dev_hands list have been removed.
    if len(dev_hands) == 0:
        print('\nYou have exhausted the list of scenarios.')

# Mark the ending time of the game
game_time_end = time_current()
# Calculate the total time
total_time = elapsed_game_time(game_time_start, game_time_end)

# Check to make sure a file exists in the directory that can accept the user's performance metrics
summary_file = summary_file_check()
# Record the performance of the game
single_game_info = record(summary_file)
# Output the performance of the game that was just played
recent_performance(single_game_info)
# Analyze the historical data in the summary file and print out notable past performances
print('\nPersonal Bests')
Historical_performance(summary_file).time_per_round()
Historical_performance(summary_file).true_count_accuracy()
Historical_performance(summary_file).deviation_accuracy()
Historical_performance(summary_file).best_running_count_streak()
Historical_performance(summary_file).best_deviation_streak()
# Done! The program is finished.
print('\n¡Hecho! ¡La programación esta terminada!\n\n')


# The situations outlined below should be confirmed by an industry professional
# check logic on <= and >= especially for 14, 15, 16 (confirm rounding logic for 0- and 0+ (i.e. -0.5 TC))
    # PH: 14  DH: 10  BS: [H]it  Deviation: [RH] surrender if TC 3+ o/w hit
    # PH: 15  DH: 9   BS: [H]it  Deviation: [RH] surrender if TC 2+ o/w hit
    # PH: 15  DH: 10  BS: [RH] surrender if 0<=TC<4 o/w hit  Deviation: [H]it if TC 0-; [RS] surrender if TC 4+ o/w stand
    # PH: 15  DH: A   BS: [RH] surrender if -1<=TC<5 o/w hit Deviation: [H]it if TC -1-; [RS] surrender if TC 5+ o/w stand
    # PH: 16  DH: 8   BS: [H]it  Deviation: [RH] surrender if TC 4+ o/w hit
    # PH: 16  DH: 9   BS: [RH] surrender if -1<TC<4 o/w hit Deviation: [H]it if TC -1-; [RS] surrender if TC 4+ o/w stand
    # PH: 16  DH: 10  BS: [RH] surrender if TC<=0 o/w hit Deviation: [RS] surrender if TC 0+ o/w stand
    # PH: 16  DH: A   BS: [RH] surrender if TC<3 o/w hit Deviation: [RS] surrender if TC 3+ o/w stand