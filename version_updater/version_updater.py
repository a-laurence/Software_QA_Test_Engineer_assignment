import logging
import os
import sys
from enum import Enum
from typing import *

import daiquiri
import yaml


class UpdateType(Enum):
    ForceUpdate = 0
    SimpleUpdate = 1
    NoUpdate = 2


class VersionUpdater:
    def __init__(
        self,
        current_version: str,
        new_version: str,
        update_type: UpdateType = None,
    ) -> None:
        self._current_version = VersionUpdater.load_yaml_file(current_version)
        self._new_version = VersionUpdater.load_yaml_file(new_version)
        self._update_current_version(update_type)

    def _update_current_version(self, _type: UpdateType) -> None:
        logger.info("Starting version update")
        for field in self._new_version.items():
            self._add_missing_fields(field)

    def _add_missing_fields(self, field: Tuple) -> None:
        key, value = field
        if key not in self._current_version:
            logger.debug(f"Adding field [{key}] to the current version")
            self._current_version[key] = value
            return

    @staticmethod
    def load_yaml_file(yaml_file: str) -> Dict:
        try:
            with open(yaml_file, "r") as file:
                logger.debug(f"YAML file is loaded - {yaml_file}")
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Could not find YAML file - {yaml_file}")
            sys.exit(1)


def concatenate_string(text: str, delimiter=" ", camel_case: bool = True) -> str:
    return "".join([s.capitalize() if camel_case else s for s in text.split(delimiter)])


if __name__ == "__main__":
    daiquiri.setup(level=logging.DEBUG)
    logger = daiquiri.getLogger(__name__)
    logger.info("Started application to update current versions")

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

    VersionUpdater(current_conf, new_conf, update)
    logger.info("Current Version is updated successfully!")
