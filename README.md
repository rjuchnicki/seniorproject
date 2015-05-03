# seniorproject

This repository contains scripts for my CS & Math senior project. These scripts
build recommendation systems for businesses from Yelp Dataset Challenge data.
The code requires Python 2.7, NumPy, and Matplotlib.



Basic Setup
-----------
In order to run the analyses and recommendations contained in this repository, 
you must first download the Yelp Dataset Challenge data from: 
http://www.yelp.com/dataset_challenge and run `json_to_csv_converter.py` from 
https://github.com/Yelp/dataset-examples on the json datasets. Once this is 
completed, make sure the files are named 
yelp_academic_datset_[users | reviews | businesses] and put into a directory
named yelp_csv. Now, you will be able to run `db_builder.py` to create and save 
the databases in a Python object format. 

Analysis and Plot Creation
--------------------------
Once the databases are made, you can output basic analyses by running
`analysis.py` and `cross_analysis.py`. You can also save some basic plots as `.png` 
images by running `plot.py`.

Recommendation Engine
---------------------
The recommendation engine is run in two parts. First, `initialize_recommenders.py` is 
run to build the backbone of the recommenders used to make recommendations. It saves results
needed to run `recommend.py`, which creates recommendations of businesses for users state
by state and computes accuracy measurements for the recommendations produced.
