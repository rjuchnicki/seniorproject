# Robert Juchnicki														4/24/15
# 
# Performs analysis and inspection of data accross databases. This script uses 
# the databases built using db_builder.py and saved using the cPickle module.


import cPickle

from sys import platform
from db_builder import USER_FIELDS, BUSINESS_FIELDS, REVIEW_FIELDS


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

	multiple_cities = 0
	for user in cities:
		if len(set(cities[user])) > 1:
			multiple_cities+=1

	print "Users with reviews for businesses in mutliple cities:", multiple_cities

	multiple_states = 0
	for user in states:
		if len(set(states[user])) > 1:
			multiple_states+=1

	print "Users with reviews for businesses in mutliple states:", multiple_states