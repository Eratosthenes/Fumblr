import ast
import random
import falcon
import pickle
import time
import pdb
from fumbler import Fumbler
from multiprocessing import Pool
from collections import defaultdict
from cachetools import LRUCache
import os

# location dictionary is stored as an lru cache to prevent memory from overflowing
loc_d = LRUCache(maxsize=10) # a dictionary with buckets that represent time/loc segments
match_d = defaultdict(list) # dictionary of matches

# create dictionary of friendships 
friend_d = defaultdict(set) 
for rel in eval(open('relationships.json').read()):
    friend_d[rel['from']].add(rel['to'])
    friend_d[rel['to']].add(rel['from']) # assume friendship is always mutual

class Resource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  
        user_id = int(req.get_param('userId'))
        with open('match_d.p', 'rb') as handle:
            match_d = pickle.load(handle)
        
        body = {user_id: match_d[user_id]} if match_d.get(user_id) else {user_id: []}
        resp.body = '{}'.format(body)


    def on_post(self, req, resp):
        """Handles POST requests"""
        resp.status = falcon.HTTP_201
        d = ast.literal_eval(req.stream.read().decode('utf-8')) 
        ts = time.time()
        resp.body = 'userId={}; lat={}; long={}; ts={}'.format(d['userId'], d['lat'], d['lon'], ts)
        print(resp.body)
        
        # populate location dictionary
        h_data = self.granularize(d['lat'], d['lon'], ts) # granularized hashed data
        self.populate_loc_d(h_data, d['userId'])

        # populate match dictionary 
        # shouldn't take too long as long as people have a limited number of friends
        global match_d
        for user in friend_d[d['userId']]:
            if user in loc_d[h_data]:
                print('match found!')
                match_d[d['userId']].append(user)
                match_d[user].append(d['userId'])

        # batch writing for the match dictionary (with a very low threshold)
        # load/combine with previous match data so that we're not overwriting
        if len(match_d) > 1:
            print(match_d)
            with open('match_d.p', 'rb') as handle:
                old_match_d = pickle.load(handle)

            combo_d = {k: v for d in [match_d, old_match_d] for k, v in d.items()}
            with open('match_d.p', 'wb') as handle:
                pickle.dump(combo_d, handle, protocol=pickle.HIGHEST_PROTOCOL)

            match_d.clear() # technically not necessary since it's not referenced elsewhere
            match_d = defaultdict(list)
    
    def populate_loc_d(self, h_data, user_id):
        if not loc_d.get(h_data):
            loc_d[h_data] = set([user_id])
        loc_d[h_data].add(user_id)

    # round these numbers to whatever you like in order to define a match
    def granularize(self, lat, lon, ts):
        lat = "{0:.1f}".format(round(lat, 2))
        lon = "{0:.1f}".format(round(lon, 2))
        ts = "{0:.0f}".format(round(time.time(), -2))
        return hash(' '.join([lat, lon, ts]))

app = falcon.API()
app.add_route('/', Resource())

if __name__=='__main__':
    # create a matching pair of users
    n_users = 10
    users = []
    users.append(Fumbler(1, 10.01, 20.0))
    users.append(Fumbler(2, 10.007, 20.003))

    # create some non-matching users
    for i in range(3, n_users + 1):
        users.append(Fumbler(i))

    # simulate roaming
    p = Pool(len(users))
    p.map(Fumbler.roam, users)

    # get matches for each user after roaming
    for i in range(1, n_users + 1):
        os.system('http :8000 userId=={}'.format(i))

