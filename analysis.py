# Robert Juchnicki                                                     04/15/15
#
# Performs the initial data analysis of the Yelp Dataset Challenge data used to
# inform the recommendation algorithms built in this project. This script uses
# the databases built using db_builder.py and saved using the pickle module.


import numpy as np
import pickle


# Return the average value over all id's in the database for a numerical value
# stored under field.
def db_average(db, field):
	res = 0.0
	n = 0

	for key in db:
		res += db[key][field]
		n += 1

	return res/n


# Return the median value over all id's in the database for a numerical value
# stored under field.
def db_median(db, field):
	return np.median(np.array([db[key][field] for key in db]))


# Return the min value over all id's in the database for a numerical value
# stored under field. Assume all values are positive.
def db_max(db, field):
	res = 0

	for item in db:
		if db[item][field] > res:
			res = db[item][field]


# Return the max value over all id's in the database for a numerical value 
# stored under field.
def db_min(db, field):
	keys = db.keys()
	n = len(keys)
	res = db[keys[0]][field]

	for i in xrange(1, n):
		if db[keys[i]][field] < res:
			res = db[keys[i]][field]

	return res



if __name__ == "__main__":
	"""print "Average Review Count:", db_average(user_db, 'review_count')
	print "Average Stars:", db_average(user_db, 'average_stars')
	print "Median Review Count:", db_median(user_db, 'review_count')
	print "Median Average Stars:", db_median(user_db, 'average_stars')

	print "Number of elite:", elite_users
	print "Number of elite errors:", len(errors)"""