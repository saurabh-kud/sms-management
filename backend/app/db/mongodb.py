from pymongo import MongoClient



client = MongoClient('mongodb://mongo:27017')
db = client['sms_service']
collection = db['countryOperator']

