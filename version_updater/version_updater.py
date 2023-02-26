import os
import sys

import yaml
import logging
import daiquiri
from datetime import datetime
from typing import Dict
from enum import Enum


class UpdateType(Enum):
    ForceUpdate = 0
    SimpleUpdate = 1
    NoUpdate = 2


class VersionUpdater:
    def __init__(
        self,
        current_version,
        new_version,
        update_type: UpdateType = None,
    ) -> None:
        self._current_version = VersionUpdater.load_yaml_file(current_version)
        self._new_version = VersionUpdater.load_yaml_file(new_version)
        self._update_version(update_type)

    def _update_version(self, _type: UpdateType) -> None:
        pass

    @staticmethod
    def load_yaml_file(yaml_file: str) -> Dict:
        logger.debug(f"Loading yaml file {yaml_file}")
        try:
            with open(yaml_file, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Could not find YAML file {yaml_file}")
            sys.exit(1)


def concatenate_string(text: str, delimiter=" ", camel_case: bool = True) -> str:
    return "".join([s.capitalize() if camel_case else s for s in text.split(delimiter)])


if __name__ == "__main__":
    daiquiri.setup(level=logging.DEBUG)
    logger = daiquiri.getLogger(__name__)
    logger.info("Starting version updater")

    try:
        current_conf = os.environ["CURRENT_VERSION"].strip()
        new_conf = os.environ["NEW_VERSION"].strip()
    except KeyError:
        logger.error("Not enough YAML file given (required 2)")
        sys.exit(1)

    try:
        update = UpdateType[
            concatenate_string(os.environ["UPDATE"].strip().lstrip("--"), "-")
        ]
        logger.debug(f"Found update type: {update.name}")
    except KeyError:
        update = UpdateType.NoUpdate
