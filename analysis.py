# Robert Juchnicki                                                     04/15/15
#
# Performs the initial data analysis of the Yelp Dataset Challenge data used to
# inform the recommendation algorithms built in this project. This script uses
# the databases built using db_builder.py and saved using the pickle module.


import numpy as np
import cPickle

from db_builder import USER_FIELDS, BUSINESS_FIELDS, REVIEW_FIELDS
from sys import platform


# Return the average value over all id's in the database for a numerical value
# stored under field.
def db_average(db, field):
	res = 0.0
	n = 0

	for key in db:
		res += db[key][field]
		n += 1

	return res/n


# Return the value at the n-th percentile value over all id's in the database 
# for a numerical value stored under field. n is a float between 0 and 100
# inclusive.
def db_percentile(db, field, n):
	return np.percentile(np.array([db[key][field] for key in db]), n)


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


# Return a list of the unique values stored under field for entries in db.
def unique_vals(db, field):
	res = []

	for key in db:
		if key[db][field] not in res:
			res.append(key[db][field])

	return res


# Return a list of the unique years stored under date_field for entries in db.
def unique_years(db, date_field):
	res = []

	for key in db:
		if key[db][date_field] not in res:
			res.append(key[db][date_field][0:4])

	return res.sorted()



if __name__ == "__main__":
	if platform == 'win32':
		slash = '\\'
	else:
		slash = '/'

	f = open('db_pickled' + slash + 'user_db_pickled')
	users = cPickle.load(f)
	f.close()


	num_users = len(users.keys())
	print "Number of users in database: ", num_users

	print "Average Review Count: ", db_average(users, 'review_count')
	print "25-th Percentile Review Count: ", db_percentile(users, 'review_count', 25)
	print "50-th Percentile Review Count: ", db_percentile(users, 'review_count', 50)
	print "75-th Percentile Review Count: ", db_percentile(users, 'review_count', 75)

	print "Average Average Star Rating: ", db_average(users, 'average_stars')
	print "25-th Percentile Average Stars: ", db_percentile(users, 'review_count', 25)
	print "50-th Percentile Review Count: ", db_percentile(users, 'review_count', 50)
	print "75-th Percentile Review Count: ", db_percentile(users, 'review_count', 75)

	num_elites = 0
	current_elites = 0
	all_elite_years = []

	yelping_since = {}
	for i in xrange(2004, 2016):
		yelping_since[i] = 0

	for user in users:
		if len(users) > 0:
			num_elites += 1
			all_elite_years = list(set(all_elite_years + users[user]['elite']))

			if 2015 in users[user]['elite']:
				current_elites +=1

			yelping_since[int(users[user]['yelping_since'][0:4])] += 1

	print "Number of users that were elite at some point: ", num_elites
	print "Number of sers who are currently elite users: ", current_elites
	print "All years any users were elite: ", all_elite_years



	# print "Number of elite:", elite_users