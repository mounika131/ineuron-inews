from flask import Flask, render_template
from newsapi import NewsApiClient
import pandas as pd
from IPython.core.display import HTML

 

app = Flask(__name__)
 
 

@app.route('/')

def index():
    return render_template('bbc.html')
def bbc():
    newsapi = NewsApiClient(api_key="9ae12a7cbf8f4fb985379a7c61dc12b2")
    topheadlines = newsapi.get_top_headlines(sources="bbc-news")
 
    articles = topheadlines['articles']
 
    desc = []
    news = []
    img = []
 
    for i in range(len(articles)):
        myarticles = articles[i]
 
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
    df1 = pd.DataFrame(news, columns=["Title"])
    df2 = pd.DataFrame(desc, columns=["Content"])
    df3 = pd.DataFrame(img, columns=["Pictures"])
    df = pd.concat([df1, df2, df3], axis=1)
    data = df[0:10]

    filename_et = 'bbc.csv'
    data.to_csv(filename_et)

    HTML(data.to_html('.\\templates\\bbc.html', escape=False, formatters=dict(Pictures=image_link_to_html_tag),
                      justify='center'))


def image_link_to_html_tag(image_link):
    return '<img src="'+ image_link + '" width="120" >'

from subprocess import call
call(["python", "test.py"])

 
 
if __name__ == "__main__":
    bbc()
    app.run(debug=True,port=8000)