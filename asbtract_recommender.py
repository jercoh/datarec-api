import pandas as pandas
from pandas import DataFrame
import numpy as numpy
import re
import operator
import argparse
import datarec_dbconfig
import pymongo

db_name = datarec_dbconfig.getName()
db = pymongo.MongoClient()[db_name]
cnames = ['id', 'email', 'history']

def sim(u,v):
	norm_u = numpy.linalg.norm(u)
	norm_v = numpy.linalg.norm(v)
	if norm_u != 0 and norm_v !=0:
		return u.dot(v)/(norm_u*norm_v)
	else:
		return 0


def sim_object(objectId_1, objectId_2):
	vect = similarity_dic[str(objectId_1)]
	return vect[objects_list.index(str(objectId_2))]

def normalize_matrix(matrix, axis, type):
	if type == 1:
		norm_vector  = numpy.sum(matrix,axis=axis) # axis = -1 for row normalization, axis = -2 for columns
	elif type == 2:
		norm_vector  = numpy.sum(matrix**2,axis=axis)**(1./2) # axis = -1 for row normalization, axis = -2 for columns
	return matrix / norm_vector[:,numpy.newaxis].astype(float)


def dictionarizearray(x,list_of_columns):
	"""
	Assigns a dictionary key to each of the m-columns
	of the (n,m) x array

	EXAMPLE in some code which loads this function:
	>>> names=['var1','var2',...,'varN']
	>>> xnames=dictionarizearray(x,names)
	>>> xmask=x[xnames['var1']<xnames['var2']]
	#instead of
	>>> xmask=x[x[:,0]<x[:,1]]
	"""

	import sys
	x=numpy.asarray(x)
	# if not len(x.shape)==2:
	#     sys.exit('ERROR: Not a two-dimensional array')

	if x.shape[1]!=len(list_of_columns):
		sys.exit('ERROR: Wrong number of dictionary keys')
	dictx={}
	for i in range(len(list_of_columns)):
		dictx[list_of_columns[i]]=x[:,i]
	return dictx

def compute_similarity_matrix2(matrix):
	a = numpy.sqrt(sum(matrix*matrix))[numpy.newaxis]
	return normalize_matrix(matrix.T.dot(matrix)*1/(a.T.dot(a)), -2, 1)

def sort_nicely( l ):
	""" Sort the given list in the way that humans expect.
	"""
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )

def read_table_from_file(file, cnames):
	return pandas.read_table(file, sep=';', header=None, names=cnames)


def get_object_list(dataFrame):
	object_iter = (set(x.split('|')) for x in getattr(dataFrame, cnames[2]))
	objects = sorted(set.union(*object_iter))
	sort_nicely(objects)
	return objects

def prepare_data(file):
	user_item_matrix = read_table_from_file(file, cnames)
	objects = get_object_list(user_item_matrix)
	dummies = DataFrame(numpy.zeros((len(user_item_matrix), len(objects))), columns=objects)
	for i, ph in enumerate(getattr(user_item_matrix, cnames[2])):
		dummies.ix[i, ph.split('|')] = 1
	#object_windic = user_item_matrix.join(dummies.add_prefix('object_'))
	object_windic = user_item_matrix.join(dummies)
	return object_windic

def clean_data(dataFrame):
	# remove useless columns
	dataFrame = dataFrame.drop(cnames[0],1)
	dataFrame = dataFrame.drop(cnames[1],1)
	dataFrame = dataFrame.drop(cnames[2],1)
	# remove Null columns and rows
	dataFrame = dataFrame.dropna(axis=0,how='all')
	dataFrame = dataFrame.dropna(axis=1,how='all')
	return dataFrame

def get_n_most_similar_objects(n, object_id):
	vect = similarity_dic[object_id]
	index_list = numpy.argsort(vect)[-n:]
	similar_objects = []
	for i in range(len(index_list)):
		similar_objects.append(objects_list[index_list[i]])
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

def init(content_url):
	global dataFrame, objects_list, dataFrame_clean, similarity_matrix, similarity_dic
	dataFrame = prepare_data(content_url)
	objects_list = get_object_list(dataFrame)
	dataFrame_clean = clean_data(prepare_data(content_url))
	similarity_matrix = compute_similarity_matrix2(numpy.array(dataFrame_clean))
	similarity_dic = dictionarizearray(similarity_matrix, objects_list)

def calculate(client_id, client_name, content_type):
	for i in dataFrame.index:
		id = dataFrame.ix[i][cnames[0]]
		email = dataFrame.ix[i][cnames[1]]
		reco = get_n_recommended_objects_for_user(10, id).tolist()
		collection = db[client_name]
		collection.update({"user_id":id.astype(int)}, {"$set": {"client_id": client_id, "email": email, content_type+"_recommendation" : reco}}, True)

def hello():
	return "hello"

content_url = '/Users/Jeremie/Downloads/liste-commandes.csv'#'C:\Users\G7V\Downloads\liste-commandes.csv'
init(content_url)
calculate(content_url)












































































































	