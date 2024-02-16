import os
import yaml

class Config:
    def __init__(self, config_file="config.yaml"):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        with open(config_file, "r") as f:
            return yaml.safe_load(f)

    def get_gpt_config(self):
        return self.config.get("gpt_config", {})
