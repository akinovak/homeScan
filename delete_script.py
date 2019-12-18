from config import ctx
import urllib3
from multiprocessing import Pool
import random
import sys

collection = sys.argv[1]


def handle_response_code(link, code):
    if 400 <= code <= 500:
        ctx.mongo_adapter.delete_one({'link': link}, collection)
        ctx.mongo_adapter.delete_one({'link': link}, 'test_price')


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
            p = Pool(len(data))
            p.map(send_req, [d['link'] for d in data])

        else:
            break

        last_id = data[-1]['_id']


iterate_collection(10)
