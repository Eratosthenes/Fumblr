import random
import time
import os

class Fumbler():
    """
    Simulate Fumble users
    """

    def __init__(self, userId, lat=None, lon=None):
        self.userId = userId
        if lat and lon:
            self.lat, self.lon = lat, lon
        else:
            self.lat, self.lon = self.generate_loc()

    def roam(self):
        """
        Randomly roam around
        """
        while True:
            self.publish_loc()
            self.change_loc()
            time.sleep(1)

    def get_loc(self):
        return self.lat, self.lon

    def generate_loc(self):
        lat = round(random.randint(0, 1) + random.random(), 4)
        lon = round(random.randint(0, 1) + random.random(), 4)
        return lat, lon

    def change_loc(self):
        """
        Move by up to one degree (within bounds)
        """
        self.lat = (self.lat + random.uniform(-1,1)) % 1
        self.lon = (self.lon + random.uniform(-1,1)) % 1

    # in the real world we probably wouldn't send everything all to the same machine/port
    def publish_loc(self):
        url = "http://localhost:8000"
        os.system('http POST \"{}\" userId:={} lon:={} lat:={}'.format(url, self.userId, self.lon, self.lat))

