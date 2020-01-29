from json_database import JsonStorage

save_path = "my_dict.conf"

with JsonStorage(save_path) as my_config:
    my_config["lang"] = "pt"
    my_config["secondary_lang"] = "en"
    my_config["email"] = "jarbasai@mailfence.com"

# auto saved
