# Robert Juchnicki                                                      04/02/15
#
# Script to build key-value databases from Yelp Dataset Challenge datasets stored
# in CSV format. Databases are saved using the cPickle module.The data might be
# moved into a database system with built-in query support in the future.


import os
import csv
import cPickle

from sys import platform
from ast import literal_eval


# Dictionary mapping user database fields to CSV columns
USER_CSV_INDICES = {
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

# Dictionary mapping review database fields to CSV columns
REVIEW_CSV_INDICES = {
	'user_id' 		:0,
	'review_id' 	:1,
	'text' 			:2,
	'votes.cool' 	:3,
	'business_id' 	:4,
	'votes.funny' 	:5,
	'stars' 		:6,
	'date'			:7,
	'type'			:8,
	'votes.useful'	:9 
}

# Dictionary mapping business database fields to CSV columns
BUSINESS_CSV_INDICES = {
	'attributes.Accepts Credit Cards':40,
	'attributes.Accepts Insurance':82,
	'attributes.Ages Allowed':55,
	'attributes.Alcohol':12,
	'attributes.Ambience.casual':87,
	'attributes.Ambience.classy':13,
	'attributes.Ambience.divey':0,
	'attributes.Ambience.hipster':26,
	'attributes.Ambience.intimate':69,
	'attributes.Ambience.romantic':101,
	'attributes.Ambience.touristy':17,
	'attributes.Ambience.trendy':56,
	'attributes.Ambience.upscale':104,
	'attributes.Attire':96,
	'attributes.BYOB':7,
	'attributes.BYOB/Corkage':27,
	'attributes.By Appointment Only':88,
	'attributes.Caters':68,
	'attributes.Coat Check':73,
	'attributes.Corkage':18,
	'attributes.Delivery':57,
	'attributes.Dietary Restrictions.dairy-free':30,
	'attributes.Dietary Restrictions.gluten-free':64,
	'attributes.Dietary Restrictions.halal':52,
	'attributes.Dietary Restrictions.kosher':89,
	'attributes.Dietary Restrictions.soy-free':84,
	'attributes.Dietary Restrictions.vegan':1,
	'attributes.Dietary Restrictions.vegetarian':92,
	'attributes.Dogs Allowed':90,
	'attributes.Drive-Thru':91,
	'attributes.Good For Dancing':36,
	'attributes.Good For Groups':98,
	'attributes.Good For Kids':43,
	'attributes.Good For.breakfast':33,
	'attributes.Good For.brunch':20,
	'attributes.Good For.dessert':50,
	'attributes.Good For.dinner':32,
	'attributes.Good For.latenight':71,
	'attributes.Good For.lunch':42,
	'attributes.Good for Kids':79,
	'attributes.Hair Types Specialized In.africanamerican':5,
	'attributes.Hair Types Specialized In.asian':38,
	'attributes.Hair Types Specialized In.coloring':48,
	'attributes.Hair Types Specialized In.curly':97,
	'attributes.Hair Types Specialized In.extensions':76,
	'attributes.Hair Types Specialized In.kids':6,
	'attributes.Hair Types Specialized In.perms':102,
	'attributes.Hair Types Specialized In.straightperms':28,
	'attributes.Happy Hour':2,
	'attributes.Has TV':85,
	'attributes.Music.background_music':31,
	'attributes.Music.dj':83,
	'attributes.Music.jukebox':103,
	'attributes.Music.karaoke':35,
	'attributes.Music.live':29,
	'attributes.Music.playlist':70,
	'attributes.Music.video':51,
	'attributes.Noise Level':94,
	'attributes.Open 24 Hours':100,
	'attributes.Order at Counter':4,
	'attributes.Outdoor Seating':11,
	'attributes.Parking.garage':34,
	'attributes.Parking.lot':15,
	'attributes.Parking.street':25,
	'attributes.Parking.valet':44,
	'attributes.Parking.validated':80,
	'attributes.Payment Types.amex':21,
	'attributes.Payment Types.cash_only':49,
	'attributes.Payment Types.discover':62,
	'attributes.Payment Types.mastercard':14,
	'attributes.Payment Types.visa':66,
	'attributes.Price Range':72,
	'attributes.Smoking':95,
	'attributes.Take-out':45,
	'attributes.Takes Reservations':53,
	'attributes.Waiter Service':24,
	'attributes.Wheelchair Accessible':63,
	'attributes.Wi-Fi':59,
	'hours.Friday.close':41,
	'hours.Friday.open':8,
	'hours.Monday.close':75,
	'hours.Monday.open':23,
	'hours.Saturday.close':78,
	'hours.Saturday.open':54,
	'hours.Sunday.close':86,
	'hours.Sunday.open':81,
	'hours.Thursday.close':47,
	'hours.Thursday.open':3,
	'hours.Tuesday.close':77,
	'hours.Tuesday.open':19,
	'hours.Wednesday.close':58,
	'hours.Wednesday.open':93,
	'business_id':16,
	'categories':9,
	'city':61,
	'full_address':46,
	'latitude':10,
	'longitude':74,
	'name':22,
	'neighborhoods':99,
	'open':60,
	'review_count':37,
	'stars':65,
	'state':39,
	'type':67
}


# Fields stored in the dictionary databases
USER_FIELDS = ['yelping_since', 'review_count', 'average_stars', 'elite', 'name']
BUSINESS_FIELDS = BUSINESS_CSV_INDICES.keys()
REVIEW_FIELDS = review_fields = ['user_id', 'review_id', 'business_id', 'stars', 'date']


# Open CSV file with name filename, read through it, and return a dictionary
# whose keys are specified by db_key. The values are dictionaries whose keys
# are the elements of fields, and whose values are drawn from the CSV's rows
# using the indices specified in csv_indices.
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

	db.pop(db_key)	# remove entry of labels

	return db


# Save the database to file with name filename using cPickle serialization
def save_db(db, filename):
	f = open(filename, 'w')
	cPickle.dump(db, f)
	f.close()


# Convert the data stored for each field in fields from a string to its 
# original data type for each entry in db.
def strings_to_datatypes(db, fields):
	errors = []

	for key in db:
		try:
			for field in fields:
				db[key][field] = literal_eval(db[key][field])
		except:
			errors.append(key)

	for elt in errors:
		db.pop(elt)



if __name__ == "__main__":
	try: 
		os.makedirs('db_pickled')
	except OSError:
   		if not os.path.isdir('db_pickled'):
			raise

	if platform == 'win32':
		slash = '\\'
	else:
		slash = '/'


	# Form the key-value database of users
	# The database is created as a dictionary in the following form:
	# {
	# 	user_id1: {'yelping_since':'YYYY-MM', 'review_count':_, 'average_stars':_, 'elite':[year1, year2, ...], 'name':_}, 
	# 	user_id2: {...} 
	# 	...
	# }
	user_db = create_db('yelp_csv' + slash + 'yelp_academic_dataset_user.csv', USER_CSV_INDICES, 'user_id', USER_FIELDS)
	strings_to_datatypes(user_db, ['elite', 'review_count', 'average_stars'])
	save_db(user_db, 'db_pickled' + slash + 'user_db_pickled')
	user_db.clear()


	# Form the key-value database of businesses
	# {busineess_id: {'field1':_, 'field2':_, ...}, ...}
	business_db = create_db('yelp_csv' + slash + 'yelp_academic_dataset_business.csv', BUSINESS_CSV_INDICES, 'business_id', BUSINESS_FIELDS)
	strings_to_datatypes(business_db, ['categories', 'review_count', 'stars', 'longitude', 'latitude', 'neighborhoods'])
	save_db(business_db, 'db_pickled' + slash + 'business_db_pickled')
	business_db.clear()


	# Form the key-value database of review attributes
	# {review_id: {field1:_, field2:_, ...}, ...}
	review_db = create_db('yelp_csv' + slash + 'yelp_academic_dataset_review.csv', REVIEW_CSV_INDICES, 'review_id', REVIEW_FIELDS)
	strings_to_datatypes(review_db, ['stars'])
	save_db(review_db, 'db_pickled' + slash + 'review_db_pickled')
	review_db.clear()
