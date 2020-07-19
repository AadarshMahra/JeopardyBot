import discord
import pandas as pd
from utils.question import QuestionPanel
import random


def fetch_random_panel():
    while True:  # only creates QP object when value isn't Null
        n = int(random.random() * 216930)
        df = pd.read_csv('data/jeopardy_data.csv')
        row = df.iloc[n, 3:7].tolist()  # fetches from random index
        print(row)
        temp = row[1]  # hold value here
        if temp != 'None':
            qp = QuestionPanel(row[0], row[1], row[2], row[3])
            break
    return qp


def check_answer(attempt, q_panel):
    if attempt == q_panel.get_answer():
        return True
    else:
        return False


def is_question_valid(question_str):
    return question_str != '[video clue]'

# checks if an attempt is valid given that attempt and the correct answer's panel
# returns True if attempt is valid


def is_valid(attempt, answer):
    possible_answers = set()
    attempt = attempt.lower()  # lowercase all attempts
    # takes care of case sensitivity(in general)
    answer = answer.lower()
    possible_answers.add(answer)

    # get rid of parentheses
    possible_answers.add(answer.strip(' ()'))
    # get rid of surrounding apostrophes
    possible_answers.add(answer.strip('\''))
    # print(possible_answers)
    # what else is next?
    return attempt in possible_answers
