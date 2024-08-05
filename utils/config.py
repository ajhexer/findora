import json


class Config:
    def __init__(self, config_path):
        self.config = self.__load_config(config_path)

    @staticmethod
    def __load_config(config_path):
        with open(config_path, "r") as f:
            return json.load(f)

    def __getitem__(self, key):
        return self.config[key]