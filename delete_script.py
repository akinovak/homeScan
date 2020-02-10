from datetime import datetime

from config import ctx
import urllib3
from multiprocessing import Pool, Manager
import random
import sys
from adapters.mongo_adapter import MongoAdapter

collection = sys.argv[1]

shared_delete_link_list = Manager().list()

def handle_response_code(link, code):
    if 400 <= code <= 500:
        global shared_delete_link_list
        shared_delete_link_list.append(link)



def send_req(link):
    user_agent = {'user-agent': random.choice(ctx.user_agents)}
    http = urllib3.PoolManager(2, headers=user_agent)
    r = http.request(
        'GET',
        link,
        preload_content=False)
    r.release_conn()
    handle_response_code(link, r.status)


def iterate_collection(batch_size):
    last_id = None
    while True:
        if last_id is None:
            cursor = ctx.mongo_adapter.find({}, collection, limit=batch_size)
        else:
            cursor = ctx.mongo_adapter.find({'_id': {'$gt': last_id}}, collection, limit=batch_size)

        data = [x for x in cursor]

        if data:

            start_time = datetime.now()
            #for d in data:
            #   send_req(d['link'])
            p = Pool(len(data))
            p.map(send_req, [d['link'] for d in data])
            end_time = datetime.now()
            diff = int((end_time - start_time).total_seconds())
            print(diff)
            for link in shared_delete_link_list:
                print('Deleting {} ...'.format(link))
                ctx.mongo_adapter.delete_one({'link': link}, collection)
                ctx.mongo_adapter.delete_one({'link': link}, 'test_cene')
                shared_delete_link_list.remove(link)

        else:
            break

        last_id = data[-1]['_id']


iterate_collection(10)
