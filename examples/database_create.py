from json_database import JsonDatabase

optional_file_path = "users.db"

db = JsonDatabase("users", optional_file_path)

# add some users to the database

for user in [
    {"name": "bob", "age": 12},
    {"name": "bobby"},
    {"name": ["joe", "jony"]},
    {"name": "john"},
    {"name": "jones", "age": 35},
    {"name": "jorge"},  # NOTE: no duplicate entries allowed
    {"name": "jorge"},  # this one will be ignored
    {"name": "joey", "birthday": "may 12"}]:
    db.add_item(user)

# pretty print database contents
db.print()

# save it
db.commit()