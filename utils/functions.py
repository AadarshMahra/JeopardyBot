import discord
import pandas as pd
from utils.question import QuestionPanel
import random


def fetch_random_panel():
    while True:
        n = int(random.random() * 216930)
        df = pd.read_csv('data/jeopardy_data.csv')
        row = df.iloc[n, 3:7].tolist()  # fetches from random index
        print(row)
        if row[1] != 'None' and "href" not in row[2]:  # value can't be Null and question can't have image link
            qp = QuestionPanel(row[0], row[1], row[2], row[3])
            break
    return qp


def check_answer(attempt, q_panel):
    if attempt == q_panel.get_answer():
        return True
    else:
        return False


# checks if an attempt is valid given that attempt and the correct answer's panel
# returns True if attempt is valid


def is_valid(attempt, panel):
    possible_answers = set()
    answer = panel.get_answer();
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
