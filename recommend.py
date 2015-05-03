# Robert Juchnicki                                                       5/2/15
# 
# Engine to computer recommendations for businesses in the Yelp Dataset 
# Challenge Data using user-based and item-based approaches. 
# Run after initialize_recommenders.py


import cPickle
import random

from sys import platform


# Return a random subset of elements in l of size k. Uses final algorithm 
# presented on http://propersubset.com/2010/04/choosing-random-elements.html
def random_subset(l, k):
    res = []
    n = 0

    for item in l:
        n += 1
        if len(res) < k:
            res.append(item)
        else:
            s = int(random.random() * n)
            if s < k:
                res[s] = item

    return res


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
		random_correct = 0

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

			if len(user_businesses) >= 3:
				for i in xrange(0, 3):
					bus_index = labels.index(user_businesses[i][0])
					row = matrix[bus_index]
					recs = sorted(range(len(row)), key = lambda x: row[x])[-3:]

					for r in recs:
						recommendations.append(labels[r])
			else:
				for i in xrange(0, len(user_businesses)):
					bus_index = labels.index(user_businesses[i][0])
					row = matrix[bus_index]
					recs = sorted(range(len(row)), key = lambda x: row[x])[-3:]

					for r in recs:
						recommendations.append(labels[r])


			# See if any recommendations match a business the user has been to
			for r in recommendations:
				for b in user_businesses:
					if r == b[0]:
						correct_recommendations += 1
						break


			# See how well a random choice performs
			random_rec = random_subset(labels, len(recommendations))

			for r in random_rec:
				for b in user_businesses:
					if r == b[0]:
						random_correct += 1
						break


		percent_correct = float(correct_recommendations) / float(num_users)
		random_percent = float(random_correct) / float(num_users)
		print percent_correct * 100, "% success rate for", state
		print random_percent *100, "% success rate for random choices for", state, '\n'
