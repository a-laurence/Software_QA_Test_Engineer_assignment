import logging
import os
import sys
from enum import Enum
from collections import OrderedDict
from typing import *

import daiquiri
from ruamel.yaml.main import round_trip_load as yaml_load, round_trip_load as yaml_dump


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
        # for k, v in self._current_version.items():
        #     print(k, ": ", v)
        self.update_current_version(update_type)
        for k, v in self._current_version.items():
            print(k, ": ", v)

    def update_current_version(self, _type: UpdateType) -> None:
        logger.info("Starting version update")
        self.update_current_fields()
        self.add_missing_fields()

    def add_missing_fields(self) -> None:
        logger.info("Adding new version fields that are not in the current version")
        for key, value in self._new_version.items():
            if key not in self._current_version:
                logger.debug(f"Added new field [{key}]")
                self._current_version[key] = value
            else:
                self.inspect_field(self._current_version[key], self._new_version[key])

    def inspect_field(self, curr_field: Any, new_field: Any) -> None:
        try:
            for key in new_field:
                if key not in curr_field:
                    curr_field[key] = new_field[key]
                    continue
                if isinstance(curr_field[key], dict):
                    self.inspect_field(curr_field[key], new_field[key])
        except TypeError:
            return

    def field_in_file(self, _map, key) -> bool:
        if key in _map:
            return True
        for k, v in _map.items():
            if isinstance(v, dict):
                if self.field_in_file(v, key):
                    return True

    def update_current_fields(self) -> None:
        logger.info("Removing current version fields if not in the new version")
        self._current_version = OrderedDict(
            {
                k: self.inspect_remove(v, self._new_version[k])
                for k, v in self._current_version.items()
                if k in self._new_version
            }
        )

    def inspect_remove(self, curr_field: Any, new_field: Any, result=None) -> Dict:
        if not result:
            result = dict()
        for key, value in curr_field.items():
            if key in new_field:
                result[key] = value
                continue
            if isinstance(value, dict):
                self.inspect_remove(value, curr_field[key], result)
        return result

    def dump_yaml(self, out: str) -> None:
        logger.info(f"Dumping updated version")
        with open(out, "w") as f:
            yaml_dump(self._current_version, f, preseve_quotes=True)

    @staticmethod
    def load_yaml_file(yaml_file: str) -> Dict:
        logger.info(f"Reading YAML file - {yaml_file}")
        try:
            with open(yaml_file, "r") as f:
                logger.debug(f"YAML file is loaded successfully")
                return yaml_load(f)
        except FileNotFoundError:
            logger.error(f"Could not find YAML file - {yaml_file}")
            sys.exit(1)


def concatenate(text: str, delimiter=" ", camel_case: bool = True) -> str:
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
        update = UpdateType[concatenate(os.environ["UPDATE"].strip().lstrip("--"), "-")]
        logger.debug(f"Found update type: {update.name}")
    except KeyError:
        update = UpdateType.NoUpdate

    VersionUpdater(current_conf, new_conf, update)
    logger.info("Current Version is updated successfully!")
