# Robert Juchnicki														4/24/15
# 
# Performs analysis and inspection of data accross databases. This script uses 
# the databases built using db_builder.py and saved using the cPickle module.


import cPickle

from sys import platform

# Import from project modules 
from db_builder import USER_FIELDS, BUSINESS_FIELDS, REVIEW_FIELDS
from analysis import unique_vals


if __name__ == "__main__":
	if platform == 'win32':
		slash = '\\'
	else:
		slash = '/'


	f = open('db_pickled' + slash + 'user_db_pickled')
	users = cPickle.load(f)
	f.close()

	f = open('db_pickled' + slash + 'business_db_pickled')
	businesses = cPickle.load(f)
	f.close()

	f = open('db_pickled' + slash + 'review_db_pickled')
	reviews = cPickle.load(f)
	f.close()


	cities = {}
	states = {}

	for review in reviews:
		user_id = reviews[review]['user_id']
		business_id = reviews[review]['business_id']

		if user_id in cities:
			cities[user_id].append(businesses[business_id]['city'])
			states[user_id].append(businesses[business_id]['state'])
		else:
			cities[user_id] = [businesses[business_id]['city']]
			states[user_id] = [businesses[business_id]['state']]

	two_cities = 0
	multiple_cities = 0

	for user in cities:
		num_cities = len(set(cities[user]))
		if num_cities == 2:
			two_cities+=1
		elif num_cities > 2:
			multiple_cities+=1

	print "Users with reviews in two cities", two_cities
	print "Users with reviews in more than two cities:", multiple_cities

	two_states = 0
	multiple_states = 0

	for user in states:
		num_states = len(set(states[user]))
		if num_states == 2:
			two_states+=1
		elif num_states > 2:
			multiple_states+=1

	print "Users with reviews in two states:", two_states
	print "Users with reviews in more than two states:", multiple_states