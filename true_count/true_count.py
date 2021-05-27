import os
import csv
import random
import math
import datetime
import pandas as pd

today_date = datetime.datetime.now().strftime("%Y" + '.' + "%m" + '.' + "%d")
summary_file_average = 'true_count_summary.csv'

def summary_file_check():
    # Check directory for file named double_deck.csv and create file if it does not exist.
    if not os.path.isfile(summary_file_average):
            header = ["Date", "Time", "Rounds", "Average Time", "Mistakes", "Success Rate", "Streak"]
            # open the file in the write mode
            f = open(summary_file_average, 'w')
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow(header)
            # close the file
            f.close()
def instruction():
    # Instructions
    instructions = 'This game is called True Count and it will be used in conjunction with Microsoft \n' \
               "Excel file 'true_count_summary.csv'.  The goal is to properly equate the true count \n" \
               'as accurately and as quickly as possible.  You will be given a game (i.e. # of decks), as \n' \
               'well as a running count (positive or negative).  You will be tasked with entering the true\n'\
               'count (rounded down for + counts, and rounded up for - counts).  The program will record\n'\
               'how long it takes to enter in a true count, and record your level of accuracy.\n'
    print('\n*****     *****     *****     *****\n')
    print(instructions)
def game_time():
    game_no = 1
    correct_TC = 0
    incorrect_TC = 0
    streak = 0
    streak_list = []

    game_initial_time = datetime.datetime.now()

    while True:
        # Randomly choose how many decks are being played
        possible_no_decks = [2, 4, 6, 8]
        no_decks = possible_no_decks[random.randint(0,3)]

        # How many decks have been played
        possible_decks_played = []
        x= .5
        for increment in range(0, 2*no_decks):
            possible_decks_played.append(no_decks - x)
            x += .5
        decks_played = possible_decks_played[random.randint(0, 2*no_decks-1)]

        # Create the limits for the running count
        #remaining_decks = no_decks - decks_played
        rc_limit = no_decks * 10
        rc = random.randint(-rc_limit, rc_limit)

        # Mark the time for the beginning of the round
        initial_time = datetime.datetime.now()

        round_string = 'Round ' + str(game_no)
        deck_string = 'Decks: ' + str(no_decks)
        decks_played_string = 'Decks played: ' + str(decks_played)
        rc_string = 'RC: ' + str(rc)

        print(round_string.ljust(11), end='')
        print(deck_string.ljust(11), end='')
        print(decks_played_string.ljust(20), end='')
        print(rc_string.ljust(10), end='')

        # Prompt user for the true count
        tc_user = input('What is the true count? ')

        while True:
            try:
                if tc_user == 'q':
                    print('')
                    break
                int(tc_user)
                break
            except ValueError:
                print((' '*52) + 'You did not enter a number.')
                print(' '*52, end='')
                tc_user = input('What is the true count? ')
                continue

        if tc_user == 'q':
            print('')
            break

        # Mark the end of the round
        end_time = datetime.datetime.now()
        delta_time = end_time - initial_time
        time_integer = round(delta_time.total_seconds(), 1)

        # Calculate the True Count
        tc = rc / (no_decks - decks_played)
        if tc > 0:
            tc = math.floor(tc)
        elif tc < 0:
            tc = math.ceil(tc)
        else:
            tc = 0

        # Print a message telling the user if they were correct or not
        if tc - int(tc_user) == 0:
            print((' '*52) + 'Correct. (' + str(time_integer) + ' seconds)')
            #print(str('\t' * 2) + 'Correct. The TC is ' + str(tc) + '.', end='')
            correct_TC += 1
            streak += 1
        else:
            print((' '*52) + 'Incorrect (' + str(time_integer) + ' seconds): ', end='')
            print(str(tc))
            #print(str('\t' * 2) + 'Incorrect. The TC is ' + str(tc) + '.', end='')
            incorrect_TC += 1
            streak_list.append(streak)
            streak = 0
        #print(str('\t\tTime: ') + str(time_integer) + ' seconds')

        game_no += 1

    streak_list.append(streak)
    # Mark the total time that has elapsed since starting the program
    game_end_time = datetime.datetime.now()
    game_delta_time = game_end_time - game_initial_time
    game_time_integer = round(game_delta_time.total_seconds(), 1)

    try:
        time_per_round = round(game_time_integer / (game_no-1),1)
        success_rate = round((100 * correct_TC / (game_no-1)), 1)

        print('Summary:\n' + str(game_no-1) + ' round(s) in ' + str(game_time_integer) + ' seconds ', end='')
        print('(' + str(time_per_round) + ' sec/round). ', end='')
        print(str(success_rate) + '% success rate (' + str(incorrect_TC) + ' wrong).')
        # Streak
        streak_list.sort()
        print('Best streak this session: ', end='')
        print(streak_list[-1])

        with open(summary_file_average, 'a') as file:
            file.writelines(
                today_date + ', ' +
                str(game_time_integer) + ', ' +
                str(game_no - 1) + ', ' +
                str(time_per_round) + ', ' +
                str(incorrect_TC) + ', ' +
                str(success_rate) + ', ' +
                str(streak_list[-1]) + '\n')

    except ZeroDivisionError:
        print('Summary:')
        print('You played 0 games.')
def performance_metrics():

    df = pd.read_csv(summary_file_average)

    # Quickest, flawless round
    pb_avg_time = 1000
    no_rounds = 0
    counter = 0
    for entry in df['Rounds']:
        if entry >= 10:
            if df['Average Time'][counter] < pb_avg_time and df['Success Rate'][counter] == 100:
                pb_avg_time = df['Average Time'][counter]
                no_rounds = df['Rounds'][counter]
        counter += 1
    print('P.B. average time (min. 10 rounds, 0 mistakes): ' + str(pb_avg_time) + ' second(s)/round, ' + str(no_rounds)
          + ' rounds.')

    # Quickest, non flawless round
    pb_pct = 0
    pb_avg = 1000
    no_rounds = 0
    counter = 0
    for entry in df['Rounds']:
        if entry >= 20:
            if df['Average Time'][counter] < pb_avg:
                pb_pct = df['Success Rate'][counter]
                pb_avg = df['Average Time'][counter]
                no_rounds = df['Rounds'][counter]
        counter += 1
    print('P.B. average time (min. 20 rounds): ' + str(pb_avg) + ' seconds/round, ' + str(no_rounds) +
          ' rounds (' + str(pb_pct) + '%).')

    # Longest Streak
    pb_streak = 0
    counter = 0
    for entry in df['Streak']:
        if entry > pb_streak:
            pb_streak = entry
        counter += 1
    print('P.B. streak: ' + str(pb_streak) + ' in a row.\n')

summary_file_check()
instruction()
input('\nPress enter to begin.\n')
game_time()
performance_metrics()
