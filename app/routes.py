from app import app
from app import ma

from app.models import News, NewsSchema
from flask import jsonify

import json


@app.route('/news')
def articles():
    n = News.query.all()
    n = (n[-1])
    news_schema = NewsSchema()
    output = news_schema.dump(n)
    output_json = jsonify(output)

    return output_json






























