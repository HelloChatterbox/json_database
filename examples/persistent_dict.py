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

# keep working with dict
print(my_config)

try:
    my_config.reload()
except FileNotFoundError:
    print("you deleted config above dumbass")
