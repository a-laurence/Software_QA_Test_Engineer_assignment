import logging
import os
import sys
import inspect
from enum import Enum
from typing import *

import daiquiri
import yaml
from ruamel.yaml.main import round_trip_load as yaml_load


class UpdateMode(Enum):
    Brute = 0
    Simple = 1


class VersionUpdater:
    def __init__(
        self,
        current_version: str,
        new_version: str,
        mode: UpdateMode = None,
    ) -> None:
        self._current_version = VersionUpdater.load_yaml_file(current_version)
        self._new_version = VersionUpdater.load_yaml_file(
            new_version, is_new_version=True
        )
        self._update_current_version(mode)
        self.write_update_to_file(current_version)

    def _update_current_version(self, _type: UpdateMode) -> Any:
        logger.info(f"Starting {_type.name} update")
        if _type == UpdateMode.Brute:
            self._update_current_fields()
            self._add_missing_fields()

        logger.info(
            "Replacing the values of the current fields with the values from new_version"
        )
        self._current_version = {
            k: self._update_field_value(self._current_version[k], v)
            for k, v in self._new_version.items()
            if k in self._current_version
        }

    def _update_field_value(self, curr_field: Any, new_field: Any) -> Any:
        collection = dict()
        try:
            for field in curr_field:
                if field in new_field:
                    if isinstance(new_field[field], dict):
                        collection[field] = self._update_field_value(
                            curr_field[field], new_field[field]
                        )
                    else:
                        collection[field] = new_field[field]
                else:
                    collection[field] = curr_field[field]
        except TypeError:
            return new_field
        return collection

    def _add_missing_fields(self) -> None:
        logger.info("Adding new version fields that are not in the current version")
        for key, value in self._new_version.items():
            if key not in self._current_version:
                logger.debug(f"Added new field - {key}")
                self._current_version[key] = value
            else:
                self._inspect_add_collections(
                    self._current_version[key], self._new_version[key]
                )

    def _inspect_add_collections(self, curr_field: Any, new_field: Any) -> None:
        try:
            for key in new_field:
                if key not in curr_field:
                    curr_field[key] = new_field[key]
                    continue
                if isinstance(curr_field[key], dict):
                    self._inspect_add_collections(curr_field[key], new_field[key])
        except TypeError:
            return

    def _field_in_file(self, _map: Dict, key: str) -> bool:
        if key in _map:
            return True
        for k, v in _map.items():
            if isinstance(v, dict):
                if self._field_in_file(v, key):
                    return True

    def _update_current_fields(self) -> None:
        logger.info("Removing current version fields if not in the new version")
        for key in self._current_version.copy():
            if key not in self._new_version.keys():
                logger.debug(f"Removed field from current version - {key}")
                del self._current_version[key]
            else:
                self._inspect_remove_collections(
                    self._current_version[key], self._new_version[key]
                )

    def _inspect_remove_collections(self, curr_field: Dict, new_field: Dict):
        try:
            for key in curr_field.copy():
                if key not in new_field.keys():
                    del curr_field[key]
                else:
                    if isinstance(curr_field[key], dict):
                        self._inspect_remove_collections(
                            curr_field[key], new_field[key]
                        )
        except AttributeError:
            return

    @staticmethod
    def load_yaml_file(file: str, is_new_version: bool = False) -> Dict:
        logger.info(f"Reading YAML file - {file}")

        if is_new_version and os.stat(file).st_size == 0:
            logger.error(
                f"Found an empty new version file! New version should not be empty"
            )
            sys.exit(1)

        if not is_yaml_file(file):
            logger.error("Invalid file type! Version file should be a YAML file")
            sys.exit(1)

        try:
            with open(file, "r") as f:
                logger.debug(f"YAML file is loaded successfully!")
                return yaml.full_load(f)
        except FileNotFoundError:
            logger.error(f"Could not find YAML file - {file}")
            sys.exit(1)


def get_debug_level(level: str) -> int:
    try:
        return getattr(logging, level.strip().upper())
    except AttributeError:
        return 10


def get_update_mode(_type: str) -> UpdateMode:
    try:
        return UpdateMode[_type.strip().capitalize()]
    except KeyError:
        return UpdateMode.Simple


def is_yaml_file(file: str) -> bool:
    return False


if __name__ == "__main__":
    daiquiri.setup(level=get_debug_level(os.environ["DEBUG"]))
    logger = daiquiri.getLogger(__name__)
    logger.info("Started application to update current versions")

    update_mode = get_update_mode(os.environ["UPDATE"])
    logger.debug(f"Update Mode: {update_mode.name}")

    VersionUpdater(
        current_version=os.environ["CURRENT_VERSION"].strip(),
        new_version=os.environ["NEW_VERSION"].strip(),
        mode=update_mode,
    )

    logger.info("Current Version is updated successfully!")
