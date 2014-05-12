import app_config
import pymongo
import hot_ranking
from datetime import datetime

db = pymongo.MongoClient()[app_config.Config.MONGODB_DB]

import abstract_recommender
def calculate_recommendations_for(client):
	client_id = client['id']
	client_name = client['name']
	for content in client['contents']:
		content_type = content['content']
		content_url = content['url']
		abstract_recommender.calculate(client_id, client_name, content_type, content_url)

def calculate_popularity_for(product):
	score = hot_ranking.hot(product["total_sales"], datetime.strptime(product["created_at"], '%d/%m/%y %H:%M'))
	db.products.update({"product_id": product["product_id"]}, {"$set": {"score": score}}, True)

def calculate_popularity():
	for product in db.products.find():
		calculate_popularity_for(product)

def get_n_most_popular_products(n):
	list(db.products.find().sort("score", -1).limit(n))