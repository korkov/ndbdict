from google.appengine.ext import ndb
from google.appengine.api import memcache

class NdbDictModel(ndb.Model):
    key = ndb.StringProperty()
    data = ndb.JsonProperty()

storage = {}

class NdbStorage:
    def __init__(self, key):
        self.key = key

    def _req(self):
        return NdbDictModel.query(NdbDictModel.key == self.key).get()

    def get(self):
        if self.key in storage:
            return storage[self.key]

        entry = self._req()
        storage[self.key] = entry.data if entry else {}
        return storage[self.key]

    def set(self, data):
        storage[self.key] = data

        entry = self._req()
        if not entry:
            entry = NdbDictModel(key=self.key)
        entry.data = data
        entry.put()

class NdbDict:
    def __init__(self, id):
        self.memcache_id = "NDBDICT_"+id
        self.storage = NdbStorage(self.memcache_id)

    def _data(self):
        d = memcache.get(self.memcache_id)
        if not d:
            d = self.storage.get()
            memcache.set(self.memcache_id, d)
        return d

    def get(self, key, default=None):
        return self._data().get(key, default)

    def set(self, key, data):
        d = memcache.get(self.memcache_id)
        if not d:
            d = self.storage.get()
        d[key] = data
        memcache.set(self.memcache_id, d)
        self.storage.set(d)

    def __getitem__(self, key):
        return self._data()[key]

    def __setitem__(self, key, data):
        return self.set(key, data)
