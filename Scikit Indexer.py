import codecs
import os
import pandas as pd
from pandas import read_html
import html5lib
import re
import math
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import pickle


def tfIDF_Index(a):
    inv_idx = {}
    sym = [',', "'", '.']
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] not in sym:
                if a[i][j].lower() not in inv_idx:
                    inv_idx[a[i][j].lower()] = [[i]]
                if a[i][j].lower() in inv_idx:
                    st = a[i][j].lower()
                    if i > inv_idx[st][len(inv_idx[st])-1][0]:
                        inv_idx[st].append([i])
    for i in inv_idx:
        for j in range(len(inv_idx[i])):
            tf = 0
            for k in a[inv_idx[i][j][0]]:
                if i == k.lower():
                    tf += 1
            tf = tf/len(a[inv_idx[i][j][0]])
            inv_idx[i][j].append(tf*math.log(len(a)/len(inv_idx[i])))
            
    return inv_idx

def queryVector(inv_index, a):
    query = input("Enter query: ")
    query = query.split()    
    qVector = {}
    for i in query:
        if i.lower() not in inv_index:
            qVector[i.lower()] = []
        if i.lower() in inv_index:
            qVector[i.lower()] = [math.log(len(a)/len(inv_index[i.lower()]))]
    return qVector

def cosineScore(qVector, inv_index, a):
    scores = {}
    for i in qVector:
        wtq = qVector[i][0]
        postlist = inv_index[i]
        for j in postlist:
            if j[0] not in scores:
                scores[j[0]] = 0
            wftd = j[1]
            scores[j[0]] += wtq*wftd
    for i in scores:
        scores[i] = scores[i]/len(a[i])
        Score = []
    for i in scores:
        Score.append((i,scores[i]))
    return sorted(Score)

def takeSecond(elem):
    return elem[1]

# User specified directory, set as you wish
path  = 'D:/College/College Courses/CS 429/Project/full'

# Change the directory
os.chdir(path)
      
c = []
corpus = []

# iterate through all files
for file in os.listdir():
    file_path = f'{path}/{file}'
    c.append(str(codecs.open(file_path, 'r').read()))
    
for i in range(len(c)):
    corpus.append(re.sub("[^a-zA-Z0-9]+", " ",c[i]))

clist = []
for i in range(len(corpus)):
    clist.append([])
    temp = ''
    for j in corpus[i]:
        if j != ' ':
            temp = temp+j
        if j == ' ':
            clist[i].append(temp)
            temp = ''
            

inv_index = tfIDF_Index(clist)


# Create the Document Term Matrix
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer = CountVectorizer()
sparse_matrix = (count_vectorizer.fit_transform(corpus))

# Turn into Data Frame
doc_term_matrix = sparse_matrix.todense()
df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names())


# df.head(11) Run this to see data frame head


# Cosine Similarity

dj=pd.DataFrame(cosine_similarity(df, dense_output=True))
# dj.head(11) Run this to see data frame head


t=[]

# Part 01:
for j,k in enumerate(dj.values):
    for n in range(len(k)):
        t.append([j,n,k[n]])

# Part 02:
qq=[]
for i in range(len(t)):
    if t[i][0]==t[i][1]:
        qq.append([t[i][0],t[i][1],0])
    else:
        qq.append(t[i])


u=defaultdict(list)

for i in range(len(qq)):
    u[qq[i][0]].append(qq[i][2])
    
updated_df=pd.DataFrame(u)

# update_df.head(11) Run this to see data frame head


# User specified directory, set as you wish
filename = "D:/College/College Courses/CS 429/Project/index.pkl"
os.makedirs(os.path.dirname(filename), exist_ok=True)

# This will download the index as a pickle file in the '.../Project' directory
with open('D:/College/College Courses/CS 429/Project/index.pkl', 'wb') as f:
    pickle.dump(inv_index, f)
    
with open('D:/College/College Courses/CS 429/Project/corpus.pkl', 'wb') as ft:
    pickle.dump(clist, ft)

