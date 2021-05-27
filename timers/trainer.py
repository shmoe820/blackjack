import os
import csv
import random
import datetime
import pandas as pd

today_date = datetime.datetime.now().strftime("%Y" + '.' + "%m" + '.' + "%d")
summary_file= 'trainer.csv'
exercise_times = []
mistakes_made = []

def summary_file_check():
    # Check directory for file named single_deck.csv and create file if it does not exist.
    if not os.path.isfile(summary_file):
            header = ["Date", "Time", "xx out of 100"]
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
    instructions = 'This game is called BJ Trainer and it will be used in conjunction with Microsoft Excel file\n' \
               "'trainer.csv'.  The object of the game is to properly execute 100 BJ hands as accurately and\n" \
               "as quickly as possible.  As the user, you will start the timer using the 'enter' key when \n" \
               "prompted, and hit it again once you have completed the deck.  Then you will enter a number\n"\
               "between 0 and 100 for accuracy. Time penalty per mistake is 5 seconds."
    print('\n*****     *****     *****     *****\n')
    print(instructions)
def game_time():
    while True:
        start_game = input("\nPress 'enter' when ready to begin the BJ Trainer exercise. Press 'q' to quit.")
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
                correct_hands = input('Enter how many hands out of 100 you played correctly: ')
                mistakes_made.append(correct_hands)

                time_integer = round(time_integer + 5*(100-int(correct_hands)),2)
                exercise_times.append(time_integer)
                print('Time: %s seconds. Mistakes: %s.' % (time_integer, (100-int(correct_hands))))

                with open(summary_file, 'a') as file:
                    file.writelines(today_date + ', ' + str(time_integer) +'{}'.format(', ') + correct_hands + '\n')
                break
            except ValueError:
                print('You did not enter a number.')
                continue

def performance_metrics():
    summary_file_average = 'trainer_average.csv'
    # Check directory for file named basic_strategy.csv and create file if it does not exist.
    if not os.path.isfile(summary_file_average):
            header = ["Date", "No. of 100 Hand Sets", "Average Time", "Mistakes"]
            # open the file in the write mode
            f = open(summary_file_average, 'w')
            # create the csv writers
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
        total_mistakes += (100 - int(mistakes))

    try:
        avg_time = round((total_time)/len(exercise_times),2)
        print(
            "\n\nYou completed %s '100 hand sets' with %s total mistake(s)."
            "\nAverage time = %s seconds per 100 hands.\n " % (len(exercise_times), total_mistakes, avg_time))
    except ZeroDivisionError:
        print("You played 0 games.\n")
        exit()

    with open(summary_file_average, 'a') as file:
        file.writelines(today_date + ', ' + str(len(exercise_times)) + ', ' + str(avg_time) + ', ' + str(total_mistakes)+ '\n')

    personal_best = 1000
    counter = 0
    df = pd.read_csv(summary_file_average)

    for entry in df['No. of 100 Hand Sets']:
        if entry >= 1:
            if df['Average Time'][counter]<personal_best and df['Mistakes'][counter]==0:
                personal_best = df['Average Time'][counter]
        counter += 1
    print('Your personal best average time (min. 1 rounds, 0 mistakes) is ' + str(personal_best) + ' seconds.')

    personal_best_perfect_rounds = 0
    count_pb = 0
    for entry in df['No. of 100 Hand Sets']:
        if entry >= 1 and df['Mistakes'][count_pb]==0:
            total_hands = int(entry) * 100
            if total_hands > personal_best_perfect_rounds:
                personal_best_perfect_rounds = total_hands
                average_decision = df['Average Time'][count_pb] / 100
        count_pb += 1
    print('Your personal best flawless rounds is ' + str(personal_best_perfect_rounds) + ' rounds.  ', end="")
    print('The average time per hand is ' + str(average_decision) + ' seconds.')

summary_file_check()
instruction()
game_time()
performance_metrics()
