import json
import re
import urllib2

def extractAttribute(data, key):
	if isinstance(data, dict):
		return [data[key]]
	elif isinstance(data, list):
		return [obj[key] for obj in data]
	else: return []

def sortNicely(l):
	# Sort the given list in the way that humans expect.
	convert = lambda text: int(text) if (hasattr(text, 'isdigit') and text.isdigit()) else text
	l.sort( key=convert  )
	return l

def getUniqueValues(l):
	if all(isinstance(item, int) for item in l):
		l.sort()
		return list(set(l))
	else:
		return sortNicely(list(set(l)))

def readJsonFile(url, local):
	if (local == True):
		json_data = open(url)
	else:
		json_data = urllib2.urlopen(url)
	data = json.load(json_data)
	json_data.close()
	return data