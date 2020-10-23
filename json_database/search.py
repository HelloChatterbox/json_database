from json_database.utils import fuzzy_match, match_one
from json_database import JsonDatabase, JsonStorageXDG


class Query:
    def __init__(self, db):
        if isinstance(db, JsonDatabase):
            self.result = [a for _, a in db.db.items()]
        else:
            self.result = [a for _, a in db.items()]

    def contains_key(self, key, fuzzy=False, thresh=0.7):
        if fuzzy:
            after = []
            for e in self.result:
                filter = True
                for k in e:
                    score = fuzzy_match(k, key)
                    if score < thresh:
                        continue
                    filter = False
                if not filter:
                    after.append(e)
            self.result = after
        else:
            self.result = [a for a in self.result if a.get(key)]
        return self

    def contains_value(self, key, value, fuzzy=False, thresh=0.75):
        self.contains_key(key)
        if fuzzy:
            after = []
            for e in self.result:
                if isinstance(e[key], str):
                    score = fuzzy_match(value, e[key])
                    if score > thresh:
                        after.append(e)
                elif isinstance(e[key], list) or isinstance(e[key], dict):
                    v, score = match_one(value, e[key])
                    if score < thresh:
                        continue
                    after.append(e)
            self.result = after
        else:
            self.result = [a for a in self.result if value in a[key]]
        return self

    def value_contains(self, key, value, ignore_case=False):
        self.contains_key(key)
        if ignore_case:
            after = []
            value = str(value).lower()
            for e in self.result:
                if isinstance(e[key], str):
                    if value in e[key].lower():
                        after.append(e)
                elif isinstance(e[key], list):
                    if value in [str(_).lower() for _ in e[key]]:
                        after.append(e)
                elif isinstance(e[key], dict):
                    if value in [str(_).lower() for _ in e[key].keys()]:
                        after.append(e)
            self.result = after
        else:
            self.result = [e for e in self.result if value in e[key]]
        return self

    def value_contains_token(self, key, value, ignore_case=False):
        self.contains_key(key)
        after = []
        value = str(value)
        for e in self.result:
            if isinstance(e[key], str):
                if ignore_case:
                    if value.lower() in e[key].lower().split(" "):
                        after.append(e)
                else:
                    if value in e[key].split(" "):
                        after.append(e)
            elif value in e[key]:
                after.append(e)
        self.result = after
        return self

    def equal(self, key, value):
        self.contains_key(key)
        self.result = [a for a in self.result if a[key] == value]
        return self

    def bellow(self, key, value):
        self.contains_key(key)
        self.result = [a for a in self.result if a[key] < value]
        return self

    def above(self, key, value):
        self.contains_key(key)
        self.result = [a for a in self.result if a[key] > value]
        return self

    def bellow_or_equal(self, key, value):
        self.contains_key(key)
        self.result = [a for a in self.result if a[key] <= value]
        return self

    def above_or_equal(self, key, value):
        self.contains_key(key)
        self.result = [a for a in self.result if a[key] >= value]
        return self

    def in_range(self, key, min_value, max_value):
        self.contains_key(key)
        self.result = [a for a in self.result if min_value < a[key] < max_value]
        return self

    def all(self):
        return self

    def build(self):
        return self.result


