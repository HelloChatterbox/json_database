from json_database.utils import *
from json_database.exceptions import InvalidItemID, DatabaseNotCommitted
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
            raise DatabaseNotCommitted

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

    def __len__(self):
        return len(self.db[self.name])

    def __getitem__(self, item):
        if not isinstance(item, int):
            try:
                item_id = int(item)
            except Exception as e:
                item_id = self.get_item_id(item)
                if item_id < 0:
                    raise InvalidItemID
        else:
            item_id = item
        if item_id >= len(self.db[self.name]):
            raise InvalidItemID
        return self.db[self.name][item_id]

    def __setitem__(self, item_id, value):
        if not isinstance(item_id, int) or item_id >= len(self):
            raise InvalidItemID
        else:
            self.update_item(item_id, value)

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
