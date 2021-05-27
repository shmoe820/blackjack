import os
import csv
import random
import datetime
import pandas as pd
import sys
import statistics

today_date = datetime.datetime.now().strftime("%Y" + '.' + "%m" + '.' + "%d")
summary_file = 'double_deck.csv'
exercise_times = []
mistakes_made = []

def summary_file_check():
    # Check directory for file named double_deck.csv and create file if it does not exist.
    if not os.path.isfile(summary_file):
            header = ["Date", "Time", "Count"]
            # open the file in the write mode
            f = open(summary_file, 'w')
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow(header)
            # close the file
            f.close()
def instruction():
    # Instructions
    instructions = 'This game is called Double Deck Countdown and it will be used in conjunction with Microsoft \n' \
               "Excel file 'double_deck.csv'.  The object of the game is to properly count down two decks as \n" \
               'accurately and as quickly as possible.  As the user, you will start the timer using the \n' \
               "'enter' key when prompted, and hit it again once you have completed the two deck.  \n" \
               "Enter the count (in absolute value) accuracy purposes. Time penalty per mistake is 10 seconds."
    print('\n*****     *****     *****     *****\n')
    print(instructions)
def game_time():
    while True:
        print('\nRound ' + str(len(exercise_times) + 1))
        start_game = input("Press 'enter' when ready to begin or [q]uit. ")
        if start_game == 'q':
            break

        initial_time = datetime.datetime.now()

        completion = input("Hit 'enter' to call time or [q]uit.")
        if completion == 'q':
            break

        end_time = datetime.datetime.now()
        delta_time = end_time - initial_time
        time_integer = round((delta_time.total_seconds()), 2)

        while True:
            try:
                mistakes = input('Enter the count: ')
                if mistakes == 'q':
                    break
                elif mistakes != '0':
                    time_integer += 10*int(mistakes)
                    exercise_times.append(time_integer)
                    exercise_times.append(time_integer)
                    mistakes_made.append(mistakes)
                    with open(summary_file, 'a') as file:
                        file.writelines(today_date + ', ' + str(time_integer) + '{}'.format(', ') + mistakes + '\n')
                else:
                    exercise_times.append(time_integer)
                    mistakes_made.append(mistakes)
                    with open(summary_file, 'a') as file:
                        file.writelines(today_date + ', ' + str(time_integer) + '{}'.format(', ') + mistakes + '\n')
                print('Time: %s seconds.' % time_integer)
                break
            except ValueError:
                print('You did not enter a number.')
                continue

def performance_metrics():
    summary_file_average = 'double_deck_average.csv'
    # Check directory for file named basic_strategy.csv and create file if it does not exist.
    if not os.path.isfile(summary_file_average):
            header = ["Date", "No. of Games", "Average Time", "Count", "S_D"]
            # open the file in the write mode
            f = open(summary_file_average, 'w')
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow(header)
            # close the file
            f.close()

    total_time = 0
    for times in exercise_times:
        total_time += times

    total_mistakes = 0
    for mistakes in mistakes_made:
        total_mistakes += int(mistakes)

    try:
        avg_time = round(total_time / len(exercise_times), 2)
        s_d = str(round(statistics.stdev(exercise_times), 2))
        print("\n\nYou completed %s deck(s) with %s mistakes."
              "\nAverage time = %s seconds per deck. " % (len(exercise_times), total_mistakes, avg_time))
        print("The standard deviation was " + s_d + ' seconds.\n')
    except ZeroDivisionError:
        print("You played 0 games.\n")
        exit()

    try:
        with open(summary_file_average, 'a') as file:
            file.writelines(today_date + ', ' + str(len(exercise_times)) + ', ' + str(avg_time) + ', ' +
                            str(total_mistakes) + ', ' + s_d + '\n')
    except PermissionError:
        print("The file you are trying to write to is open.\n")


    personal_best = 1000
    personal_best_s_d = 1000
    personal_best_s_d_avg = 1000
    counter = 0
    df = pd.read_csv(summary_file_average)

    for entry in df['No. of Games']:
        if entry >= 5:
            if df['Average Time'][counter]<personal_best and df['Count'][counter]==0:
                personal_best = df['Average Time'][counter]
        if entry >= 5:
            if df['S_D'][counter]<personal_best_s_d:
                personal_best_s_d = df['S_D'][counter]
                personal_best_s_d_avg = df['Average Time'][counter]
        counter += 1
    print('Your P.B. average time (min 5 rounds; no mistakes) is ' + str(personal_best) + ' seconds.')
    print('Your P.B standard deviation (min 5 rounds) is ' + str(personal_best_s_d) + ' seconds (' +
          str(personal_best_s_d_avg) + ' avg sec per round).')

    best_round = 100
    df_sg = pd.read_csv(summary_file)
    for entry in df_sg['Time']:
        if entry<best_round:
            best_round = entry
    print('Your P.B single round is ' + str(best_round) + ' seconds.\n')

summary_file_check()
instruction()
game_time()
performance_metrics()
