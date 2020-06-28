import discord
import pandas as pd
from utils.question import QuestionPanel


def fetch_random_panel(n):
    df = pd.read_csv('data/jeopardy_data.csv')
    row = df.iloc[n, 3:7].tolist()  # fetches from random index
    print(row)
    qp = QuestionPanel(row[0], row[1], row[2], row[3])
    return qp


def check_answer(attempt, q_panel):
    if attempt == q_panel.get_answer():
        return True
    else:
        return False


def is_question_valid(question_str):
    return question_str != '[video clue]'
