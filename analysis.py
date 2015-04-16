# Robert Juchnicki                                                     04/15/15
#
# Performs the initial data analysis of the Yelp Dataset Challenge data used to
# inform the recommendation algorithms built in this project. This script uses
# the databases built using db_builder.py and saved using the pickle module.


import numpy as np
import pickle

def db_average(db, field):
	res = 0.0
	n = 0

	for key in db:
		res += db[key][field]
		n += 1

	return res/n


def db_median(db, field):
	return np.median(np.array([db[key][field] for key in db]))


"""print "Number of errors", len(errors)

for el in errors:
	user_db.pop(el, None)

f = open('user_db','w')

print "Average Review Count:", db_average(user_db, 'review_count')
print "Average Stars:", db_average(user_db, 'average_stars')
print "Median Review Count:", db_median(user_db, 'review_count')
print "Median Average Stars:", db_median(user_db, 'average_stars')

print "Number of elite:", elite_users
print "Number of elite errors:", len(errors)"""
