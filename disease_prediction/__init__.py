import os
import pandas as pd
import numpy as np
import json
from json import JSONEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

r = RandomForestClassifier()

# Dataset
train = pd.read_csv('disease_prediction/dataset/training.csv')
data_symptoms_list = train.columns.tolist()

#Train Model
def train():
    train = pd.read_csv('disease_prediction/dataset/training.csv')
    x = train.drop('prognosis', axis=1)
    y = train['prognosis']
    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)
    r.fit(x_train, y_train)
    print(x_test)
    predict = r.predict(x_test)
    return r.score(x_test, predict)

def test():
    test = pd.read_csv('disease_prediction/dataset/testing.csv')
    test.drop('prognosis', axis=1, inplace=True)
    predict = r.predict(test)
    return r.score(test, predict)

def predict(sympotoms_list):
    x_predict_dict = {}
    for i in range(0,len(data_symptoms_list)):
        if data_symptoms_list[i] in sympotoms_list:
            x_predict_dict[data_symptoms_list[i]] = [1]
        else:
            x_predict_dict[data_symptoms_list[i]] = [0]
    print(x_predict_dict)
    predict_df = pd.DataFrame.from_dict(x_predict_dict)
    predict_df = predict_df.drop('prognosis', axis=1)
    return r.predict(predict_df).tolist()

