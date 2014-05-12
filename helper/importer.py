import app_config
import pymongo
from helper.json_helper import readJsonFile

class Importer:
	"""Data Importer"""
	def __init__(self, clientDB):
		self.db = clientDB

	def importData(self, url):
		try: 
			dataType = url.split("/")[4].split("?")[1].split("=")[1]
		except:
			dataType = None
		collectionName = url.split("/")[4].split("?")[0]
		collection = self.db[collectionName]
		data = readJsonFile(url, False)
		for obj in data:
			for key in obj.keys():
				collection.update({"id":obj["id"]}, {"$set": {key: obj[key]}}, True)
