from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import pandas as pd
import random
import time
import threading as th


def showQuestions(q_no, q_name):
    # A function to print the snippets in the folder.
    question_title = "Question " + str(q_no)
    plt.title(question_title)
    plt.xlabel("GOOD")
    plt.ylabel("LUCK")

    question_name = q_name + '.jpg'
    image = mpimg.imread(question_name)
    plt.imshow(image)
    plt.show()
    question_title = "Question "


def checkSolution(question_list, answers, d_frame):
    score = 0
    corr = 0
    skipped = 0
    incorrect = 0

    correct_answers = []

    print('YOUR RESULTS: ')
    for x in range(1, len(answers)+1):
        q_no = question_list[x - 1]
        correct = d_frame.iloc[q_no-1, 2]
        selected = answers[x-1]
        correct_answers.append(correct)

        if selected == correct:
            corr += 1
            comp_ques.append(q_no)
            score += 4

        elif selected == 'x':
            skipped += 1
            score += 1

        elif selected != correct:
            incorrect += 1
            continue

    print(' ')
    print('MAXIMUM SCORE: ' + str(4*len(answers)))
    print('TOTAL SCORE: ' + str(score))
    print(' ')
    print('CORRECT: ' + str(corr))
    print('INCORRECT: ' + str(incorrect))
    print('SKIPPED: ' + str(skipped))

    return correct_answers


def takeTest(question_list, d_frame, r):

    # Creating a 30 member array
    answers = []
    for x in range(r):
        answers.append('x')

    process_on = True
    count = 1

    # Looping through a test session
    while process_on:
        q_no = question_list[count-1]
        q_name = d_frame.iloc[q_no-1, 1]
        print('Enter the choice for Question ' + str(count)+':')
        print('\t The current answer is : ' + answers[count-1])
        print('\t 0. Enter the answer')
        print('\t 1. Enter 1 to previous')
        print('\t 2. Enter 2 to next')
        print('\t 3. Enter 3 to jump to a question')
        print('\t 4. Enter 4 to submit')
        showQuestions(count, q_name)

        # Input Section
        chc = input()
        if chc == 'a' or chc == 'b' or chc == 'c' or chc == 'd':
            if count == r:
                answers[count - 1] = chc
                count -= 1

            else:
                answers[count-1] = chc
                count += 1

        elif chc == '1':
            if count == 1:
                print('Hey! This is the first question!')
                print(' ')
                continue
            else:
                count -= 1
                continue

        elif chc == '2':
            if count == r:
                print('Hey! This is the last question!')
                print(' ')
                continue
            else:
                count += 1
                continue

        elif chc == '3':
            print('Enter the question number from (1, '+str(r)+'):')
            q_choice = int(input())
            count = q_choice
            continue

        elif chc == '4':
            process_on = False

    correct_ans = checkSolution(question_list, answers, d_frame)

    # Print questions for reference
    print(' ')
    print('Question No. \t Question List \t Selected options \t Correct options \t Status \t Topic ')
    for x in range(r):
        q_no = question_list[x]
        q_top = d_frame.iloc[q_no - 1, 3]
        status = 'Incorrect'

        if answers[x] == correct_ans[x]:
            status = 'Correct'
        elif answers[x] == 'x':
            status = 'Skipped'

        line = str(x+1)+'\t \t'+str(question_list[x])+'\t \t'\
               + str(answers[x])+'\t \t'+str(correct_ans[x])\
               + '\t \t'+status + '\t \t'+str(q_top)
        print(line)

    print_questions(question_list, d_frame)


def get_question_list(n, r):
    questions = []
    repeat = False
    while len(questions) <= (r-1):
        q_no = random.choice(range(1, n+1))
        # Check for repeats
        for x in questions:
            if q_no == x:
                repeat = True
        if repeat == False:
            questions.append(q_no)
        repeat = False

    return questions


def get_topic_question_list(d_frame, topic_code, n, r):
    questions = []
    repeat = False
    while len(questions) <= (r-1):
        q_no = random.choice(range(1, n+1))
        # Check for repeats
        for x in questions:
            if q_no == x:
                repeat = True
        if repeat == False and topic_code == d_frame.iloc[q_no-1, 3]:
            questions.append(q_no)
        repeat = False

    return questions


def get_weighted_question_list(d_frame, n, wts):
    # print('start')
    questions = []
    repeat = False
    i = 0  # i in [0,11]
    j = 0

    # Outer loop to get all questions
    while i < len(wts):
        # Inner loop to reset the topics
        topic_code = wts[i][0]
        r = wts[i][1]
        j += r
        # print(r)
        # print(topic_code)

        while len(questions) < j:
            q_no = random.choice(range(1, n+1))
            # Check for repeats
            for x in questions:
                if q_no == x:
                    repeat = True
            if repeat == False and topic_code == d_frame.iloc[q_no-1, 3]:
                questions.append(q_no)

            repeat = False
        i += 1
    # print(questions)
    # print('end')
    random.shuffle(questions)
    return questions


def print_questions(question_list, d_frame):
    for x in range(len(question_list)):
        q_no = question_list[x]
        q_name = d_frame.iloc[q_no-1, 1]
        showQuestions(x+1, q_name)


def time_end():
    print(' ')
    for x in range(5):
        print('TIME IS UP!')
        time.sleep(2)


# Main Code

# Creating the data-frame for the csv file with problems
df = pd.read_csv('ProblemDetails-PCA.csv')

# Changing the Image Size
plt.rcParams["figure.figsize"] = [10.0, 5.0]
plt.rcParams["figure.autolayout"] = True

# Getting the number of records
n_val = df['Sl. No.'].count()
# Default number of questions to be generated
r_val = 30

# Program Begins
print('TAKE A MOCK TEST')
print(' ')

# Enter Topic Code
print('Enter Topic Code: ')
print(' ')
print('ALL	All Topics 244')
print('AL	Algebra	51')
print('CA	Calculus	38')
print('CG	Co-ordinate Geometry	17')
print('COM	Combinatorics	17')
print('DE	Differential Equations	13')
print('GRP	Group Theory	9')
print('LA	Linear Algebra	31')
print('MVC	Multivariable Calculus	11')
print('NT	Number Theory	16')
print('PRB	Probability	16')
print('RA	Real Analysis	20')
print('TRI	Trigonometry	5')
top = input()
print(' ')

# Inputs for hours, minutes, seconds on timer
h = int(input("Enter the time in hours: "))
m = int(input("Enter the time in minutes: "))
s = int(input("Enter the time in seconds: "))
print(' ')

# Calculate the total number of seconds
total_seconds = h * 3600 + m * 60 + s

# Getting the list of questions for the test
if top == 'ALL':
    print('Enter w for weighted, and r for random')
    wt = input()
    if wt == 'r':
        q_list = get_question_list(n_val, r_val)

    elif wt == 'w':
        weights = [['AL', 6], ['CA', 5], ['CG', 2],
                   ['COM', 2], ['DE', 2], ['GRP', 1],
                   ['LA', 4], ['MVC', 1], ['NT', 2],
                   ['PRB', 2], ['RA', 2], ['TRI', 1]]
        q_list = get_weighted_question_list(df, n_val, weights)
else:
    print('Enter no of questions: ')
    r_val = int(input())
    q_list = get_topic_question_list(df, top, n_val, r_val)


S = th.Timer(total_seconds, time_end)
S.start()

takeTest(q_list, df, r_val)

