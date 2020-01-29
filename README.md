# Json Database

Python dict based database with persistence and search capabilities

For those times when you need something simple and sql is overkill


## Features

- pure python
- save and load from file
- search recursively by key and key/value pairs
- fuzzy search
- supports arbitrary objects
- supports comments in saved files

## Install

```bash
pip install json_database
```

## Usage


### JsonStorage

Sometimes you need persistent dicts that you can save and load from file

```python
from json_database import JsonStorage
from os.path import exists

save_path = "my_dict.conf"

my_config = JsonStorage(save_path)

my_config["lang"] = "pt"
my_config["secondary_lang"] = "en"
my_config["email"] = "jarbasai@mailfence.com"

# my_config is a python dict
assert isinstance(my_config, dict)

# save to file
my_config.store()

my_config["lang"] = "pt-pt"

# revert to previous saved file
my_config.reload()
assert my_config["lang"] == "pt"

# clear all fields
my_config.clear()
assert my_config == {}

# load from a specific path
my_config.load_local(save_path)
assert my_config == JsonStorage(save_path)

# delete stored file
my_config.remove()
assert not exists(save_path)

# keep working with dict in memory
print(my_config)
```

### JsonDatabase

Ever wanted to search a dict?

Let's create a dummy database with users

```python
from json_database import JsonDatabase

db_path = "users.db"

with JsonDatabase("users", db_path) as db:
    # add some users to the database

    for user in [
        {"name": "bob", "age": 12},
        {"name": "bobby"},
        {"name": ["joe", "jony"]},
        {"name": "john"},
        {"name": "jones", "age": 35},
        {"name": "joey", "birthday": "may 12"}]:
        db.add_item(user)
        
    # pretty print database contents
    db.print()


# auto saved when used with context manager
# db.commit()


```
         
search entries by key

```python
from json_database import JsonDatabase

db_path = "users.db"

db = JsonDatabase("users", db_path) # load db created in previous example

# search by exact key match
users_with_defined_age = db.search_by_key("age")

for user in users_with_defined_age:
    print(user["name"], user["age"])
    
# fuzzy search
users = db.search_by_key("birth", fuzzy=True)
for user, conf in users:
    print("matched with confidence", conf)
    print(user["name"], user["birthday"])
```

search by key value pair

```python
# search by key/value pair
users_12years_old = db.search_by_value("age", 12)

for user in users_12years_old:
    assert user["age"] == 12

# fuzzy search
jon_users = db.search_by_value("name", "jon", fuzzy=True)
for user, conf in jon_users:
    print(user["name"])
    print("matched with confidence", conf)
    # NOTE that one of the users has a list instead of a string in the name, it also matches
```

updating an existing entry

```python
# get database item
item = {"name": "bobby"}

item_id = db.get_item_id(item)

if item_id >= 0:
    new_item = {"name": "don't call me bobby"}
    db.update_item(item_id, new_item)
else:
    print("item not found in database")

# clear changes since last commit
db.reset()
```

You can save arbitrary objects to the database

```python
from json_database import JsonDatabase

db = JsonDatabase("users", "~/databases/users.json")


class User:
    def __init__(self, email, key=None, data=None):
        self.email = email
        self.secret_key = key
        self.data = data

user1 = User("first@mail.net", data={"name": "jonas", "birthday": "12 May"})
user2 = User("second@mail.net", "secret", data={"name": ["joe", "jony"], "age": 12})

# objects will be "jsonified" here, they will no longer be User objects
# if you need them to be a specific class use some ORM lib instead (SQLAlchemy is great)
db.add_item(user1)
db.add_item(user2)

# search entries with non empty key
print(db.search_by_key("secret_key"))

# search in user provided data
print(db.search_by_key("birth", fuzzy=True))

# search entries with a certain value
print(db.search_by_value("age", 12))
print(db.search_by_value("name", "jon", fuzzy=True))

```