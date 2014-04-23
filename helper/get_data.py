from json_helper import extractAttribute, getUniqueValues

def getUserProductIds(users):
	result = []
	for user in users:
		products = sum(extractAttribute(user['orders'],'products'), [])
		ids = extractAttribute(products, 'product_id')
		result.append({'user_id' : user['user_id'], 'purchases' : getUniqueValues(ids)})
	return result

def getProductIds(products):
	return getUniqueValues(extractAttribute(products, "id"))