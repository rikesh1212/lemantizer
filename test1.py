import pandas as pd
import json
import nltk
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from Levenshtein import ratio


df = pd.read_csv('lemantizer.csv')

def getResults(questions, fn):
    def getResult(q):
        answer, score, prediction = fn(q)
        return [q, prediction, answer, score]
    return pd.DataFrame(list(map(getResult, questions)), columns=["Q", "Prediction", "A", "Score"])

test_data = []

sentence = "What is your father doing?"

test_data.append(sentence)

def getApproximateAnswer(q):
    max_score = 0
    answer = ""
    prediction = ""
    for idx, row in df.iterrows():
        score = ratio(row["Questions "], q)
        if score >= 0.9: # I'm sure, stop here
            return row["Answers"], score, row["Questions "]
        elif score > max_score: # I'm unsure, continue
            max_score = score
            answer = row["Answers"]
            prediction = row["Questions "]
    if max_score > 0.8:
        return answer, max_score, prediction
    return "Sorry, I didn't get you.", max_score, prediction
df1 = getResults(test_data, getApproximateAnswer)
print(df1.loc[df1.index[0],'A'])
