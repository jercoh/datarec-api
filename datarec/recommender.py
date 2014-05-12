from pandas import DataFrame
import numpy as numpy
import operator
from helper.json_helper import readJsonFile
from helper.get_data import getItemIds, getUserItemIds
from helper.dataframe_helper import cleanData
import helper.maths

class ItemRecommender:
	"""Item-Based Recommender Class"""
	def __init__(self, contentType, items, users):
		self.itemIds = getItemIds(items)
		self.userItemIds = getUserItemIds(users, contentType)
		dummies = DataFrame(numpy.zeros((len(users), len(self.itemIds)+1)), columns=['id']+self.itemIds)
		for i in range(len(self.userItemIds)):
			dummies.loc[i,'id'] = self.userItemIds[i]['id']
			for p in self.userItemIds[i][contentType]: 
				dummies.loc[i, p] = 1
		self.dataFrame = dummies
		self.cleanDataFrame = cleanData(dummies.copy(), ['id'])
		self.userItemsMatrix = helper.maths.normalize_matrix(numpy.array(self.cleanDataFrame), -1, 2)
		self.similarity_matrix = helper.maths.compute_similarity_matrix2(numpy.array(self.cleanDataFrame))
		self.similarity_dic = helper.maths.dictionarizearray(self.similarity_matrix, self.itemIds)


	def get_n_most_similar_objects(self, n, object_id):
		vect = self.similarity_dic[object_id]
		index_list = numpy.argsort(vect)[-n:]
		similar_objects = []
		for i in range(len(index_list)):
			similar_objects.append(self.itemIds[index_list[i]])
		return similar_objects

	def get_n_recommended_objects_for_user(self, n, id, contentType):#n et id sont des int
		similarity = {}
		C = set()
		user = (u for u in self.userItemIds if u["id"] == id).next()
		if (user[contentType] != []):
			for item in user[contentType]:
				similar_objects = self.get_n_most_similar_objects(2*n, item)
				C = C.union(set(similar_objects))
			C = C - set(user[contentType])
			for item in C:
				m = 0
				for itm in user[contentType]:
					m += helper.maths.sim_object(item, itm, self.similarity_dic, self.itemIds)
				similarity[item]= m
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
		return []
