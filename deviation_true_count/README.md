# deviations.py

Welcome to Blackjack Deviations! This program is useful for practicing two exercises that
are critical to successful card counting:

        (i)  True Count calculations
        (ii) Deviation decisions
        
Directions for True Count exercise:

        Step 1: Three variables are printed:
                - Decks: total number of cards decks in the game
                - DP (Decks Played): number of decks that have already been played
                - RC (Running Count): the count which players apply in order to determine the
                        true count by counting the cards during the course of the game, using
                        a particular card counting system. The popular card counting system
                        is called "Hi-Lo" where cards 2, 3, 4, 5 & 6 have value of +1, cards
                        7,8 & 9 have a value of 0, and cards 10, J, Q, K, & A have value -1.
                        For this exercise, the Running Count is given.

        Step 2: Calculate the True Count based on the "Hi-Lo" system:
                - True Count = Running Count / (Decks - Decks Played)
                        For True Counts > 0: round down to the nearest integer
                        For True Counts < 0: round up to the nearest integer

        Step 3: Input the True Count integer and the program will check for correctness:
                - The message "Correct" will appear for correct answers
                - The message "Incorrect" will appear for incorrect answers
                - The correct True Count (TC) will be shown as part of the Deviation exercise
                
Directions for Deviation exercise:

        Step 1: Three variables are printed:
                - PH (Player Hand): two cards are assigned to the player
                - DH (Dealer Hand): one card is assigned to the dealer
                - TC (True Count): RC / (Decks - DP)

        Step 2: Input the correct play based on Basic Strategy, True Count & Deviations:
                - [H]it                                 - s[P]lit
                - [S]tand                               - [RH] surrender o/w hit
                - [DH] double otherwise (o/w) hit       - [RS] surrender o/w stand
                - [DS] double o/w stand                 - [I]nsurance

                Example: enter "H" if the correct decision is [H]it

User inputs are not case sensitive.

The object of the game is to answer as accurately and as quickly as possible.

A summary file will be created at the completion of the program to log the user's performance.
