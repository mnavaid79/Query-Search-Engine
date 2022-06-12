import flask
from flask import Flask
from flask import redirect, url_for, request
from flask import render_template
import os
import pickle
import math

def queryVector(inv_index, a):
    query = input("Enter query: ")
    if query not in inv_index:
        return 'Error, given query not found. Please try again!'
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

# User specified directory, Import index from the pickle file
with open('D:/College/College Courses/CS 429/Project/index.pkl', 'rb') as f:
    inv_index = pickle.load(f)

with open('D:/College/College Courses/CS 429/Project/corpus.pkl', 'rb') as ft:
    corpus = pickle.load(ft)
    

qVector = queryVector(inv_index, corpus)

if type(qVector) == type('abc'):
    print('Error, given query not found. Please try again!')

if type(qVector) != type('abc'):
    global cs 
    cs = cosineScore(qVector, inv_index, corpus)
    cs.sort(key = takeSecond, reverse=True)

global k
k = input('Set top K limit (integer number): ')

app = Flask(__name__, template_folder='D:/College/College Courses/CS 429/Project')

@app.route('/')

def user():
    comments = {}
    for i in range(len(cs)):
        if i != k:
            comments[i] = str(cs[i][0])
        if i == k:
            break
    return render_template('format.html', comments =  comments) 

if __name__ == '__main__':
  
    app.run()

