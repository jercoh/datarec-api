import pandas as pandas
from pandas import DataFrame
import numpy as numpy

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

def normalize_matrix(matrix, axis, normType):
	if normType == 1:
		norm_vector  = numpy.sum(matrix,axis=axis) # axis = -1 for row normalization, axis = -2 for columns
	elif normType == 2:
		norm_vector  = numpy.sum(matrix**2,axis=axis)**(1./2) # axis = -1 for row normalization, axis = -2 for columns
	return matrix / norm_vector[:,numpy.newaxis].astype(float)

def dictionarizearray(x,list_of_columns):
	"""
	Assigns a dictionary key to each of the m-columns
	of the (n,m) x array
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