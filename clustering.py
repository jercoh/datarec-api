from math import pow

def distance(user1,user2):
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

