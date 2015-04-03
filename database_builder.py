# Robert Juchnicki													   04/02/15
#
# Utilities to build and analyze key-value databases for Yelp Dataset Challenge
# datasets. This might be moved into a database system with query support in 
# the future.


import csv
import numpy as np
import pickle

from ast import literal_eval


user_csv_indices = {
	'yelping_since'			:0,
	'compliments.plain'		:1, 
	'review_count'			:2,
	'friends'				:3,
	'compliments.cute'		:4,
	'compliments.writer'	:5,
	'fans'					:6,
	'compliments.note'		:7,
	'type'					:8, 
	'compliments.hot'		:9,
	'compliments.cool'		:10,
	'compliments.profile'	:11,
	'average_stars'			:12,
	'compliments.more'		:13,
	'elite'					:14,
	'name'					:15,
	'user_id'				:16,
	'votes.cool'			:17,
	'compliments.list'		:18,
	'votes.funny'			:19,
	'compliments.photos'	:20,
	'compliments.funny'		:21,
	'votes.useful'			:22
}


def create_db(filename, csv_indices, db_key, fields):
	db = {}

	f = open(filename, 'rt')

	try:
		reader = csv.reader(f)
		for row in reader:
			row_key = csv_indices[db_key]
			item = row[row_key]

			db[item] = {}

			for field in fields:
				db[item][field] = row[csv_indices[field]]

	finally:
		f.close()

	return db


def db_average(db, field):
	res = 0.0
	n = 0

	for key in db:
		res += db[key][field]
		n += 1

	return res/n


def db_median(db, field):
	return np.median(np.array([db[key][field] for key in db]))


# {user_id: {'yelping_since':_, 'review_count':_, 'average_stars':_, 'elite':_, 'name':_}...}
user_fields = ['yelping_since', 'review_count', 'average_stars', 'elite', 'name']
user_db = create_db('yelp_csv\yelp_academic_dataset_user.csv', user_csv_indices, 'user_id', user_fields)


elite_users = 0
errors = []
fields = ['elite', 'review_count', 'average_stars']

for key in user_db:
	try:
		for field in fields:
			user_db[key][field] = literal_eval(user_db[key][field])

		if len(user_db[key]['elite']) > 0:
			elite_users+=1
	except:
		errors.append(key)


print "Number of errors", len(errors)

for el in errors:
	user_db.pop(el, None)

f = open('user_db','w')
user_db = 


print "Average Review Count:", db_average(user_db, 'review_count')
print "Average Stars:", db_average(user_db, 'average_stars')
print "Median Review Count:", db_median(user_db, 'review_count')
print "Median Average Stars:", db_median(user_db, 'average_stars')

# print "Number of elite:", elite_users
# print "Number of elite errors:", len(errors)
