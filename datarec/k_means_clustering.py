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
	changed = True
	i = 0
	idx = [0]*m
	cost = cost_function(training_set, centroids, idx)

	while changed and i < number_of_iter:
	# for i in range(number_of_iter):
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
		new_cost = cost_function(training_set, centroids, idx)
		if new_cost == cost:
			changed = False
			break
		else:
			cost = new_cost
			i += 1
	return [idx, centroids, cost]

def cost_function(training_set, centroids, idx):
	m = training_set.shape[0]
	cost = 0
	for i in range(m):
		centroid = centroids[idx[i]]
		cost += distance(training_set[i], centroid)**2
	return cost/m



def test():
	# data generation
	data = numpy.vstack((numpy.random.rand(150,2) + numpy.array([.5,.5]),numpy.random.rand(150,2)))
	result = k_means(data,2)
	cost = result [2]
	centroids = numpy.array(result[1])
	idx = result[0]
	# repeat 100 times k_means
	for i in range(500):
		# computing K-Means with K = 2 (2 clusters)
		result = k_means(data,2)
		new_cost = result[2]
		if new_cost < cost:
			cost = new_cost
			centroids = numpy.array(result[1])
			idx = result[0]
			print "new---->"+str(cost)
	# assign each sample to a cluster
	red = numpy.array([ item for item, flag in zip( data, idx ) if flag == 1 ])
	blue = numpy.array([ item for item, flag in zip( data, idx ) if flag == 0 ])

	# some plotting using numpy's logical indexing
	plot(red[:,0],red[:,1],'ob')
	plot(blue[:,0],blue[:,1],'or')
	plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
	show()
