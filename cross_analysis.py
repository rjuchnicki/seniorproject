# Robert Juchnicki														4/24/15
# 
# Performs analysis and inspection of data accross databases. This script uses 
# the databases built using db_builder.py and saved using the pickle module.


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