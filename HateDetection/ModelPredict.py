from sklearn.externals import joblib
import nltk
import random
import json
from pandas.io.json import json_normalize
from pprint import pprint
from collections import defaultdict
import pandas as pd
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import  MultinomialNB
from nltk.tokenize import sent_tokenize,word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from time import time
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import string
import random
from sklearn.ensemble import VotingClassifier
import pickle


# load pickle files
logisticRegression = joblib.load("feature_mapper_Lr.pkl")
mapper = joblib.load("vectorizer_mapper.pkl")




df = pd.DataFrame(columns=['comment', 'replies', 'otherMetadata', 'likeDislikeRatio'])


with open("../output/602.json", encoding='utf-8') as f:
    data = json.load(f)
    commentsText = ""
    replyText = ""
    replies = defaultdict(list)
# store sentiment of the data
    sentiment = data[0]['sentiment']
    otherMetaData = data[0]["title"] + data[0]["description"]  # + item["tags"]
    likes = int(data[0]["likeCount"])
    dislikes = int(data[0]["dislikeCount"])
    likeDislikeRatio = str(float(likes/dislikes))
    for item in data[0]["comments"]:
        commentsText += item["comment"]
        if 'replies' in item.keys():
            for reply in item['replies']:
                replyText += reply['replyComment']
    df.loc[0] = [commentsText] + [replyText] + [otherMetaData] + [likeDislikeRatio]



tranformed = mapper.transform(df)
print(tranformed[0][2])
prediction = logisticRegression.predict(tranformed)
print(prediction)

clf = logisticRegression
z = np.dot(clf.coef_, tranformed.T) + clf.intercept_
hypo = 1/(1+np.exp(-z))
print("Level of hate =" + str(hypo))

# print(len(classification_df))
# print(clf.coef_[0])
# print(clf.intercept_)
#
# print("weights")
# print("bias, comment, otherMeta , Like/dislike")
# print(np.hstack((clf.intercept_[:, None], logreg.py.coef_)))
#
# i = 601
# z = clf.intercept_ + float(classification_df['comment_sentiment'].iloc[i]) * float(clf.coef_[0][0]) + float(classification_df['otherMetadata_sentiment'].iloc[i]) * float(clf.coef_[0][1]) + float(classification_df['likeDislikeRatio'].iloc[i]) * float(clf.coef_[0][2])
# hypo = 1/(1+np.exp(-z))
# print("Level of hate =" + str(hypo))


# coefficients = pd.concat([pd.DataFrame(df.columns),pd.DataFrame(np.transpose(logisticRegression.coef_))], axis = 1)
# print(coefficients)

# prediction_df = pd.DataFrame(columns=['comment_sentiment', 'reply_sentiment','otherMetadata_sentiment', 'likeDislikeRatio'])
# prediction_df = prediction_df.astype({"comment_sentiment": bool, "reply_sentiment": bool, "otherMetadata_sentiment": bool, "likeDislikeRatio": float})
#
# # comment automatic annotation
# sentiment_score_comment = [positive_score_comment[w] for w in df['comment'].iloc[0].split() if w in positive_score_comment.index]
#
# if len(sentiment_score_comment) > 0:
#     prob_score_comment = np.mean(sentiment_score_comment)
# else:
#     prob_score_comment = np.random.random()
#
# prediction_comment = 1 if prob_score_comment > 0.56 else 0
#
# # reply automatic annotation
#
# sentiment_score_replies = [positive_score_comment[w] for w in df['replies'].iloc[0].split() if w in positive_score_comment.index]
# if len(sentiment_score_replies) > 0:
#     prob_score_replies = np.mean(sentiment_score_comment)
# else:
#     prob_score_replies = np.random.random()
#
# prediction_replies = 1 if prob_score_replies > 0.56 else 0
#
# # other meta data automatic annotation
# sentiment_score_other = [positive_score_comment[w] for w in df['replies'].iloc[0].split() if w in positive_score_comment.index]
# if len(sentiment_score_other) > 0:
#     prob_score_other = np.mean(sentiment_score_comment)
# else:
#     prob_score_other = np.random.random()
#
# prediction_other = 1 if prob_score_other > 0.56 else 0
# likeDislikeRatio = df['likeDislikeRatio'].iloc[0]
# prediction_df.loc[0] = [prediction_comment] + [prediction_replies] + [prediction_other] + [likeDislikeRatio]

