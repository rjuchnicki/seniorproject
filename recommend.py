# Robert Juchnicki														4/28/15
# 
# Engine to build recommenders for businesses in the Yelp Dataset Challenge 
# Data using user-based and item-based approaches. 


import numpy as np
import cPickle

from sys import platform


if __name__ == "__main__":
	if platform == 'win32':
		slash = '\\'
	else:
		slash = '/'