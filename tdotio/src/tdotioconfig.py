import json
import os

import td
from TDStoreTools import DependDict
# from TDStoreTools import DependList


class ConfigExt:

    def __init__(self, owner_comp, config_path):
        self.owner_comp = owner_comp
        self._config = DependDict()

        self.load_config(config_path)

    def load_config(self, config_path):
        if not config_path:
            return {}

        with open(os.path.normpath(config_path)) as config_json:
            config_dict = json.load(config_json)

        for key, val in config_dict.items():
            self._config.setItem(key, val)

    def update(self, update_dict):

        for key, val in update_dict.items():
            self._config.setItem(key, val)

        return self._config

    def set(self, new_config_dict):
        for key in self._config:
            self._config.setItem(key, None)

        return self.update(new_config_dict)

    # Touch Designer
    @property
    def Config(self):
        return self._config

    def Set(self, newConfigDict):
        return self.set(newConfigDict)

    def Update(self, upateDict):
        self.update(upateDict)

    def LoadConfig(self, config_path):
        self.load_config(config_path)
