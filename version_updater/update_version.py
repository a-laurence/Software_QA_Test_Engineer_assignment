import os
import sys
from pathlib import Path
from typing import *

import yaml

from version_updater.constants import UpdateMode
from version_updater.logger import logger


class VersionUpdater:
    def __init__(
        self,
        current_version: Dict,
        new_version: Dict,
        mode: UpdateMode = None,
        log=logger(),
    ) -> None:
        self._current_version = current_version
        self._new_version = new_version
        self.logger = log

        self.logger.info("Started Version Updater app")

        if self.update_current_version(mode):
            self.logger.info("Updated versions successfully!")
            # self.write_update_to_file(current_version)
        else:
            self.logger.info("Version update is unsuccessful!")

    def update_current_version(self, mode: UpdateMode) -> bool:
        self.logger.info(f"Starting update, mode={mode.name}")
        if mode == UpdateMode.Simple:
            return self.simple_update()
        elif mode == UpdateMode.Brute:
            return self.brute_update()
        else:
            return self.default_update()

    def default_update(self) -> bool:
        try:
            self.update_remove_fields()
            self.update_add_fields()
        except Exception as e:
            self.logger.error(e)
            sys.exit(1)
        return True

    def simple_update(self) -> bool:
        self.logger.info(
            "Replacing the values of the current fields with the values from new_version"
        )
        try:
            self._current_version = {
                k: self.populate_new_values(v, self._new_version[k])
                if k in self._new_version
                else v
                for k, v in self._current_version.items()
            }
        except Exception as e:
            self.logger.error(e)
            return False
        return True

    def brute_update(self) -> bool:
        try:
            self.default_update()
            self.simple_update()
        except Exception as e:
            self.logger.error(e)
            return False
        return True

    def populate_new_values(self, curr_field: Any, new_field: Any) -> Any:
        collection = dict()
        try:
            for field in curr_field:
                if field in new_field:
                    if isinstance(new_field[field], dict):
                        collection[field] = self.populate_new_values(
                            curr_field[field], new_field[field]
                        )
                    else:
                        collection[field] = new_field[field]
                else:
                    collection[field] = curr_field[field]
        except TypeError:
            return new_field
        return collection

    def update_add_fields(self) -> None:
        self.logger.info(
            "Adding new version fields that are not in the current version"
        )
        for key, value in self._new_version.items():
            if key not in self._current_version:
                self.logger.debug(f"Added new field - {key}")
                self._current_version[key] = value
            else:
                self.logger.debug(
                    f"Inspecting existing field ({key}) and adding sub-field if not in current version"
                )
                self.inspect_add_data(
                    self._current_version[key], self._new_version[key]
                )

    def update_remove_fields(self) -> None:
        self.logger.info("Removing current version fields if not in the new version")
        for key in self._current_version.copy():
            if key not in self._new_version.keys():
                self.logger.debug(f"Removed field from current version - {key}")
                del self._current_version[key]
            else:
                self.logger.debug(
                    f"Inspecting existing field ({key}) and removing sub-field if not in the new version"
                )
                self.inspect_remove_data(
                    self._current_version[key], self._new_version[key]
                )

    def inspect_add_data(self, curr_field: Any, new_field: Any) -> None:
        try:
            for key in new_field:
                if key not in curr_field:
                    curr_field[key] = new_field[key]
                    continue
                if isinstance(curr_field[key], dict):
                    self.inspect_add_data(curr_field[key], new_field[key])
        except TypeError:
            return

    def inspect_remove_data(self, curr_field: Dict, new_field: Dict):
        try:
            for key in curr_field.copy():
                if key not in new_field.keys():
                    del curr_field[key]
                else:
                    if isinstance(curr_field[key], dict):
                        self.inspect_remove_data(curr_field[key], new_field[key])
        except AttributeError:
            return

    def has_value(self, data: Tuple, _map: Dict) -> bool:
        if data in _map.items():
            return True
        for _, v in _map.items():
            if isinstance(v, dict):
                return self.has_value(data, v)
        return False

    def contains(self, items: List[Tuple]) -> list:
        result = []
        for item in items:
            result.append(self.has_value(item, self._current_version))
        print(result)
        return result


def get_update_mode(_type: str) -> UpdateMode:
    try:
        return UpdateMode[_type.strip().capitalize()]
    except KeyError:
        return UpdateMode.Default


def load_yaml(file_name: str) -> Dict:
    file = Path(file_name)
    if file.suffix != ".yaml":
        logger.error("Invalid file type! File should be .yaml")
        sys.exit(1)
    try:
        with Path(file).open(mode="r") as fid:
            return yaml.full_load(fid)
    except FileNotFoundError:
        logger.error("Could not find YAML file!")
        sys.exit(1)


if __name__ == "__main__":
    curr = load_yaml(os.environ["CURRENT_VERSION"].strip())
    new = load_yaml(os.environ["NEW_VERSION"].strip())
    update_mode = get_update_mode(os.environ["UPDATE"])
    logger = logger(os.environ["DEBUG"].strip().upper())

    logger.debug(f"Update Mode: {update_mode.name}")
    VersionUpdater(current_version=curr, new_version=new, mode=update_mode, log=logger)
    logger.info("Version Updater app is closed!")
