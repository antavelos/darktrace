import os
from pathlib import Path

import yaml

from lib.broker.pubsub import PubSub

with open(os.path.dirname(__file__) + '/../config.yml', "r") as f:
    config = yaml.safe_load(f)
    if config is None:
        config = {}
print(config)
pubsub = PubSub.create(config["BROKER"])

