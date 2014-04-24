from pandas import DataFrame

def cleanData(dFrame, keys):
	# remove useless columns
	for key in keys:
		dFrame = dFrame.drop(key,1)
	# remove Null columns and rows
	dFrame = dFrame.dropna(axis=0,how='all')
	dFrame = dFrame.dropna(axis=1,how='all')
	return dFrame