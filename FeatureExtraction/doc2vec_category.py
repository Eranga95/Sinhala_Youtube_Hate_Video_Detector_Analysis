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
from tqdm import tqdm
tqdm.pandas(desc="progress-bar")
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import multiprocessing
from sklearn import utils
import string

dataset = defaultdict(list)

# create a dataframe to store dataset
df = pd.DataFrame(columns=['comment', 'replies', 'otherMetadata', 'likeDislikeRatio', 'category'])


i =0
for x in range(603):
    with open("../output/"+str(x)+".json", encoding='utf-8') as f:
        data = json.load(f)
    commentsText = ""
    replyText=""
    replies = defaultdict(list)
    category = data[0]['category']
    otherMetaData = data[0]["title"] + data[0]["description"]  # + item["tags"]
    likes = int(data[0]["likeCount"])
    dislikes = int(data[0]["dislikeCount"])
    likeDislikeRatio = str(float(likes/dislikes))
    for item in data[0]["comments"]:
        commentsText += item["comment"]
        replyText = ""
        if 'replies' in item.keys():
            for reply in item['replies']:
                replyText += reply['replyComment']
    df.loc[i] = [commentsText] + [replyText] + [otherMetaData] + [likeDislikeRatio] + [category]
    i += 1
# class variable binerization

# plt.figure(figsize=(10, 4))
# df['category'].value_counts().plot(kind='bar')
# plt.show()



df['data'] = df['comment'] + df['otherMetadata']


def labelize_data(comments, label):
    result = []
    prefix = label
    for j, t in zip(comments.index, comments):
        result.append(LabeledSentence(t.split(), [prefix + '_%s' % j]))
    return result

all_comments = df['data']
all_comments_wv = labelize_data(all_comments, 'all')

print(all_comments_wv)

cores = multiprocessing.cpu_count()
model_ug_dbow = Doc2Vec(dm=0, size=100, negative=5, min_count=2, workers=cores, alpha=0.065, min_alpha=0.065)
model_ug_dbow.build_vocab([x for x in tqdm(all_comments_wv)])

for epoch in range(30):
    model_ug_dbow.train(utils.shuffle([x for x in tqdm(all_comments_wv)]), total_examples=len(all_comments_wv), epochs=1)
    model_ug_dbow.alpha -= 0.002
    model_ug_dbow.min_alpha = model_ug_dbow.alpha


def get_vectors(model, corpus, size):
    vecs = np.zeros((len(corpus), size))
    n = 0
    for i in corpus.index:
        prefix = 'all_' + str(i)
        vecs[n] = model.docvecs[prefix]
        n += 1
    return vecs

# Train split
x_train, x_test, y_train, y_test = train_test_split(df['comment'], df['category'], test_size=0.3)



train_vecs_dbow = get_vectors(model_ug_dbow, x_train, 100)
validation_vecs_dbow = get_vectors(model_ug_dbow, x_test, 100)

# Logistic Regression

clf = LogisticRegression()
clf.fit(train_vecs_dbow, y_train)
accuracy = clf.score(validation_vecs_dbow, y_test)
print("Doc2Vec Accuracy "+str(accuracy))







