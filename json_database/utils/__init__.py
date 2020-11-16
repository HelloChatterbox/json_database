import json
from difflib import SequenceMatcher


def fuzzy_match(x, against):
    """Perform a 'fuzzy' comparison between two strings.
    Returns:
        float: match percentage -- 1.0 for perfect match,
               down to 0.0 for no match at all.
    """
    return SequenceMatcher(None, x, against).ratio()


def match_one(query, choices):
    """
        Find best match from a list or dictionary given an input

        Arguments:
            query:   string to test
            choices: list or dictionary of choices

        Returns: tuple with best match, score
    """
    if isinstance(choices, dict):
        _choices = list(choices.keys())
    elif isinstance(choices, list):
        _choices = choices
    else:
        raise ValueError('a list or dict of choices must be provided')

    best = (_choices[0], fuzzy_match(query, _choices[0]))
    for c in _choices[1:]:
        score = fuzzy_match(query, c)
        if score > best[1]:
            best = (c, score)

    if isinstance(choices, dict):
        return (choices[best[0]], best[1])
    else:
        return best


def merge_dict(base, delta):
    """
        Recursively merging configuration dictionaries.

        Args:
            base:  Target for merge
            delta: Dictionary to merge into base
    """

    for k, dv in delta.items():
        bv = base.get(k)
        if isinstance(dv, dict) and isinstance(bv, dict):
            merge_dict(bv, dv)
        else:
            base[k] = dv
    return base


def load_commented_json(filename):
    """ Loads an JSON file, ignoring comments

    Supports a trivial extension to the JSON file format.  Allow comments
    to be embedded within the JSON, requiring that a comment be on an
    independent line starting with '//' or '#'.

    NOTE: A file created with these style comments will break strict JSON
          parsers.  This is similar to but lighter-weight than "human json"
          proposed at https://hjson.org

    Args:
        filename (str):  path to the commented JSON file

    Returns:
        obj: decoded Python object
    """
    with open(filename) as f:
        contents = f.read()

    return json.loads(uncomment_json(contents))


def uncomment_json(commented_json_str):
    """ Removes comments from a JSON string.

    Supporting a trivial extension to the JSON format.  Allow comments
    to be embedded within the JSON, requiring that a comment be on an
    independent line starting with '//' or '#'.

    Example...
       {
         // comment
         'name' : 'value'
       }

    Args:
        commented_json_str (str):  a JSON string

    Returns:
        str: uncommented, legal JSON
    """
    lines = commented_json_str.splitlines()
    # remove all comment lines, starting with // or #
    nocomment = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("//") or stripped.startswith("#"):
            continue
        nocomment.append(line)

    return " ".join(nocomment)


def is_jsonifiable(thing):
    if not isinstance(thing, dict):
        if isinstance(thing, str):
            try:
                json.loads(thing)
                return True
            except:
                pass
        else:
            try:
                thing.__dict__
                return True
            except:
                pass
        return False
    return True


def get_key_recursively(search_dict, field, filter_None=True):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    if not is_jsonifiable(search_dict):
        raise ValueError("unparseable format")
    fields_found = []

    for key, value in search_dict.items():
        if value is None and filter_None:
            continue
        if key == field:
            fields_found.append(search_dict)

        elif isinstance(value, dict):
            fields_found += get_key_recursively(value, field, filter_None)

        elif isinstance(value, list):
            for item in value:
                if not isinstance(item, dict):
                    try:
                        if get_key_recursively(item.__dict__, field, filter_None):
                            fields_found.append(item)
                    except:
                        continue  # can't parse
                else:
                    fields_found += get_key_recursively(item, field, filter_None)

    return fields_found


def get_key_recursively_fuzzy(search_dict, field, thresh=0.6, filter_None=True):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    if not is_jsonifiable(search_dict):
        raise ValueError("unparseable format")

    fields_found = []

    for key, value in search_dict.items():
        if value is None and filter_None:
            continue
        score = 0
        if isinstance(key, str):
            score = fuzzy_match(key, field)

        if score >= thresh:
            fields_found.append((search_dict, score))
        elif isinstance(value, dict):
            fields_found += get_key_recursively_fuzzy(value, field, thresh, filter_None)

        elif isinstance(value, list):
            for item in value:
                if not isinstance(item, dict):
                    try:
                        if get_key_recursively_fuzzy(item.__dict__, field, thresh, filter_None):
                            fields_found.append((item, score))
                    except:
                        continue  # can't parse
                else:
                    fields_found += get_key_recursively_fuzzy(item, field, thresh, filter_None)
    return sorted(fields_found, key = lambda i: i[1],reverse=True)


def get_value_recursively(search_dict, field, target_value):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    if not is_jsonifiable(search_dict):
        raise ValueError("unparseable format")
    fields_found = []

    for key, value in search_dict.items():

        if key == field and value == target_value:
            fields_found.append(search_dict)

        elif isinstance(value, dict):
            fields_found += get_value_recursively(value, field, target_value)

        elif isinstance(value, list):
            for item in value:
                if not isinstance(item, dict):
                    try:
                        if get_value_recursively(item.__dict__, field, target_value):
                            fields_found.append(item)
                    except:
                        continue  # can't parse
                else:
                    fields_found += get_value_recursively(item, field, target_value)

    return fields_found


def get_value_recursively_fuzzy(search_dict, field, target_value, thresh=0.6):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    if not is_jsonifiable(search_dict):
        raise ValueError("unparseable format")
    fields_found = []
    for key, value in search_dict.items():
        if key == field:
            if isinstance(value, str):
                score = fuzzy_match(target_value, value)
                if score >= thresh:
                    fields_found.append((search_dict, score))
            elif isinstance(value, list):
                for item in value:
                    score = fuzzy_match(target_value, item)
                    if score >= thresh:
                        fields_found.append((search_dict, score))
        elif isinstance(value, dict):
            fields_found += get_value_recursively_fuzzy(value, field, target_value, thresh)

        elif isinstance(value, list):
            for item in value:
                if not isinstance(item, dict):
                    try:
                        found = get_value_recursively_fuzzy(item.__dict__, field, target_value, thresh)
                        if len(found):
                            fields_found.append((item, found[0][1]))
                    except:
                        continue  # can't parse
                else:
                    fields_found += get_value_recursively_fuzzy(item, field, target_value, thresh)

    return sorted(fields_found, key = lambda i: i[1],reverse=True)


def jsonify_recursively(thing):
    if isinstance(thing, list):
        jsonified = list(thing)
        for idx, item in enumerate(thing):
            jsonified[idx] = jsonify_recursively(item)
    elif isinstance(thing, dict):
        try:
            # can't import at top level to do proper check
            jsonified = dict(thing.db)
        except:
            jsonified = dict(thing)
        for key in jsonified.keys():
            value = jsonified[key]
            jsonified[key] = jsonify_recursively(value)
    else:
        try:
            jsonified = thing.__dict__
        except:
            jsonified = thing
    return jsonified
