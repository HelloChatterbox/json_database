from json_database import JsonDatabase
from os.path import isfile


optional_file_path = "users.db"


if not isfile(optional_file_path):
    print("run database_create.py first!")
    exit()


db = JsonDatabase("users", optional_file_path) # loaded automatically from previous step
users_with_defined_age = db.search_by_key("age")


assert len(users_with_defined_age) == 2

for user in users_with_defined_age:
    print(user["name"], user["age"])

# keys do not need to be an exact match
users = db.search_by_key("birth", fuzzy=True)
for user, conf in users:
    print("matched with confidence", conf)
    print(user["name"], user["birthday"])


# search by key/value pair
users_12years_old = db.search_by_value("age", 12)

for user in users_12years_old:
    assert user["age"] == 12

# fuzzy key/value pair search
jon_users = db.search_by_value("name", "jon", fuzzy=True)
for user, conf in jon_users:
    print(user["name"])
    print("matched with confidence", conf)

# get database item
item = {
            "name": "bobby"
        }
item_id = db.get_item_id(item)

if item_id > 0:
    db.update_item(item_id, {"name": "don't call me bobby"})
else:
    print("item not found in database")

# clear changes since last commit
db.reset()

