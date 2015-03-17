from pymongo import MongoClient
from pymongo import Connection

mongo_lst = []
client = MongoClient()
# app.mongo_table = client[db_name][table_name]
db = client['shoes']
table = db['category']
count2 = 0
# print db.collection_names()
for collection in db.collection_names():
	# cursor= db[collection].find_one({'company': 'barneys', 'product_id': '158585078'}, {'price': "{'$exists' :True}", 'designer_name':  "{'$exists' :True}", 'description':  "{'$exists' :True}", 'product_link':  "{'$exists' :True}"});
	cursor = db[collection].find({'product_link': u'http://shop.nordstrom.com/s/giuseppe-zanotti-sharon-peep-toe-platform-pump-women/3871510?origin=category'});
	# if cursor != None and cursor['product_id'] not in mongo_lst:
	if cursor.count>2:
		for info in cursor:	
			if(count2==0):
				mongo_lst.append(info)
			count2+=1

print mongo_lst



