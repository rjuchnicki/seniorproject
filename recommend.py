# Robert Juchnicki														4/28/15
# 
# Engine to build recommenders for businesses in the Yelp Dataset Challenge 
# Data using user-based and item-based approaches. 


import numpy as np
import cPickle

from sys import platform
from datetime import date


# Return the key in a dictionary with the max value.
def key_for_max_value(d): 
    values = list(d.values())
    keys = list(d.keys())

    return keys[values.index(max(values))]

# Returns the user's current state. Looks at the dates and locations of all
# business the user has reviewed to compute the result. 
def determine_state(user_id, reviews, businesses):
	review_info = []

	for review in reviews:
		if reviews[review]['user_id'] == user_id:
			business_id = reviews[review]['business_id']
			date_string = reviews[review]['date']
			day = date(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:]))

			review_info.append((review, day, businesses[business_id]['state']))

	review_info.sort(key = lambda x: x[1])
	n = len(review_info)

	states = {}
	for i in xrange(n/2,n):
		state = review_info[i][2]
		if state in states:
			states[state] += 1
		else: 
			states[state] = 1

	return key_for_max_value(states)


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


	for user in users:
		print determine_state(user, reviews, businesses)