from math import pow
import numpy
import random
from pylab import plot,show

EPSILON = 1e-6

def distance_json(user1,user2):
	if len(user1.items()) != len(user2.items()):
		return False
	else:
		distance = 0
		m = len(user1.items())
		for i in range(0, m):
			if user1.items()[i][0] == user2.items()[i][0]:
				distance += pow(user1.items()[i][1] - user2.items()[i][1], 2)
			else:
				return False
		return distance

def distance(u,v):
	return numpy.linalg.norm(u-v)


def k_means(training_set, k = 2, number_of_iter = 1000):
	m = training_set.shape[0]
	centroids = random.sample(training_set, k)
	for i in range(number_of_iter):
		idx = [0]*m
		for j in range(m):
			current = training_set[j]
			distance_to_centroids_vector = ((centroids-current).dot((centroids-current).T)).diagonal()
			idx[j] = distance_to_centroids_vector.argmin()
		for l in range(k):
			cluster_size = 0
			new_centroid = numpy.zeros(training_set.shape[1])
			for t in range(m):
				if idx[t] == l:
					cluster_size += 1
					new_centroid += training_set[t]
			new_centroid /= cluster_size
			centroids[l] = new_centroid
	return [idx, centroids]



def test():
	# data generation
	data = numpy.vstack((numpy.random.rand(150,2) + numpy.array([.5,.5]),numpy.random.rand(150,2)))

	# computing K-Means with K = 2 (2 clusters)
	result = k_means(data)
	centroids = result[1]
	# assign each sample to a cluster
	idx = result[0]
	print idx
	# some plotting using numpy's logical indexing
	plot(data[idx==0,0],data[idx==0,1],'ob',
	     data[idx==1,0],data[idx==1,1],'or')
	plot(centroids[0,],centroids[1,],'sg',markersize=8)
	show()
