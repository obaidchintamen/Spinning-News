import requests
import pandas as pd
import json
from newsapi import NewsApiClient
import mysql.connector
from config import Config
import os

news_api_key = os.environ.get('NEWS_API_KEY')
newsApi = NewsApiClient(api_key=news_api_key)

df = pd.read_csv('news_sigma_spreadsheet_sheet1.csv')
columns = ['country','country_code', 'news_source']
df.columns = columns 

mydb = mysql.connector.connect(
  host=os.environ.get('HOST'),
  user=os.environ.get('DBUSER'),
  passwd=os.environ.get('PASSWD'),
  database=os.environ.get('DATABASE')
)
mycursor = mydb.cursor()

temp_dict = {}

for _,row in df.iterrows(): 
    row = row.to_dict()
    country = row['country']
    news_source = row['news_source']
    news = newsApi.get_top_headlines(sources=news_source,language='en')
    row['news_list']= news['articles'][:3]

    index = 0
    for article in row['news_list']:
        article_dict = json.loads(json.dumps(article))

        if article['author'] is not None:
            author = article['author'].replace("'", "")
            author = author.replace("\n", "\\n")
            author = author.replace("\r", "\\r")
            author = author.replace("\"", """ \\" """)
            article_dict['author'] = author
        if article['title'] is not None:
            title = article['title'].replace("'", "")
            title = title.replace("\n", "\\n")
            title = title.replace("\r", "\\r")
            title = title.replace("\"", """ \\" """)
            article_dict['title'] = title
        if article['description'] is not None:
            description = article['description'].replace("'", "")
            description = description.replace("\n", "\\n")
            description = description.replace("\r", "\\r")
            description = description.replace("\"", """ \\" """)
            article_dict['description'] = description
        if article['content'] is not None:
            content = article['content'].replace("'", "")
            content = content.replace("\n", "\\n")
            content = content.replace("\r", "\\r")
            content = content.replace("\"", """ \\" """)
            article_dict['content'] = content
        if article['url'] is not None:
            url = article['url'].replace("\t", "")
            article_dict['url'] = url


        row['news_list'][index] = article_dict
        index+=1

    temp_dict[country] = row

final_dict = {
    'countries':temp_dict
}

news_json_string = json.dumps(final_dict)

sqlFormula = """INSERT IGNORE INTO news_data (news) VALUES ('{}');"""
news_format = sqlFormula.format(news_json_string)
mycursor.execute(news_format)

mydb.commit()
print("done")
mycursor.close()





