import requests
from flask import Flask, render_template
from newsapi import NewsApiClient
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
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
    url_for = []
    data = []
    whole_Data=[]


    # link for extract html data
    def getdata(url):
        r = requests.get(url)
        return r.text

    def convert(list):
        s = [str(i) for i in list]
        res = "".join(s)
        return (res)

    for i in range(len(articles)):
        myarticles = articles[i]
 
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        url_for.append(myarticles['url'])

    for i in range(len(url_for)):
        htmldata = getdata(url_for[i])
        soup = BeautifulSoup(htmldata, 'html.parser')
        for rate in soup.findAll('div', {'data-component': 'text-block'}):
            for data in rate.find_all("p"):
                whole_Data.append({'val': str(i),'data':data.get_text()})
                # whole_Data.append('------------')

    new = pd.DataFrame.from_dict(whole_Data)
    for i in range(len(new)):
        data.append("".join(new[new.val==str(i)]['data']))



    df1 = pd.DataFrame(news, columns=["Title"])
    df2 = pd.DataFrame(desc, columns=["Content"])
    df3 = pd.DataFrame(img, columns=["Pictures"])
    df4 = pd.DataFrame(url_for, columns=["Completedata"])
    df5 = pd.DataFrame(data, columns=["data"])

    df = pd.concat([df1, df2, df3,df4,df5], axis=1)
    data = df[0:10]
    #

    filename_et = 'bbc.csv'
    data.to_csv(filename_et)

    HTML(data.to_html('.\\templates\\bbc.html', escape=False, formatters=dict(Pictures=image_link_to_html_tag),
                      justify='center'))


def image_link_to_html_tag(image_link):
    return '<img src="'+ image_link + '" width="120" >'
#
# from subprocess import call
# call(["python", "test.py"])



if __name__ == "__main__":
    bbc()
    app.run(debug=True,port=8000)