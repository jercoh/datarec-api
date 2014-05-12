import app_config
import pymongo
from helper.importer import Importer
from datarec.recommender import ItemRecommender

dbName = 'test_database'
baserUrl = 'thebeautyst.org'
dataToImport = ['products', 'posts?type=photos', 'posts?type=videos', 'posts?type=post', 'users/purchases', 'users/views', 'users/likes?type=photos', 'users/likes?type=videos', 'users/likes?type=products', 'users/likes?type=post']
db = pymongo.MongoClient()[app_config.Config(dbName).MONGODB_DB]
contentTypes = ['likes_photos', 'likes_videos', 'likes_post', 'purchases']


def importData():
	importer = Importer(db)
	for url in dataToImport:
		importer.importData('http://'+baserUrl+'/datarec_exporter/'+url)

def calculate():
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