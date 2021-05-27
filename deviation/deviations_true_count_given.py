import os
import csv
import random
import datetime
import pandas as pd
import webbrowser

# TO DO:
# make it more challenging by making the user calculate the running count

# check logic on <>=, especially for 14, 15, 16 (confirm rounding logic for 0- and 0+ (i.e. -0.5 TC))
    # PH: 14  DH: 10  BS: [H]it  Deviation: [RH] surrender if TC 3+ o/w hit
    # PH: 15  DH: 9   BS: [H]it  Deviation: [RH] surrender if TC 2+ o/w hit
    # PH: 15  DH: 10  BS: [RH] surrender if 0<=TC<4 o/w hit  Deviation: [H]it if TC 0-; [RS] surrender if TC 4+ o/w stand
    # PH: 15  DH: A   BS: [RH] surrender if -1<=TC<5 o/w hit Deviation: [H]it if TC -1-; [RS] surrender if TC 5+ o/w stand
    # PH: 16  DH: 8   BS: [H]it  Deviation: [RH] surrender if TC 4+ o/w hit
    # PH: 16  DH: 9   BS: [RH] surrender if -1<TC<4 o/w hit Deviation: [H]it if TC -1-; [RS] surrender if TC 4+ o/w stand
    # PH: 16  DH: 10  BS: [RH] surrender if TC<=0 o/w hit Deviation: [RS] surrender if TC 0+ o/w stand
    # PH: 16  DH: A   BS: [RH] surrender if TC<3 o/w hit Deviation: [RS] surrender if TC 3+ o/w stand

def instruction():
    # Instructions discussing object of the game
    instructions = 'This game is called Blackjack Deviations and it will be used in conjunction with notepad \n' \
                "file 'deviations_summary.csv'.  The object of the game is to properly decide deviation \n" \
                "strategy as accurately and as quickly as possible.  The program will present you with a true\n" \
                "count, a dealer hand, and a player hand.  Your job is to input the correct play: \n\t[H]it" \
                "\n\t[S]tand\n\t[DH] double otherwise (o/w) hit\n\t[DS] double o/w stand\n\ts[P]lit" \
                "\n\t[RH] surrender o/w hit\n\t[RS] surrender o/w stand\n\t[I]nsurance. \n\n**Enter 'q' at any time "\
                "to end the program.**\n"
    print('\n*****     *****     *****     *****\n')
    print(instructions)

    deviations_video = 'https://www.blackjackapprenticeship.com/blackjack-deviations/'
    watch_video = input('If you would like to watch a quick video to further explain deviations, type "Y".\n'
                        'Otherwise, press "enter" to continue or press [q]uit.\n\n')
    if watch_video == 'Y':
        webbrowser.open(deviations_video)
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
def deal(dev_hands):
    # Pop one list (each list contains 3 items) from the 'dev_hands' list (method: def deviation_hands():)
    # The first two items in the popped list represent the player cards; the third item represents the dealer card
    if len(dev_hands)>=1:
        random.shuffle(dev_hands)
        cards_dealt = dev_hands.pop()
        return cards_dealt
def deal_to_player(cards_dealt):
    # Assign the first two items from the popped 'dev_hands' list to the player_hand
    player_hand = cards_dealt[0:2]
    player_total = 0

    # Add first and second card to player total
    for z in range(0,2):
        # Aces: since this program only handles 2 player cards at a time, an Ace is valued at 11 and never valued at 1
        if player_hand[z] == 'A': player_total += 11
        # Tens: add 10 to the player total and then re-assign 10 card to a 10 or face card
        elif player_hand[z] == 10:
            player_total += player_hand[z]
            tens_assignment = [10, 'J', 'Q', 'K']
            player_hand[z] = tens_assignment[random.randint(0,3)]
        # If item is not a 10 or A, then add the integer to the player total
        else:
            player_total += player_hand[z]
    return player_hand, player_total
def deal_to_dealer(cards_dealt):
    # Assign the third item from the popped 'dev_hands' list to the dealer_hand
    dealer_hand = cards_dealt[2]
    dealer_total = 0

    # Add card to the dealer total
    # Aces: an Ace is valued at 11; never 1
    if dealer_hand == 'A': dealer_total += 11
    # Tens: add 10 to the dealer total and then re-assign 10 card to a 10 or face card
    elif dealer_hand == 10:
        dealer_total += dealer_hand
        tens_assignment = [10, 'J', 'Q', 'K']
        dealer_hand = tens_assignment[random.randint(0,3)]
    # If item is not a 10 or A, then add the integer to the player total
    else:
        dealer_total += dealer_hand
    return dealer_hand, dealer_total
def true_count():
    # A random True Count is provided
    # The True Count dictates when a deviation from blackjack basic strategy should occur
    # This is a parallel method to 'def running_count():' and is for beginners learning the deviations
    # At a minimum, the range should cover (-3,+6)
    true_count = random.randint(-10,10)
    return true_count
def running_count():
    # Rounding is to follow the 'floor' rounding method for +TC and 'ceiling' rounding method for -TC
        # This presents a unique issue to any deviations that based on +/- running counts
            # 12 vs 4, 15 vs 10, 16 vs 10 and soft 19 v 6
            # This requires unique handling to true counts calculate to be -1<TC<1
    # This method is incomplete and not available to the program yet
    # A random running count, decks played, and total decks are provided and the user will mentally calculate the TC
    # This is a parallel method to 'def true_count():' and is for more advanced users
    running_count = random.randint(-(no_decks*10), no_decks*10)

    # How many decks have been played
    possible_decks_played = []
    x = .5
    for increment in range(0, 2 * no_decks):
        possible_decks_played.append(no_decks - x)
        x += .5
    decks_played = possible_decks_played[random.randint(0, 2 * no_decks - 1)]

    print('No. deck: ' + str(no_decks))
    print('Decks played: ' + str(decks_played))
    print('RC: ' + str(running_count))

    return running_count
def play_game(player, dealer, count):
    # A single round of the game is presented to the user and they are asked to provide the correct decision
    # PH: Player Hand; DH: Dealer Hand; BS: Basic Strategy; TC: True Count; RC: Running Count; o/w: otherwise

    # String formatting and printing of the cards for a single round of the game
    str_player_hand = 'PH: ' + str(player[0][0]) + ' ' + str(player[0][1])
    str_dealer_hand = 'DH: ' + str(dealer[0])
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
    def __init__(self, player, dealer, count, decision):
        # player[0] = list of two player cards (2-10,J,K or A); player[1] = player total as an integer
        self.player = player
        # dealer[0] = dealer card (2-10,J,K or A); dealer[1] = dealer total as an integer
        self.dealer = dealer
        # count = integer used to decide deviations from basic strategy
        self.count = count
        # decision = user input (H, S, DH, DS, P, RH, RS, or I)
        self.decision = decision
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
        if self.dealer[1] == 6 and self.count < 2:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '8 vs. 6 @ TC < 2'
        # PH: 8  DH: 6  BS: [H]it  Deviation: [DH] double if TC 2+ o/w hit
        elif self.dealer[1] == 6 and self.count >= 2:
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
        if self.dealer[1] == 2 and self.count < 1 or self.dealer[1] == 7 and self.count < 3:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '9 vs. {2 @ TC < 1 // 7 @ TC < 3}'
        # PH: 9  DH: 2 or 7  BS: [H]it  Deviation: [DH] double if TC 1+ or 3+ o/w hit
        elif self.dealer[1] == 2 and self.count >= 1 or dealer[1] == 7 and self.count >= 3:
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
        if self.dealer[1] == 10 and self.count < 4 or self.dealer[1] == 11 and self.count < 3:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '10 vs. {10 @ TC < 4 // A @ TC < 3}'
        # PH: 10  DH: 10 or A  BS: [H]it  Deviation: [DH] double if TC 4+ or 3+ o/w hit
        elif self.dealer[1] == 10 and self.count >= 4 or self.dealer[1] == 11 and self.count >= 3:
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
        if self.dealer[1] == 2 and self.count < 3 or self.dealer[1] == 3 and self.count < 2:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h,  '12 vs. {2 @ TC < 3 // 3 @ TC < 2}'
        # PH: 12  DH: 2 or 3  BS: [H]it  Deviation: [S]tand if TC 3+ or 2+
        elif self.dealer[1] == 2 and self.count >= 3 or self.dealer[1] == 3 and self.count >= 2:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s,  '12 vs. {2 @ TC 3+ // 3 @ TC 2+}'

        # PH: 12  DH: 4, 5 or 6
        # PH: 12  DH: 4, 5 or 6  BS: [S]tand
        elif self.dealer[1] == 4 and self.count >= 0 or self.dealer[1] == 5 and self.count > -2 or self.dealer[1] == 6 and self.count > -1:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, '12 vs. {4 @ TC >=0 // 5 @ TC >-2 // 6 @ TC >-1}'
        # PH: 12  DH: 4, 5 or 6  BS: [S]tand  Deviation: [H]it if TC 0-, -2-, or -1-
        elif self.dealer[1] == 4 and self.count < 0 or self.dealer[1] == 5 and self.count <= -2 or self.dealer[1] == 6 and self.count <= -1:
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
        if self.dealer[1] == 2 and self.count > -1 or self.dealer[1] == 3 and self.count > -2:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, '13 vs. {2 @ TC > -1 // 3 @ TC > -2}'
        # PH: 13  DH: 2 or 3  BS: [S]tand  Deviation: [H]it if TC -1- or -2-
        elif self.dealer[1] == 2 and self.count <= -1 or self.dealer[1] == 3 and self.count <= -2:
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
        if self.dealer[1] == 10 and self.count < 3:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '14 vs. 10 @ TC < 3'
        # PH: 14  DH: 10  BS: [H]it  Deviation: [RH] surrender if TC 3+ o/w hit
        elif self.dealer[1] == 10 and self.count >= 3:
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
        if self.dealer[1] == 9 and self.count < 2:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '15 vs. 9 @ TC < 2'
        # PH: 15  DH: 9  BS: [H]it  Deviation: [RH] surrender if TC 2+ o/w hit
        elif self.dealer[1] == 9 and self.count >= 2:
            if self.decision in self.action_rh:
                return 1
            if self.decision not in self.action_rh:
                return 0, self.rh, '15 vs. 9 @ TC 2+'

        # PH: 15  DH: 10 or A
        # PH: 15  DH: 10 or A  BS: [RH] surrender if 0<=TC<4 or -1<=TC<5 o/w hit
        elif self.dealer[1] == 10 and 0 <= self.count < 4 or self.dealer[1] == 11 and -1 <= self.count < 5:
            if self.decision in self.action_rh:
                return 1
            if self.decision not in self.action_rh:
                return 0, self.rh, '15 vs. {10 @ 0 <= TC < 4 // A @ -1 <= TC < 5}'
        # PH: 15  DH: 10 or A  BS: [RH] surrender if 0<=TC<4 or -1<=TC<5 o/w hit  Deviation: [H]it if TC 0- or -1-
        elif self.dealer[1] == 10 and self.count < 0 or self.dealer[1] == 11 and self.count < -1:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '15 vs. {10 @ TC 0- // A @ TC -1-}'
        # PH: 15  DH: 10 or A  BS: [RH] surrender if 0<=TC<4 or -1<=TC<5 o/w hit  Deviation: [RS] surrender if TC 4+ or 5+ o/w stand
        elif self.dealer[1] == 10 and self.count >= 4 or self.dealer[1] == 11 and self.count >= 5:
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
        if self.dealer[1] == 8 and self.count < 4:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '16 vs. 8 @ TC < 4'
        # PH: 16  DH: 8  BS: [H]it  Deviation: [RH] surrender if TC 4+ o/w hit
        elif self.dealer[1] == 8 and self.count >= 4:
            if self.decision in self.action_rh:
                return 1
            if self.decision not in self.action_rh:
                return 0, self.rh, '16 vs. 8 @ TC 4+'

        # PH: 16  DH: 9, 10 or A
        # PH: 16  DH: 9, 10 or A  BS: [RH] surrender if -1<TC<4 or TC<=0 or TC<3 o/w hit
        elif self.dealer[1] == 9 and -1 < self.count < 4 or self.dealer[1] == 10 and self.count <= 0 or self.dealer[1] == 11 and self.count < 3:
            if self.decision in self.action_rh:
                return 1
            if self.decision not in self.action_rh:
                return 0, self.rh, '16 vs. {9 @ -1 < TC < 4 // 10 @ TC <= 0 // A @ TC <3}'
        # PH: 16  DH: 9  BS: BS: [RH] surrender if -1<TC<4 o/w hit  Deviation: [H]it if TC -1-
        elif self.dealer[1] == 9 and self.count <= -1:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '16 vs. 9 @ TC <= -1'
        # PH: 16  DH: 9, 10 or A  BS: [RH] surrender if -1<TC<4 or TC<=0 or TC<3 o/w hit  Deviation: [RS] surrender if TC 4+, 0+ or 3+ o/w stand
        elif self.dealer[1] == 9 and self.count >= 4 or self.dealer[1] == 10 and self.count > 0 or self.dealer[1] == 11 and self.count >= 3:
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
        if self.dealer[1] == 2 and self.count < 1:
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, 'A,6 vs. 2 @ TC < 1'
        # PH: A,6 (soft 17)  DH: 2  BS: [H]it  Deviation: [DH] double if TC 1+ o/w hit
        elif self.dealer[1] == 2 and self.count >= 1:
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
        if self.dealer[1] == 4 and self.count < 3 or self.dealer[1] == 5 and self.count < 1:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, 'A,8 vs. {4 @ TC < 3 // 5 @ TC < 1}'
        # PH: A,8 (soft 19)  DH: 4 or 5  BS: [S]tand  Deviation: [DS] double if TC 3+ or 1+ o/w stand
        elif self.dealer[1] == 4 and self.count >= 3 or self.dealer[1] == 5 and self.count >= 1:
            if self.decision in self.action_ds:
                return 1
            if self.decision not in self.action_ds:
                return 0, self.ds, 'A,8 vs. {4 @ TC 3+ // 5 @ TC 1+}'

        # PH: A,8 (soft 19)  DH: 6
        # PH: A,8 (soft 19)  DH: 6  BS: [DS] double o/w stand
        elif self.dealer[1] == 6 and self.count >= 0:
            if self.decision in self.action_ds:
                return 1
            if self.decision not in self.action_ds:
                return 0, self.ds, 'A,8 vs. 6 @ TC >= 0'
        # PH: A,8 (soft 19)  DH: 6  BS: [DS] double o/w stand  Deviation: [S]tand if TC 0-
        elif self.dealer[1] == 6 and self.count < 0:
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
        if self.dealer[1] == 4 and self.count < 6 or self.dealer[1] == 5 and self.count < 5 or self.dealer[1] == 6 and self.count < 4:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, '10 vs. {4 @ TC < 6 // 5 @ TC < 5 // 6 @ TC < 4}'
        # PH: 10,10  DH: 4, 5 or 6  BS: [S]tand  Deviation: s[P]it if TC 6+, 5+ or 4+
        elif self.dealer[1] == 4 and self.count >= 6 or self.dealer[1] == 5 and self.count >= 5 or self.dealer[1] == 6 and self.count >= 4:
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
        if self.dealer[1] == 11 and self.count < 3 and self.player[1] in range(4,8):
            if self.decision in self.action_h:
                return 1
            if self.decision not in self.action_h:
                return 0, self.h, '4 thru 7 vs. A @ TC < 3 (basic strategy)'
        # PH: 18 DH: A  BS: [S]tand
        elif self.dealer[1] == 11 and self.count < 3 and self.player[1] == 18:
            if self.decision in self.action_s:
                return 1
            if self.decision not in self.action_s:
                return 0, self.s, '18 vs. A @ TC < 3 (basic strategy)'
        # PH: totals 4, 5, 6, 7 or 18  DH: A  BS: basic strategy  Deviation: [I]nsurance if TC 3+
        elif self.dealer[1] == 11 and self.count >= 3:
            if self.decision in self.action_i:
                return 1
            if self.decision not in self.action_i:
                return 0, self.i, 'X,X vs. A @ TC 3+'

        # String only appears if above logic does not execute as expected
        else:
            return 1000, (self.check_program + 'insurance')
    def run_decision_tree(self):
        # Runs through method based on player total (player[1])
        # Quit option for user input 'q'
        if self.decision == 'q':
            result = 'q'
        elif self.player[1] == 8:
            result = Deviations_decision_tree.eight(self)
        elif self.player[1] == 9:
            result = Deviations_decision_tree.nine(self)
        elif self.player[1] == 10:
            result = Deviations_decision_tree.ten(self)
        elif self.player[1] == 12:
            result = Deviations_decision_tree.twelve(self)
        elif self.player[1] == 13:
            result = Deviations_decision_tree.thirteen(self)
        elif self.player[1] == 14:
            result = Deviations_decision_tree.fourteen(self)
        elif self.player[1] == 15:
            result = Deviations_decision_tree.fifteen(self)
        elif self.player[1] == 16:
            result = Deviations_decision_tree.sixteen(self)
        elif self.player[1] == 17:
            result = Deviations_decision_tree.seventeen_soft(self)
        elif self.player[1] == 19:
            result = Deviations_decision_tree.nineteen_soft(self)
        elif self.player[1] == 20:
            result = Deviations_decision_tree.pair_tens(self)
        elif self.player[1] in range(4,8) or self.player[1] == 18:
            result = Deviations_decision_tree.insurance(self)
        else:
            result = 1000, (self.check_program + 'run_decision_tree')
        return result
def message_to_user(result):
    # Method to display message to user if they answered correctly or not; if not, the correct answer is provided
    correct = 'Correct'.rjust(18)
    incorrect = 'Incorrect: '.rjust(22)
    # Print message to user about whether their answer was correct
    # The scenario was answered correctly
    if result == 1:
        print(correct)
        print('\n')
    # The scenario was answered incorrectly
    elif result[0] == 0:
        print(incorrect + result[1] + result[2])
        print('\n')
    # The deviation decision tree logic did not execute as expected
    elif result[0] == 1000:
        print(result[1])
        print('\n')
    # The deviation decision tree logic did not execute as expected
    else:
        print('check method "message_to_user"')
def correct_answer_tally(result):
    # Tally up correct answers
    # User input was correct; +1
    if result == 1:
        return 1
    # User input was incorrect; +0
    elif result[0] == 0:
        return 0
    # The deviation decision tree logic did not execute as expected; +1000`
    elif result[0] == 1000:
        return 1000
    # The method's logic did not execute as expected; +1000
    else:
        print('check method "tally"')
        return 1000
def streak_tally(result, streak):
    # Update the user's streak of correct answers
    # User input was correct; streak: +1
    if result == 1:
        streak[-1] += 1
    # User input was incorrect; streak back to 0; record the streak into the streak list
    elif result[0] == 0 or result[0] == 1000:
        streak.append(0)
    # The deviation decision tree logic did not execute as expected
    else:
        print('check method "streak_tally"')
    return streak
def summary_file_check():
    # Check directory for file 'deviations_summary.csv' and create file if it does not exist.
    summary_file = 'deviations_summary_true_count_given.csv'
    if not os.path.isfile(summary_file):
            header = ["Date", "Time", "Rounds", "Average Time", "Mistakes", "Success Rate", "Streak"]
            # open the file in the write mode
            f = open(summary_file, 'w')
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

    # If 0 games were played, cannot divide by 0; average_time = 0
    try:
        average_time = round(total_time / (game_round - 1), 2)
    except ZeroDivisionError:
        average_time = 0
    # If 0 games were played, cannot divide by 0; success_rate = 0
    try:
        success_rate = round(correct_answers/(game_round-1)*100,2)
    except ZeroDivisionError:
        success_rate = 0

    # If 0 games were played, variable 'update_streak' is not defined
    try:
        streak_ordered = sorted(update_streak)
        streak_best = streak_ordered[-1]
    except NameError:
        streak_best = 0


    with open(summary_file, 'a') as file:
        file.writelines(
            # Date
            today_date + ', ' +
            # Time
            str(total_time) + ', ' +
            # Rounds
            str(game_round - 1) + ', ' +
            # Average Time
            str(average_time) + ', ' +
            # Mistakes
            str(incorrect_answers) + ', ' +
            # Success Rate
            str(success_rate) + ', ' +
            #Streak
            str(streak_best) + ', \n' )
    return average_time, success_rate
def recent_performance(single_game_info):
    # Outputs the performance of the game that was just played
    print('\nPerformance')
    print('Total time: ' + str(total_time) + ' seconds.')
    print('Total Hands: ' + str(game_round-1) + ' rounds.')
    print('Average time per hand: ' + str(single_game_info[0]) + ' seconds.')
    print('Success rate: ' + str(single_game_info[1]) + '% answered correctly.')
    # If 0 games were played, variable 'update_streak' is not defined
    try:
        print('Best streak: ' + str(int(update_streak[-1])) + ' in a row.')
    except NameError:
        pass
def historical_performance(summary_file):
    # Outputs all time high performance for accuracy, average time and streak
    df = pd.read_csv(summary_file)
    # header = ["Date", "Time", "Rounds", "Average Time", "Mistakes", "Success Rate", "Streak"]
    print('\nPersonal Bests')
    # Average time, minimum 25 rounds; no mistakes
    pb_avg_time = 1000
    no_rounds = 0
    counter = 0
    for entry in df['Rounds']:
        if entry >= 25 and df['Average Time'][counter] < pb_avg_time and df['Mistakes'][counter] == 0:
                pb_avg_time = df['Average Time'][counter]
                no_rounds = df['Rounds'][counter]
        counter += 1
    # Number of rounds initially 0; this will only print if the number of rounds is no longer 0
    if no_rounds != 0:
        print('P.B. avg. time (>25 rounds, 0 mistakes): ' +
              str(no_rounds)  + ' rounds at ' +
              str(pb_avg_time) + ' seconds per round.')

    # Top accuracy, minimum 25 rounds
    pb_accuracy = 0
    no_rounds = 0
    counter = 0
    time = 0
    for entry in df['Rounds']:
        if entry >= 25 and df['Success Rate'][counter] > pb_accuracy:
                pb_accuracy = df['Success Rate'][counter]
                no_rounds = df['Rounds'][counter]
                time = df['Average Time'][counter]
        counter += 1
    if no_rounds != 0:
        print('P.B. top accuracy (>25 rounds): ' +
              str(pb_accuracy) + '%, ' +
              str(no_rounds)  + ' rounds at ' +
              str(time) + ' seconds per round.')

    # Best streak
    try:
        print('P.B. streak: ' + str(int(df['Streak'].max())) + ' rounds in a row.')
    except ValueError:
        pass

    print('\n\n')


# Begin the program
instruction()
game_time_start = time_current()
deviations = deviation_hands()

correct_answers = 0
game_round = 1
streak = [0]

while len(deviations)>=1:
    print(('Round ' + str(game_round)).ljust(11), end='')
    cards_dealt = deal(deviations)
    player = deal_to_player(cards_dealt)
    dealer = deal_to_dealer(cards_dealt)
    # Either running count or true_count(): method or running_count(): method can be used
    count = true_count()
    #count = running_count()
    decision = play_game(player, dealer, count)
    if decision == 'q':
        break
    result = Deviations_decision_tree(player, dealer, count, decision).run_decision_tree()
    message_to_user(result)
    correct_answers += correct_answer_tally(result)
    update_streak = streak_tally(result, streak)
    game_round += 1
    if len(deviations) == 0:
        print('\nYou have exhausted the list of scenarios.')

game_time_end = time_current()
total_time = elapsed_game_time(game_time_start, game_time_end)
incorrect_answers = game_round - correct_answers -1

summary_file = summary_file_check()
single_game_info = record(summary_file)
recent_performance(single_game_info)
historical_performance(summary_file)
