from tinydb import TinyDB, Query
from datetime import date

def main(score):
    set_score(score)
    sort_db()

def set_score(score):
    scoredb = TinyDB("scores.json")

    name = "Jane Doe"
    score = score
    today = str(date.today())
    scoredb.insert({'name': name, 'score': score, 'date': today})

def sort_db():
    scoredb = TinyDB("scores.json")

    i = {'name': 'none', 'score': '0', 'date': '2023-03-25'}
    first = {'name': 'none', 'score': '0', 'date': '2023-03-25'}
    second = {'name': 'none', 'score': '0', 'date': '2023-03-25'}
    third = {'name': 'none', 'score': '0', 'date': '2023-03-25'}

    for i in scoredb:
        #i = item
        if int(i['score']) >= int(first['score']):
            third = second
            second = first
            first = i
        elif int(i['score']) >= int(second['score']):
            third = second
            second = i
        elif int(i['score']) >= int(third['score']):
            third = i
