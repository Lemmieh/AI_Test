import numpy as np
import pandas as pd
from sklearn import tree
import json
import matplotlib.pyplot as plt


def findSampleDifferences(labels, samples):
	print(samples)
	# for i, j in zip(range(len(samples)), range(len(labels))):
	for i, j in zip(range(len(samples)),labels):
		sampleDt = (samples.iloc[i]['dateTime'])
		sampleDt = sampleDt[0:4]+sampleDt[5:7]+sampleDt[8:10]+'_'+sampleDt[11:13]+sampleDt[14:16]
		labelDt = (j)
		if sampleDt == labelDt:
			print('Data match')
			pass
		else:
			print ('Data mismatch found')
			print('data.json dateTime:	%s' % (labelDt))
			print('df dateTime:	%s' % (sampleDt))
			input('Press Enter to Continue') 
		# print(sampleDt, labelDt)


def main():
	print('Getting Train Target...')
	train_target = []
	df = pd.read_csv('set2_rainfall_data.csv')
	df = df[['dateTime','value']]
	dt = {
	'dateTime' : [],
	'testDateTime' : []
	}


	for i, j in zip(df['value'], df['dateTime']):
		train_target.append(round(i, 5))
		dt['dateTime'].append(j)

	print('Getting Train Data...')
	with open('data.json') as json_file:
		data = json.load(json_file)

	# findSampleDifferences(data, df)
	train_data = []
	for i in data:
		val = []
		for j in data[i]:
			val.append(data[i][j])
		train_data.append(val)


	print('Getting Test Target...')
	test_target = []
	for i in range(len(train_target)//2):
		if i % 10 == 0:
			test_target.append(train_target.pop(i))
			dt['testDateTime'].append(dt['dateTime'].pop(i))

	print('Getting Test Data...')
	test_data = []
	for i in range(len(train_data)//2):
		if i % 10 == 0:
			test_data.append(train_data.pop(i))



	print('Training Tree...')
	clf = tree.DecisionTreeRegressor(max_depth=10)
	clf = clf.fit(train_data, train_target)
	# print(test_target)
	# print(test_data)
	predicted = clf.predict(test_data)
	testData = {
	'test target' : test_target,
	'predicted' : predicted
	}
	finalDf = pd.DataFrame(testData,columns = ['test target','predicted'])
	finalDf['difference'] = finalDf['test target'] - finalDf['predicted']
	finalDf['dateTime'] = dt['testDateTime']
	finalDf['dateTime'] = pd.to_datetime(finalDf['dateTime'])
	finalDf.set_index('dateTime', inplace=True)

	print(finalDf)
	print('Cumulative difference:')
	print(finalDf['difference'].abs().sum()/len(finalDf))

	finalDf[['test target', 'predicted']].plot()
	plt.show()

main()