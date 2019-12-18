import urllib3
from datetime import datetime
from pymongo import MongoClient
from multiprocessing import Pool


# def send_req(link):
#     user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
#     http = urllib3.PoolManager(2, headers=user_agent)
#     r = http.request(
#         'GET',
#         link,
#         preload_content=False)
#     r.release_conn()
#     print(r.status)


client = MongoClient('localhost', 27017)
db = client['stanovi']
stanovi = db['stanovi']
test = db['test']
test_price = db['test_cene']

coursors = test_price.find({})

for coursor in coursors:
    print(coursor['istorija'])

# start_time = datetime.now()
# last_id = None
# while True:
#     if last_id is None:
#         cursor = test_price.find().limit(10)
#     else:
#         cursor = test_price.find({'_id': {'$gt': last_id}}).limit(10)
#
#     data = [x for x in cursor]
#
#     if data:
#         p = Pool(len(data))
#         p.map(send_req, [d['link'] for d in data])
#
#     else:
#         break
#
#     last_id = data[-1]['_id']

# end = datetime.now()
# diff = int((end - start_time).total_seconds())
# print(diff)

