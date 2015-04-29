# Robert Juchnicki														4/29/15
# 
# Plots some histograms and other diagrams for Yelp data using pyplot from the 
# matplotlib module.


import numpy as np
import matplotlib.pyplot as plt
import cPickle

from sys import platform


if __name__ == "__main__":
	if platform == 'win32':
		slash = '\\'
	else:
		slash = '/'

	f = open('ratings_count')
	ratings_count = cPickle.load(f)
	f.close()


	"""ratings_count = {
		1: 0,
		2: 0,
		3: 0,
		4: 0,
		5: 0
	}

	for review in reviews:
		stars = int(reviews[review]['stars'])
		ratings_count[stars] +=1"""

	hist, bins = np.histogram(ratings_count.keys(), bins=50, range=(1,5), weights=ratings_count.values())
	width = 4 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	plt.yticks(np.arange(0, 650000, 50000))
	plt.show()