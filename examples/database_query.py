from json_database import JsonStorageXDG
from json_database.search import Query
from pprint import pprint


db = JsonStorageXDG("dust")
q = Query(db).bellow_or_equal("duration", 130).build()

#pprint(q)

q = Query(db).above_or_equal("rating", 3).build()

#pprint(q)

q = Query(db).value_contains_token("title", "noir", ignore_case=True).build()

pprint(q)