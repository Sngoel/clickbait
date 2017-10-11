'''
NLP 120 Features + Random Forest Model
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import sys
import csv
import string
import pickle
import numpy as np
from nltk import word_tokenize
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, StratifiedKFold

sys.path.append('../..')
from util.load_data import JSONData

import warnings
warnings.filterwarnings("ignore")

''' Constants and Parameters '''
DATA_ROOT = '../../../Data/dataset/'       # Root Folder of where Dataset Resides
MODEL_ROOT = '../../../Models/'            # Root Folder of where Model Resides
np.random.seed(9892)                       # Seed Parameter for PRNG

''' Import Data '''
# Load Dataset
data_load = JSONData(DATA_ROOT+'instances_train.jsonl', DATA_ROOT+'truth_train.jsonl', DATA_ROOT+'instances_test.jsonl')
raw_data = csv.reader(open('../../../Data/feat.csv', 'rb'), delimiter=',')
X = map(lambda x: map(lambda y: float(y), x), raw_data)
train_Y = data_load.load_train_Y()

# Filter Out Invalid Results
print('PREFILTER: ' + str(len(X)))
X = filter(lambda x: len(x) == 121, X)
print('POSTFILTER: ' + str(len(X)))

# Filter/Process Adjusting Results
print('Loading Dataset')
X = np.array(map(lambda x: x[1:], X), dtype='float')
Y = np.array(map(lambda x: 0 if x['truthClass'] == 'no-clickbait' else 1, map(lambda x: train_Y[int(x[0])], X)))

''' Train Full Model '''
print('Training Full Model')
randforest = RandomForestClassifier(criterion='entropy')
randforest.fit(X, Y)

''' Generate Predictions '''
# Generate Predictions
data = csv.reader(open('../../../Data/test_feat.csv', 'rb'), delimiter=',')
X_test = np.array(map(lambda x: map(lambda y: float(y), x), data))

print('PREFILTER: ' + str(len(X_test)))
X = filter(lambda x: len(x) == 121, X_test)
print('POSTFILTER: ' + str(len(X_test)))

# Filter Out Invalid Results

# Generate Predictions
# Y_pred = map(lambda x: randforest.predict([x[1:]]), X_test)

# print(Y_pred[:10])
# print(X_test.shape)

# Generate Predictions
# output = open('predictions.csv', 'wb')
# map(lambda x: output.write(str(int(x[0])) + ',' + str(x[1]), zip(X_test, Y_pred))
# output.close()

# print('DONE!')
