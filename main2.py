from ast import literal_eval
from Levenshtein import ratio
import pandas as pd
import numpy as np
import nltk
from random import choice


print("Enter the input line: \n")

sentence = input()

# lemantizing the input
word_list = nltk.word_tokenize(sentence.lower())
all_data = []


with open("QA_VIDEO_Games.json", "r") as f_in:
    for line in f_in:
        all_data.append(literal_eval(line))

df = pd.DataFrame(all_data)
df = df.explode("questions").reset_index(drop=True)
df = (
    pd.concat(
        [df, pd.json_normalize(df.pop("questions"))],
        axis=1,
    )
    .explode("answers")
    .reset_index(drop=True)
)
df = pd.concat(
    [df, pd.json_normalize(df.pop("answers"))],
    axis=1,
)

yn_list = ['Do','Does','Did','do','does','did','Am','Are','Is','Was','Were','am','are','is','was','were',
           'Have','Has','Had','have','has','had','Will','Would','Shall','Should','Can','Could','May',
           'Might','will','would','shall','should','can','could','may','might']

# list of negative Yes/No verbs
yn_negative_list = ["Don't","Doesn't","Didn't","don't","doesn't","didn't","Aren't","Isn't","aren't","isn't",
                    "Wasn't","Weren't","wasn't","weren't","Haven't","Hasn't","Hadn't","haven't","hasn't",
                    "hadn't","Won't","Wouldn't","won't","wouldn't","Shan't","shan't","Shouldn't","Can't",
                    "Couldn't","shouldn't","can't","couldn't","may not","May not","Mightn't","mightn't"]

wh_list = ['who','where','what','when','why','whom','which','whose','how','Who','Where','What','When','Why','Whom',
          'Which','Whose','How']

for x in yn_negative_list:
    yn_list.append(x)

# taking the first word of the sentence
first_word = word_list[0]

# random Yes/No Choices
answer = choice(['Yes', 'No'])

# checking if the input is a Yes/No Question or Not
for i in yn_list:
    if(i == first_word):
        print(answer)


df1 = df[df["questionText"].str.split(n=1).str[0].isin(yn_list)]

df2 = df[df["questionText"].str.lower().str.split(n=1).str[0].isin(wh_list)]

df3 = df[df["questionText"].str.endswith(".")]


test_data = []

for j in wh_list:
    if(j == first_word):
        test_data.append(sentence)

        def getResults(questions, fn):
            def getResult(q):
                answer, score, prediction = fn(q)
                return [q, prediction, answer, score]
            return pd.DataFrame(list(map(getResult, questions)), columns=["Q", "Prediction", "A", "Score"])



        # sentence = []

        # test_data.append(sentence)

        def getApproximateAnswer(q):
            max_score = 0
            answer = ""
            prediction = ""
            for idx, row in df2.iterrows():
                score = ratio(row["questionText"], q)
                if score >= 0.9: # I'm sure, stop here
                    return row["answerText"], score, row["questionText"]
                elif score > max_score: # I'm unsure, continue
                    max_score = score
                    answer = row["answerText"]
                    prediction = row["questionText"]
            if max_score > 0.3:
                return answer, max_score, prediction
            return "Sorry, I didn't get you.", max_score, prediction

        wh_df = getResults(test_data, getApproximateAnswer)
        print(wh_df.loc[wh_df.index[0], 'A'])

assertion = sentence.endswith('.')
if assertion == True:
    test_data.append(sentence)
    df = pd.read_csv('lematizer2.csv')
    def getResults(questions, fn):
        def getResult(q):
            answer, score, prediction = fn(q)
            return [q, prediction, answer, score]
        return pd.DataFrame(list(map(getResult, questions)), columns=["Q", "Prediction", "A", "Score"])



        # sentence = []

        # test_data.append(sentence)


    def getApproximateAnswer2(q):
        max_score = 0
        answer = ""
        prediction = ""
        for idx, row in df.iterrows():
            score = ratio(row["Questions"], q)
            if score >= 0.9:  # I'm sure, stop here
                return row["Answers"], score, row["Questions"]
            elif score > max_score:  # I'm unsure, continue
                max_score = score
                answer = row["Answers"]
                prediction = row["Questions"]
        if max_score > 0.3:  # threshold is lowered
            return answer, max_score, prediction
        return "Sorry, I didn't get you.", max_score, prediction


    as_df = getResults(test_data, getApproximateAnswer2)
    print(as_df.loc[as_df.index[0], 'A'])

