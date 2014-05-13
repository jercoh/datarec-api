import app_config
import pymongo
from helper.importer import Importer
from datarec.recommender import ItemRecommender
import datarec.hot_ranking as ranking
from datetime import datetime
from mako.template import Template
from mako.lookup import TemplateLookup
import mandrill

dbName = 'test_database'
baserUrl = 'thebeautyst.org'
dataToImport = ['products', 'posts?type=photos', 'posts?type=videos', 'posts?type=post', 'users/purchases', 'users/views', 'users/likes?type=photos', 'users/likes?type=videos', 'users/likes?type=products', 'users/likes?type=post']
db = pymongo.MongoClient()[app_config.Config(dbName).MONGODB_DB]
collectionNames = ['products', 'posts']
contentTypes = ['likes_photos', 'likes_videos', 'likes_post', 'purchases']
templatePath = ''
mylookup = TemplateLookup(directories=[''],input_encoding='utf-8',output_encoding='utf-8',)
mandrill_client = mandrill.Mandrill('QVQhU-pdRHiaPGWceEKZfg')


def importData():
	importer = Importer(db)
	for url in dataToImport:
		importer.importData('http://'+baserUrl+'/datarec_exporter/'+url)

def calculate_recommendations():
	collection = db['users']
	users = list(collection.find())
	for contentType in contentTypes:
		print contentType
		if (contentType.split('_')[0] == 'likes'):
			recommender = ItemRecommender(contentType, list(db['posts'].find({'type': contentType.split('_')[1]})), users)
		else:
			recommender = ItemRecommender(contentType, list(db['products'].find()), users)
		for user in users:
			if (contentType in user):
				results = recommender.get_n_recommended_objects_for_user(10, user['id'], contentType)
				if (results != []):
					collection.update({"id":user["id"]}, {"$set": {'recommendation_'+contentType: results.tolist()}}, True)

def calculate_popularity():
	for collectionName in collectionNames:
		collection = db[collectionName]
		for item in list(collection.find()):
			if (collectionName == 'products'):
				score = ranking.hot(item["total_sales"], datetime.strptime(item["created_at"], '%Y-%m-%d %H:%M:%S'))
			else:
				score = ranking.hot(item["likes"], datetime.strptime(item["created_at"], '%Y-%m-%d %H:%M:%S'))
			collection.update({"id": item["id"]}, {"$set": {"score": score}}, True)

def send_newsletter():
	mytemplate = mylookup.get_template(template)
	collection_users = db['users']
	collection_posts = db['posts']
	collection_products = db['products']
	#users = list(collection_users.find())
	# for user in users:
	user = list(collection_users.find({'id':'49'}))[0]
	try:
		recommended_video = list(collection_posts.find({'id': user['recommendation_likes_videos'][0], 'type': 'videos'}))[0]
	except:
		recommended_video = list(collection_posts.find({'type':'videos'}).sort([('score',-1)]).limit(-1))[0]
	try:
		recommended_article = list(collection_posts.find({'id': user['recommendation_likes_post'][0], 'type': 'post'}))[0]
	except:
		recommended_article = list(collection_posts.find({'type':'post'}).sort([('score',-1)]).limit(-1))[0]
	try:
		product_ids = user['recommendation_purchases']
	except:
		product_ids = []
	recommended_products = []
	if (product_ids != []):
		for product_id in product_ids:
			recommended_products.append(list(collection_products.find({'id':product_id}))[0])
	else:
		recommended_products = list(collection_products.find().sort([('score',-1)]).limit(-8))
	html = mytemplate.render(video=recommended_video, article= recommended_article, products = recommended_products)
	mandrill_client.messages.send(message=message(html, 'jeremcoh@gmail', user['first_name']+user['last_name']), async=False, ip_pool='Main Pool', send_at='')

def message(html, email, name):
	message = {
		'attachments': None,
        'auto_html': None,
        'auto_text': None,
        'from_email': 'jeremie@datarec.io',
		 'from_name': 'Jeremie Cohen',
		 'headers': {'Reply-To': 'jeremie@datarec.io'},
		 'html': html,
		 'important': False,
		 'metadata': {'website': 'www.datarec.io'},
		 'preserve_recipients': None,
		 'recipient_metadata': [{'rcpt': email,
		                         'values': {'user_id': 123456}}],
		 'subject': 'Test Email',
		 'tags': ['thebeautyst'],
		 'to': [{'email': email,
		         'name': name,
		         'type': 'to'}],
		 'track_clicks': True,
		 'track_opens': True,
		 'tracking_domain': True
	}
	return message

