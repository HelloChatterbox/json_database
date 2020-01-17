from json_database import JsonDatabase

db = JsonDatabase("users")


class User:
    def __init__(self, email, key=None, data=None):
        self.email = email
        self.secret_key = key
        self.data = data

    def __repr__(self):
        return "User:"+self.email


user1 = User("first@mail.net", data={"name": "jonas", "birthday": "12 May"})
user2 = User("second@mail.net", "secret", data={"name": ["joe", "jony"], "age": 12})

# objects will be jsonified here, they will no longer be User objects
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

