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
        current_version: str,
        new_version: str,
        mode: str = "Debug",
        log=logger(),
    ) -> None:
        self.logger = log
        self.logger.info("Started Version Updater app")

        self._current_version = self.load(current_version)
        self._new_version = self.load(new_version)

        self._mode = self.mode(mode)
        self.logger.debug(f"Update Mode: {self._mode.name}")

        if self.update_current_version():
            self.logger.info("Updated versions successfully!")
            # self.write_update_to_file(current_version)
        else:
            self.logger.info("Version update is unsuccessful!")

    def update_current_version(self) -> bool:
        self.logger.info(f"Starting {self._mode.name} Update")
        if self._mode == UpdateMode.Simple:
            return self.simple_update()
        elif self._mode == UpdateMode.Brute:
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

    def load(self, data) -> Dict:
        try:
            file = Path(data)
        except TypeError:
            if isinstance(data, dict):
                self.logger.debug(f"Found input data: {data}")
                return data
            self.logger.error("TypeError: expected str, bytes or os.PathLike object")
            sys.exit(1)

        if file.suffix != ".yaml":
            self.logger.error("Invalid file type! Given should be a YAML file")
            sys.exit(1)

        self.logger.info(f"Loading YAML file - {data}")

        try:
            with file.open(mode="r") as f:
                self.logger.debug("YAML file loaded successfully!")
                return yaml.full_load(f)
        except FileNotFoundError:
            self.logger.error(f"Could not find YAML file - {data}")
            sys.exit(1)

    def mode(self, mode: str) -> UpdateMode:
        try:
            return UpdateMode[mode.strip().capitalize()]
        except KeyError:
            self.logger.error("Setting to default mode")
            return UpdateMode.Default


if __name__ == "__main__":
    VersionUpdater(
        current_version=os.environ["CURRENT_VERSION"].strip(),
        new_version=os.environ["NEW_VERSION"].strip(),
        mode=os.environ["UPDATE"],
        log=logger(os.environ["DEBUG"].strip().upper()),
    )
