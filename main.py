# This is a sample Python script.
import nltk
from random import choice
import pandas as pd
from Levenshtein import ratio
import numpy as np


print("Enter the input line: \n")

sentence = input()

# lemantizing the input
word_list = nltk.word_tokenize(sentence.lower())

# i = []
# for index, row in df.iterrows():
#     i.append(row['Questions '])
#
# one_word = []
# for j in i:
#     j_list = nltk.word_tokenize(j.lower())
#     one_word.append(j_list[0])
#
# df['First Word'] = one_word


# this function is used to get printable results





# X = df.drop(columns=['Questions ', 'Answers'])
#
#
#
# y = df['Answers'].astype(str)
#
# le = preprocessing.LabelEncoder()
# X = le.fit_transform(X.astype(str))
#
# X = X.reshape(-1, 1)
#
# model = DecisionTreeClassifier()
# model.fit(X,y)




# list of Yes/No verbs
yn_list = ['Do','Does','Did','do','does','did','Am','Are','Is','Was','Were','am','are','is','was','were',
           'Have','Has','Had','have','has','had','Will','Would','Shall','Should','Can','Could','May',
           'Might','will','would','shall','should','can','could','may','might']

# list of negative Yes/No verbs
yn_negative_list = ["Don't","Doesn't","Didn't","don't","doesn't","didn't","Aren't","Isn't","aren't","isn't",
                    "Wasn't","Weren't","wasn't","weren't","Haven't","Hasn't","Hadn't","haven't","hasn't",
                    "hadn't","Won't","Wouldn't","won't","wouldn't","Shan't","shan't","Shouldn't","Can't",
                    "Couldn't","shouldn't","can't","couldn't","may not","May not","Mightn't","mightn't"]

wh_list = ['who','where','what','when','why','whom','which','whose','how']

# combining two lists
test_data = []
assertion = sentence.endswith('.')

if assertion == True:
    test_data.append(sentence)
    df = pd.read_csv('lematizer2.csv')


    def getResults(questions, fn):
        def getResult(q):
            answer, score, prediction = fn(q)
            return [q, prediction, answer, score]

        return pd.DataFrame(list(map(getResult, questions)), columns=["Q", "Prediction", "A", "Score"])


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


    df1 = getResults(test_data, getApproximateAnswer2)
    print(df1.loc[df1.index[0], 'A'])




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


for j in wh_list:
    if(j == first_word):
        test_data.append(sentence)

        df = pd.read_csv('lemantizer.csv')
        def getResults(questions, fn):
            def getResult(q):
                answer, score, prediction = fn(q)
                return [q, prediction, answer, score]

            return pd.DataFrame(list(map(getResult, questions)), columns=["Q", "Prediction", "A", "Score"])


        def getApproximateAnswer2(q):
            max_score = 0
            answer = ""
            prediction = ""
            for idx, row in df.iterrows():
                score = ratio(row["Questions "], q)
                if score >= 0.9:  # I'm sure, stop here
                    return row["Answers"], score, row["Questions "]
                elif score > max_score:  # I'm unsure, continue
                    max_score = score
                    answer = row["Answers"]
                    prediction = row["Questions "]
            if max_score > 0.3:  # threshold is lowered
                return answer, max_score, prediction
            return "Sorry, I didn't get you.", max_score, prediction
        df1 = getResults(test_data, getApproximateAnswer2)
        print(df1.loc[df1.index[0], 'A'])





        # j_array = []
        # j_array.append(j)
        #
        # j_array1 = np.array(j_array)
        # # print(j_array1.shape)
        #
        # j_array2 = le.fit_transform(j_array1)
        #
        #
        # predictions = model.predict([[j_array2[0]]])
        # print(predictions[0])










