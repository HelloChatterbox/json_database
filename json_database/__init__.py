from json_database.utils import *
from os.path import expanduser, isdir, dirname, exists, isfile, join
from os import makedirs, remove
import json
import logging
from pprint import pprint


LOG = logging.getLogger("JsonDatabase")


class JsonStorage(dict):
    """
        json dict from file.
    """
    def __init__(self, path):
        super().__init__()
        self.path = path
        if self.path:
            self.load_local(self.path)

    def load_local(self, path):
        """
            Load local json file into self.

            Args:
                path (str): file to load
        """
        path = expanduser(path)
        if exists(path) and isfile(path):
            self.clear()
            try:
                config = load_commented_json(path)
                for key in config:
                    self[key] = config[key]
                LOG.debug("Json {} loaded".format(path))
            except Exception as e:
                LOG.error("Error loading json '{}'".format(path))
                LOG.error(repr(e))
        else:
            LOG.debug("Json '{}' not defined, skipping".format(path))

    def clear(self):
        for k in dict(self):
            self.pop(k)

    def reload(self):
        if exists(self.path) and isfile(self.path):
            self.load_local(self.path)
        else:
            LOG.error("Can not reload because file does not exist")
            raise FileNotFoundError

    def store(self, path=None):
        """
            store the json db locally.
        """
        path = path or self.path
        if not path:
            LOG.warning("json db path not set")
            return
        path = expanduser(path)
        if dirname(path) and not isdir(dirname(path)):
            makedirs(dirname(path))
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(self, f, indent=4, ensure_ascii=False)

    def remove(self):
        if isfile(self.path):
            remove(self.path)

    def merge(self, conf):
        merge_dict(self, conf)
        return self


class JsonDatabase(dict):
    def __init__(self, name, path=None):
        super().__init__()
        self.name = name
        self.path = path or join(dirname(__file__), self.name + ".json")
        self.db = JsonStorage(self.path)
        self.db[name] = []
        self.db.load_local(self.path)

    def __repr__(self):
        return str(jsonify_recursively(self))

    def __getitem__(self, item):
        if not isinstance(item, int):
            item_id = self.get_item_id(item)
        else:
            item_id = item
        if item_id < 0 or item_id >= len(self.db[self.name]):
            return None
        return self.db[self.name][item_id]

    def __setitem__(self, key, value):
        self.add_item({key: value})

    def add_item(self, value):
        value = jsonify_recursively(value)
        if value not in self.db[self.name]:
            self.db[self.name] += [value]

    def search_by_key(self, key, fuzzy=False, thresh=0.7, include_empty=False):
        if fuzzy:
            return get_key_recursively_fuzzy(self.db, key, thresh, not include_empty)
        return get_key_recursively(self.db, key, not include_empty)

    def search_by_value(self, key, value, fuzzy=False, thresh=0.7):
        if fuzzy:
            return get_value_recursively_fuzzy(self.db, key, value, thresh)
        return get_value_recursively(self.db, key, value)

    def commit(self):
        """
            store the json db locally.
        """
        self.db.store(self.path)

    def reset(self):
        if not self.path:
            raise ValueError("database path not set")
        self.db.reload()

    def print(self):
        pprint(jsonify_recursively(self))

    def get_item_id(self, item):
        item = jsonify_recursively(item)
        if item not in self.db[self.name]:
            return -1
        return self.db[self.name].index(item)

    def update_item(self, item_id, new_item):
        new_item = jsonify_recursively(new_item)
        self.db[self.name][item_id] = new_item


if __name__ == "__main__":
    db = JsonDatabase("users")
    for user in [
            {"name": "bob", "age": 12},
            {"name": "bobby"},
            {"name": ["joe", "jony"]},
            {"name": "john"},
            {"name": "jones", "age": 35},
            {"name": "jorge"},
            {"name": "joey",  "birthday": "may 12"} ]:
        db.add_item(user)

    print(db[2])
    exit()
    print(db.search_by_key("age"))
    print(db.search_by_key("birth", fuzzy=True))

    print(db.search_by_value("age", 12))
    print(db.search_by_value("name", "jon", fuzzy=True))

    item = db.search_by_value("name", "bobby")[0]
    item_id = db.get_item_id(item)
    db.update_item(item_id, {"name": "don't call me bobby"})

    db.reset()

    db.commit()

    db.print()
