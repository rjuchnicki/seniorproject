# Robert Juchnicki														4/29/15
# 
# Plots histograms and other diagrams for Yelp data using pyplot from the 
# matplotlib module and the numpy module.


import numpy as np
import matplotlib.pyplot as plt
import cPickle

from sys import platform


if __name__ == "__main__":
	if platform == 'win32':
		slash = '\\'
	else:
		slash = '/'


	f = open('histogram_counts' + slash + 'review_ratings_count')
	ratings_count = cPickle.load(f)
	f.close()

	# ratings_count = {
	# 	1: 0,
	# 	2: 0,
	# 	3: 0,
	# 	4: 0,
	# 	5: 0
	# }

	# for review in reviews:
	# 	stars = int(reviews[review]['stars'])
	# 	ratings_count[stars] +=1

	# f = open('review_ratings_count', 'w')
	# cPickle.dump(ratings_count, f)
	# f.close()


	# plot a histogram for star ratings for reviews

	# make the histogram in numpy
	hist, bins = np.histogram(ratings_count.keys(), bins=50, range=(1,5), weights=ratings_count.values())

	# plot histogram hist using matplotlib.pyplot
	width = 4 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)

	# set yticks
	plt.yticks(np.arange(0, 700000, 50000))

	# set labels
	plt.suptitle("Frequency of Star Ratings in Reviews", fontsize=18)
	plt.xlabel("Star Rating", fontsize=14)
	plt.ylabel("Frequency", fontsize=14)

	# save the Review Stars Histogram
	plt.savefig("review_frequency.png")		

	# clear the plot
	plt.clf()
