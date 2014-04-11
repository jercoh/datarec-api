from math import pow
import numpy
import random

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


def k_means(training_set, k, number_of_iter):
	m = training_set.shape[0]
	centroids = random.sample(training_set, k)
	for i in range(0:number_of_iter):
		idx = [0]*m
		for j in range(0:m):
			current = training_set[j]
			distance_to_centroids_vector = ((centroids-current).dot((centroids-current).T)).diagonal()
			idx[j] = distance_to_centroids_vector.argmin()
		for l in range(0:k):
			cluster_size = 0
			new_centroid = numpy.zeros(training_set.shape[1])
			for t in range(0:m):
				if idx[t] == l:
					cluster_size += 1
					new_centroid += training_set[t]
			centroids[l] = new_centroid/cluster_size


