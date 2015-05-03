# Robert Juchnicki                                                      4/28/15
# 
# Trains the recommenders used to output recommendation in recommend.py. Also
# adds the current state and a list of review ids for every user in the user
# database. 


import numpy as np
import cPickle
import os

from sys import platform
from datetime import date
from math import sqrt

# Import from project modules
from analysis import unique_vals
from db_builder import BUSINESS_CSV_INDICES


# Add a field 'reviews' to entries in the user database that is a list of all
# review ids for the user's reviews
def add_reviews_to_users(users, reviews, path):
	for user in users:
		users[user]['reviews'] = []

	for review in reviews:
		user = reviews[review]['user_id']
		review_list = users[user]['reviews']
		review_list.append(review)

	f = open(path, 'w')
	cPickle.dump(users, f)
	f.close()

	return


# Return the key in a dictionary with the max value.
def key_for_max_value(d): 
    values = list(d.values())
    keys = list(d.keys())

    return keys[values.index(max(values))]


# Returns the user's current state. Looks at the dates and locations of all
# business the user has reviewed to compute the result. 
def determine_state(user_id, users, reviews, businesses):
	review_info = []

	for review in users[user_id]['reviews']:
		business_id = reviews[review]['business_id']
		date_string = reviews[review]['date']
		day = date(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:]))

		review_info.append((review, day, businesses[business_id]['state']))

	review_info.sort(key = lambda x: x[1])	# sort review_info tuples by date

	# determine the most common state among the most recent half of reviews
	n = len(review_info)
	states = {}
	for i in xrange(n/2, n):
		state = review_info[i][2]
		if state in states:
			states[state] += 1
		else: 
			states[state] = 1

	return key_for_max_value(states)


# Add the user's current state to the user database. The current state is
# computed using determine state
def add_current_state(users, reviews, businesses, path):
	for user in users:
		users[user]['current_state'] = determine_state(user, users, reviews, businesses)

	f = open(path, 'w')
	cPickle.dump(users, f)
	f.close()

	return


# Return the dot product of vectors x and y.
def dot_product(x, y):
	if len(x) != len(y):
		return None

	product = 0.0
	for i in xrange(0, len(x)):
		product += x[i]* y[i]

	return product


# Return the magnitude of vector v.
def magnitude(v):
	res = 0.0

	for i in v:
		res += i**2

	return sqrt(res)


# Normalize vector v. 
def normalize(v):
	mag = magnitude(v)

	for i in v:
		v[i] = i / mag

	return 


# Return the cosine distance of x and y.
def cosine_distance(x, y):
	m1 = magnitude(x)
	m2 = magnitude(y)

	if m1 == 0 or m2 == 0:
		return 0

	return dot_product(x, y) / (m1 * m2)


# Return a vectore for a business whose entries are 0's and 1's, indicating
# the presence or absence of an attribute or category for the business. 
def attribute_vector(business_entry, attributes, categories):
	v = []

	for i in xrange(0, len(attributes)):
		try:
			if business_entry[attributes[i]] == 'True':
				v.append(1.0)
			else:
				v.append(0.0)
		except:
			v.append(0.0)

	for i in xrange(0, len(categories)):
		if categories[i] in business_entry['categories']:
			v.append(1.0)
		else:
			v.append(0.0)

	return v


# Return an item similarity matrix for the all the businesses in state using the 
# similarity measure sim.
def compute_similarities(businesses, state, sim, make_vector, attributes, categories):
	labels = []

	for business in businesses:
		if businesses[business]['state'] == state:
			labels.append(business)

	xr = xrange(0,len(labels))
	similarities = [[0 for i in xr] for i in xr]

	for i in xrange(0, len(labels)):
		business1 = make_vector(businesses[labels[i]], attributes, categories)

		for j in xrange(0, len(labels)):
			if i != j:
				business2 = make_vector(businesses[labels[j]], attributes, categories)
				similarity = sim(business1, business2)
				similarities[i][j] = similarity
			else:
				similarities[i][j] = 0.0

	return similarities, labels



if __name__ == "__main__":
	try: 
		os.makedirs('similarity_matrices')
	except OSError:
		if not os.path.isdir('similarity_matrices'):
			raise


	if platform == 'win32':
		slash = '\\'
	else:
		slash = '/'


	user_path = 'db_pickled' + slash + 'user_db_pickled'
	f = open(user_path)
	users = cPickle.load(f)
	f.close()

	f = open('db_pickled' + slash + 'business_db_pickled')
	businesses = cPickle.load(f)
	f.close()

	f = open('db_pickled' + slash + 'review_db_pickled')
	reviews = cPickle.load(f)
	f.close()


	user_keys = users.keys()

	# Add a list of review ids to each entry in users if it does not already exist
	if 'reviews' not in users[user_keys[0]]:
		add_reviews_to_users(users, reviews, user_path)

	# Precompute a current state for each user and store it in the database
	if 'current_state' not in users[user_keys[0]]:
		add_current_state(users, reviews, businesses, user_path)


	attributes = []

	prefixes = (
		'attributes.Ambience',
		'attributes.Good For',
		'attributes.Good for',
		'attributes.Dietary'
	)

	for label in BUSINESS_CSV_INDICES:
		if (label.startswith(prefixes)):
			attributes.append(label)

	categories = [
		'Restaurants',
		'Food Stands',
		'Bistro',
		'Buffets',
		'Grocery',
		'Drugstores', 
		'Hotels & Travel',
	]

	states = ['IL', 'WI', 'PA', 'NC']


	for state in states: 
		print "BUILDING MATRIX FOR", state

		M, labels = compute_similarities(businesses, state, cosine_distance, attribute_vector, attributes, categories)

		print "COMPLETED MATRIX FOR", state
		print "SAVING MATRIX FOR", state

		f = open('similarity_matrices' + slash + 'matrix_' + state, 'w')
		cPickle.dump(M, f)
		f.close()

		f = open('similarity_matrices' + slash + 'labels_' + state, 'w')
		cPickle.dump(labels, f)
		f.close()

		print "SAVED MATRIX FOR", state


	# Build a second similarity matrix for IL using all categories
	attributes = []

	prefixes = (
		'attributes.Ambience',
		'attributes.Good For',
		'attributes.Good for',
		'attributes.Dietary'
	)

	for label in BUSINESS_CSV_INDICES:
		if (label.startswith(prefixes)):
			attributes.append(attributes)

	f = open('category_list', 'r')
	categories = cPickle.load(f)
	f.close()

	states = ['IL']

	for state in states: 
		print "BUILDING MATRIX FOR", state

		M, labels = compute_similarities(businesses, state, cosine_distance, attribute_vector, attributes, categories)

		print "COMPLETED MATRIX FOR", state
		print "SAVING MATRIX FOR", state

		f = open('similarity_matrices' + slash + 'matrix_' + state + '_2', 'w')
		cPickle.dump(M, f)
		f.close()

		f = open('similarity_matrices' + slash + 'labels_' + state + '_2', 'w')
		cPickle.dump(labels, f)
		f.close()

		print "SAVED MATRIX FOR", state
		