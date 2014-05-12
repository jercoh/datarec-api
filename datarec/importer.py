import app_config
import pymongo
import hot_ranking
from helper.json_helper import readJsonFile

class Importer:
	"""Data Importer"""
	def __init__(self, clientName):
		db = pymongo.MongoClient()[app_config.Config(clientName).MONGODB_DB]

	def importData(self, url):
		try: 
			dataType = url.split("/")[5].split("?")[1].split("=")[1]
		except:
			dataType = None
		collectionName = url.split("/")[5].split("?")[0]
		collection = self.db[collectionName]
		data = readJsonFile(url)
		#if collection == TODO
		for obj in data:
			for key in obj.keys():
				collection.update({"id":obj["id"]}, {"$set": {key: obj[key]}}, True)
