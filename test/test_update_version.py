import inspect
import pathlib

import pytest
import yaml

from version_updater.update_version import VersionUpdater


class VersionUpdaterTest(VersionUpdater):
    def __init__(self, current_version, new_version, mode):
        super().__init__(current_version, new_version, mode)

    def has_value(self, data: tuple, _map: dict) -> bool:
        if data in _map.items():
            return True
        for _, v in _map.items():
            if isinstance(v, dict):
                return self.has_value(data, v)
        return False

    def contains_all(self, items: list[tuple]) -> bool:
        result = True
        for item in items:
            result &= self.has_value(item, self._current_version)
        return result

    def contains_any(self, expected: list[tuple]) -> bool:
        result = True
        for each in expected:
            result |= self.has_value(each, self._current_version)
        return result


class TestVersionUpdate:
    @staticmethod
    def get_test_name():
        return inspect.stack()[2][3]

    @staticmethod
    def get_test_data(test: str) -> dict:
        test_file = pathlib.Path().cwd() / "test/test_data.yaml"
        with test_file.open(mode="r") as f:
            return yaml.full_load(f)[test]

    def get_test_event(self, mode: str = "default") -> VersionUpdaterTest:
        test_name = self.get_test_name()
        test_data = self.get_test_data(test_name)
        return VersionUpdaterTest(
            test_data["current_version"], test_data["new_version"], mode
        )

    def test_add_new_fields_not_in_current(self):
        """
        Verify if fields in new_version and its values are added to current_version if fields not in current_version.
        :return:
        """
        event = self.get_test_event()
        assert event.contains_all(
            [
                (
                    "max_error",
                    {"bottle": [0.005, 0.005, 0.005], "can": [0.003, 0.003, 0.003]},
                ),
                ("auto_check", False),
            ]
        )

    def test_new_version_in_current_version(self):
        """
        Verify if values in current_version are kept when fields are both in new_version and current_version.
        :return:
        """
        event = self.get_test_event()
        assert event.contains_all(
            [
                ("max_speed", 0.20),
                ("origin_offset", [0.2, 0.1, 0.5]),
                ("auto_check", False),
            ]
        )

    def test_current_version_field_not_in_new_version(self):
        """
        Verify if current_version fields are removed when fields are not in new_version.
        :return:
        """
        event = self.get_test_event()
        assert not event.contains_all(
            [
                ("auto_check", False),
                (
                    "max_error",
                    {"bottle": [0.005, 0.005, 0.005], "can": [0.003, 0.003, 0.003]},
                ),
            ]
        )

    def test_simple_update_replace_value_only(self):
        """
        Verify when mode is Simple update:
            - It only replaces the values of the current_version fields with the values from new_version;
            - No fields are removed from or added to the current_version.
        :return:
        """
        event = self.get_test_event(mode="simple")
        assert event.contains_all(
            [
                ("origin_offset", [0.2, 0.1, 0.5]),
                ("auto_check", True),
                ("max_speed", 0.25),
            ]
        ) and not event.contains_all(
            [
                (
                    "move",
                    {
                        "max_error": [0.005, 0.005, 0.005],
                        "max_speed": 0.15,
                        "max_accel": 0.30,
                    },
                )
            ]
        )

    def test_brute_update(self):
        """
        Verify when mode is Brute update:
            - Removes fields in current_version if fields not in new_version.
            - Adds fields to current_version if field are in new_version and not in current_version.
            - Replaces values in current_version with the values in new_version.
        :return:
        """
        event = self.get_test_event(mode="brute")
        assert event.contains_all(
            [
                ("auto_check", True),
                (
                    "move",
                    {
                        "max_error": [0.005, 0.005, 0.005],
                        "max_speed": 0.15,
                        "max_accel": 0.30,
                    },
                ),
            ]
        ) and not event.contains_all([("origin_offset", [0.2, 0.1, 0.5])])


if __name__ == "__main__":
    pytest.main(["-x", "--verbose"])
