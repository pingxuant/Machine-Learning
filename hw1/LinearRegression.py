# ML 2017 hw1 
# Linear Regression with Gradient Descent, version 1
# Validation (Ev)

import numpy as np
from sys import argv

# read from csv and trim all chinese words
train = []
with open(argv[1], 'rb') as f:
	data = f.read().splitlines()
	i = 0
	for line in data[1:]: # trim the first data which is header
		line = [x.replace("\'", "") for x in str(line).split(',')[3:]]

		if i % 18 == 10:
			line = [x.replace("NR", "0") for x in line]

		line = [float(x) for x in line]
		if i < 18:
			train.append(line)
		else:
			train[i % 18] += line
		
		i += 1

test = []
with open(argv[2], 'rb') as f:
	data = f.read().splitlines()
	i = 0
	for line in data: # trim the first data which is header
		line = [x.replace("\'", "") for x in str(line).split(',')[2:]]

		if i % 18 == 10:
			line = [x.replace("NR", "0") for x in line]

		line = [float(x) for x in line]
		test.append(line)

		i += 1

np.set_printoptions(precision = 2, suppress = True)

def print_message():
	print("iteration =", ITERATION)
	print("eta =", ETA)
	print("validation =", VALIDATION)
	print("selected features =", FEATURE)
	print("w =\n", w)
	print("b =", b)

# define constants
ITERATION = 10000
ETA = 1e-8
VALIDATION = 0

MAX_TIME = int(len(train[0]))
PERIOD = 7

FEATURE = [5, 9, 12] # selected feature
NUM_FEATURE = len(FEATURE)
#w = np.array([[0.01] * PERIOD] * NUM_FEATURE) # feature * period
w = np.array([[-0.02, -0.04, 0.01, -0.02, 0.02, 0.01, -0.04, -0.03, 0.2], [-0.02, -0.02, 0.2, -0.21, -0.04, 0.49, -0.54, 0.01, 1.03], [-0.2, 0.11, -0.06, -0.09, -0.03, 0.0, -0.06, 0.12, 0.31]])
#b = 0.959 # bias
b = 1.0

print_message()

def filter_data(FEATURE, d):
	result = []
	for sf in FEATURE:
		
		result.append(train[d * 18 + sf])
	
	return result

def filter_hours(data, start, period, selected_features):
	result = []
	for f in selected_features:
		result += [data[f][start : start + period]]
	
	return result

def predict(X, w, b):
	Y = np.sum(X * w) + b
	return Y

# train
all_Ein = []
for i in range(ITERATION):
	if i % 100 == 0:
		print("progress:", i)
	
	iter_Ein = []
	sum_gradient_X = np.zeros([NUM_FEATURE, PERIOD])
	sum_gradient_b = 0.0

	for start in range(MAX_TIME - PERIOD - 1)[VALIDATION:]:

		X = np.array( filter_hours(train, start, PERIOD, FEATURE) )
		yh = train[9][start + PERIOD]

		sum_gradient_X += (-2.) * (yh - predict(X, w, b)) * X
		sum_gradient_b += (-2.) * (yh - predict(X, w, b))

		Etrain = (yh - predict(X, w, b)) ** 2
		iter_Ein.append(Etrain)

	current_Ein = np.mean(iter_Ein)
	all_Ein.append(current_Ein)
	if i % 10 == 0:
		print("current Ein =", np.sqrt(current_Ein))

	# update parameters
	w = w - ETA * sum_gradient_X
	b = b - ETA * sum_gradient_b	

average_Ein = np.sqrt(np.mean(all_Ein))

# print result
print_message()
print("average Ein = ", average_Ein)

# validation
Evalid = []
for start in range(MAX_TIME - PERIOD - 1)[:VALIDATION]:
	X = np.array( filter_hours(train, start, PERIOD, FEATURE))
	yh = train[9][start + PERIOD]

	Ev = (yh - predict(X, w, b)) ** 2
	Evalid.append(Ev)
if VALIDATION:
	print("Evalid =", np.sqrt(np.mean(Evalid)))

# test
with open(argv[3], "w") as f:
	f.write("id,value\n")
	for d in range(240):
		
		test_data = filter_hours(test[ d*18 : d*18 + 18], 9-PERIOD, PERIOD, FEATURE)
		np_data = np.array(test_data)

		dot_result = int(predict(np_data, w, b))
		f.write("id_" + repr(d) + "," + repr(dot_result) + "\n")
