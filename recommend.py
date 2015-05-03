# Robert Juchnicki                                                       5/2/15
# 
# Engine to computer recommendations for businesses in the Yelp Dataset 
# Challenge Data using user-based and item-based approaches. 
# Run after initialize_recommenders.py


import cPickle

from sys import platform


if __name__ == "__main__":
	if platform == 'win32':
		slash = '\\'
	else:
		slash = '/'


	# Load the user, business, and review databases
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


	# States for which recommendations will be made for users
	states = ['IL', 'WI', 'PA', 'NC']


	for state in states:
		correct_recommendations = 0

		# Load the similarity matrix for state and labels for the indices
		f = open('similarity_matrices' + slash + 'matrix_' + state)
		matrix = cPickle.load(f)
		f.close()

		f = open('similarity_matrices' + slash + 'labels_' + state)
		labels = cPickle.load(f)
		f.close()

		n = len(labels)


		# Gather all the users in state
		users_in_state = []
		for user in users:
			if users[user]['current_state'] == state:
				users_in_state.append(user)

		num_users = len(users_in_state)


		# Compute a recommendation for each user in state
		for user in users_in_state:
			user_reviews = users[user]['reviews']

			# Get all the business the user has reviewed in state and store 
			# tuples of business_id and rating in user_businesses
			user_businesses = []
			for review in user_reviews:
				business_id = reviews[review]['business_id']

				if businesses[business_id]['state'] == state:
					rating = reviews[review]['stars']

					if business_id not in user_businesses:
						user_businesses.append((business_id, rating))

			user_businesses.sort(key = lambda x: x[1])
			user_businesses = user_businesses[::-1]


			# Compute 3 recommended businesses for user
			recommendations = []

			if len(user_businesses) > 3:
				for i in xrange(0, 3):
					bus_index = labels.index(user_businesses[i][0])
					rec = 0

					for j in xrange(0, n):
						if matrix[bus_index][j] > matrix[bus_index][rec]:
							rec = j

					recommendations.append(labels[j])
			else:
				num_users -= 1


			# See if any recommendations match a business the user has been to
			for r in recommendations:
				if r in user_businesses:
					correct_recommendations += 1
					break


		percent_correct = float(correct_recommendations) / float(num_users)
		print percent_correct, "%% success rate for", state, '\n'
