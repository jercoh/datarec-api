from json_helper import extractAttribute, getUniqueValues

def getUserItemIds(users, contentType):
	result = []
	for user in users:
		if (contentType == 'purchases'):
			try:
				products = sum(extractAttribute(user['purchases'],'products'), [])
				ids = extractAttribute(products, 'id')
				result.append({'id' : user['id'], 'purchases' : getUniqueValues(ids)})
			except KeyError:
				pass
		else:
			try:
				result.append({'id' : user['id'], contentType : user[contentType]})
			except KeyError:
				pass
	return result

def getItemIds(items):
	return getUniqueValues(extractAttribute(items, "id"))