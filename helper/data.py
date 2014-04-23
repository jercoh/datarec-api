import json

def extractAttribute(data, key):
	if isinstance(data, dict):
		return [data[key]]
	elif isinstance(data, list):
		return [obj[key] for obj in data]
	else: return []

