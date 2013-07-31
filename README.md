ndbdict
=======

Google App Engine ndb-memcached dict

# Example

```python

import NdbDict from ndbdict

tel = NdbDict("tel")
tel['guido'] = 4127 # store value in memcache and in ndb table
a = tel['guido'] # get value from memcache else from ndb table

tel.get('guido', 0) # get value without exceptions

```
