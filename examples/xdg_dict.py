from json_database import JsonStorageXDG
from json_database.exceptions import DatabaseNotCommitted
from os.path import exists

save_path = "my_dict"

my_config = JsonStorageXDG(save_path)
print(my_config.path)
my_config["lang"] = "pt"
my_config["secondary_lang"] = "en"
my_config["email"] = "jarbasai@mailfence.com"

# my_config is a python dict
assert isinstance(my_config, dict)

# save to file
my_config.store()
print(my_config)
my_config["lang"] = "pt-pt"
print(my_config)
# revert to previous saved file
my_config.reload()
print(my_config)
assert my_config["lang"] == "pt"

# clear all fields
my_config.clear()

assert my_config == {}

# delete stored file
my_config.remove()
assert not exists(save_path)

# keep working with dict
print(my_config)

try:
    my_config.reload()
except DatabaseNotCommitted:
    print("you deleted config above dumbass")
