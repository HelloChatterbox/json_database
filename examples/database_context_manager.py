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

# auto saved