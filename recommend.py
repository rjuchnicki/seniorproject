# Robert Juchnicki														4/28/15
# 
# Engine to build recommenders for businesses in the Yelp Dataset Challenge 
# Data using user-based and item-based approaches. 


import numpy as np
import cPickle

from sys import platform
from datetime import date
from analysis import unique_vals
from math import sqrt


# Add a field 'reviews' to entries in the user database that is a list of all
# review ids for the user's reviews
def add_reviews_to_users(users, reviews, path):
	for user in users:
		users[user]['reviews'] = []

	for review in reviews:
		print 'Progress', i
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


# Return the magnitude of 
def magnitude(v):
	res = 0

	for i in v:
		res += i**2

	return sqrt(res)


# Normalize vector v
def normalize(v):
	mag = magnitude(v)

	for i in v:
		v[i] = i / mag

	return 


# Return the cosine distance of x and y.
def cosine_distance(x, y):
	return dot_product(x, y) / (magnitude(x) * magnitude(y))

# Return an item similarity matrix for the all the businesses in state using the 
# similarity measure sim.
def compute_similarities(businesses, state, sim):
	return


if __name__ == "__main__":
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

	user_keys = users.key()

	# Add a list of review ids to each entry in users if it does not already exist
	if 'reviews' not in users[user_keys[0]]:
		add_reviews_to_users(users, reviews, user_path)

	# Precompute a current state for each user and store it in the database
	if 'current_state' not in users[user_keys[0]]:
		add_current_state(users, reviews, businesses, user_path)

	states = unique_vals(users, 'current_state')

