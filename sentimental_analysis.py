from flask import Flask, render_template,request
from textblob import TextBlob
from imdb import IMDb
ia = IMDb()
import nltk
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
app = Flask(__name__)

@app.route('/')
def student():
    return render_template('front.html')

@app.route('/result',methods = ['POST', 'GET'])
def hello_world():
    resultdict={}
    pos = 0
    neg = 0
    avg = 0
    result = request.form['movie']
    sid = SentimentIntensityAnalyzer()
    search = ia.search_movie(result)
    id = search[0].movieID
    a = ia.get_movie(id, ['reviews'])
    b = a['reviews']
    for i in range(len(b)):
        string = b[i]['content']
        scores = sid.polarity_scores(string)
        for key in sorted(scores):
            if key=="compound":
                resultdict[string] = round(scores[key],2)
                if scores[key] > 0:
                    if scores[key] > 0 and scores[key] < 0.5:
                        avg = avg + 1
                    else:
                        pos = pos + 1
                else:
                    neg = neg + 1

    return render_template("end.html", pos=pos,neg=neg,avg=avg,resultans=resultdict)

###################################################
#####for feteching the flimography of the actor 
from imdb import IMDb
import json
ia = IMDb()
resultdict={}
count=1
result=input("enter the actor name:")
people = ia.search_person(result)
actorid=people[0].getID()
actor = ia.get_person(actorid)
for job in actor['filmography'].keys():
    for movie in actor['filmography'][job]:
        print(movie['title'])
        resultdict[count]=movie['title']
        count=count+1
print(resultdict)
print(json.dumps(resultdict))#####

if __name__ == '__main__':
    app.run()
