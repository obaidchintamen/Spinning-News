from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app import ma
import json

from marshmallow_sqlalchemy import field_for


db.Model.metadata.reflect(bind=db.engine,schema='nsdb')

class News(db.Model):
    __table__ = db.Model.metadata.tables['nsdb.news_data']
    
class NewsSchema(ma.ModelSchema):
    news = field_for(News, "news", dump_only=True)

    class Meta:
        model = News











