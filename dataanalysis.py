import pandas as pd
import numpy as np
import ijson

f = open('yelp_json\yelp_academic_dataset_review.json', 'rb')
# for item in ijson.items(f, 'user_id'):
# 	print item

objects = ijson.items(f, 'user_id')
for user_id in objects:
    print user_id


# parser = ijson.parse(f)

# for prefix, event, value in parser:
# 	if prefix == "user_id":
# 	    print value

# 	if prefix == "business_id":
# 	    print value

# close(f)