from pandas import DataFrame
import numpy as numpy
import datarec_dbconfig
import pymongo
from helper.json_helper import readJsonFile
from helper.get_data import getProductIds, getUserProductIds
from helper.dataframe_helper import cleanData
import helper.maths


db_name = datarec_dbconfig.getName()
db = pymongo.MongoClient()[db_name]
cnames = ['id', 'email', 'history']

class ItemRecommender:
	"""Item-Based Recommender Class"""
	def __init__(self, jsonProducts, jsonUsers):
		products = readJsonFile(jsonProducts)
		users = readJsonFile(jsonUsers)
		self.productIds = getProductIds(products)
		self.userProductIds = getUserProductIds(users)
		dummies = DataFrame(numpy.zeros((len(users), len(self.productIds))), columns=['user_id']+self.productIds)
		for i in range(len(self.userProductIds)):
			dummies.ix[i]['user_id'] = self.userProductIds[i]['user_id']
			for p in self.userProductIds[i]['purchases']: 
				dummies.ix[i][p] = 1
		self.dataFrame = dummies
		self.cleanDataFrame = cleanData(dummies.copy(), ['user_id'])
		self.similarity_matrix = helper.maths.compute_similarity_matrix2(numpy.array(self.cleanDataFram))
		self.similarity_dic = helper.maths.dictionarizearray(self.similarity_matrix, self.productIds)


	def get_n_most_similar_objects(n, object_id):
		vect = self.similarity_dic[object_id]
		index_list = numpy.argsort(vect)[-n:]
		similar_objects = []
		for i in range(len(index_list)):
			similar_objects.append(self.productIds[index_list[i]])
		return similar_objects

	def get_n_recommended_objects_for_user(n, id):#n et id sont des int
		similarity = {}
		C = set()
		user = dataFrame[cnames[0]].map(lambda x: x == id)
		user_history = dataFrame[user][cnames[2]].iloc[0].split('|')
		for object in user_history:
			similar_objects = get_n_most_similar_objects(2*n, object)
			C = C.union(set(similar_objects))
		C = C - set(user_history)
		for object in C:
			m = 0
			for purchase in user_history:
				m += sim_object(object, purchase)
			similarity[object]= m
		similarity = sorted(similarity.iteritems(), key=operator.itemgetter(1))
		similarity.reverse()
		similarity_array = numpy.array(similarity).T
		l = len(similarity_array[1])
		if  l < n:
			# return numpy.argsort(-similarity_array[1].astype(float))[-l:]
			return similarity_array[0]
		else:
			# return numpy.argsort(-similarity_array[1].astype(float))[-n:]
			return similarity_array[0][0:n]

	def calculate(client_id, client_name, content_type):
		for i in dataFrame.index:
			id = dataFrame.ix[i][cnames[0]]
			email = dataFrame.ix[i][cnames[1]]
			reco = get_n_recommended_objects_for_user(10, id).tolist()
			collection = db[client_name]
			collection.update({"user_id":id.astype(int)}, {"$set": {"client_id": client_id, "email": email, content_type+"_recommendation" : reco}}, True)


content_url = '/Users/Jeremie/Downloads/liste-commandes.csv'#'C:\Users\G7V\Downloads\liste-commandes.csv'
init(content_url)
calculate(content_url)
