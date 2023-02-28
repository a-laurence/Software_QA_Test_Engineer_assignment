import pathlib

import pytest
import yaml

from version_updater.update_version import VersionUpdater, UpdateMode


class FakeEvent(VersionUpdater):
    def __init__(self, current_version, new_version, mode=UpdateMode.Default):
        super().__init__(current_version, new_version, mode)


def test_add_new_fields_not_in_current():
    """
    Verify if fields in new_version and its values are added to current_version if fields not in current_version.
    :return:
    """
    current_version = load_yaml("test_data_2.yaml")
    new_version = load_yaml("test_data_1.yaml")
    event = FakeEvent(current_version, new_version)
    assert all(
        event.contains(
            [
                (
                    "max_error",
                    {"bottle": [0.005, 0.005, 0.005], "can": [0.003, 0.003, 0.003]},
                ),
                ("auto_check", False),
            ]
        )
    )


def test_new_version_in_current_version():
    """
    Verify if values in current_version are kept when fields are both in new_version and current_version.
    :return:
    """
    current_version = load_yaml("test_data_1.yaml")
    new_version = load_yaml("test_data_3.yaml")
    event = FakeEvent(current_version, new_version)
    assert all(
        event.contains(
            [
                ("max_speed", 0.20),
                ("origin_offset", [0.2, 0.1, 0.5]),
                ("auto_check", False),
            ]
        )
    )


def test_current_version_field_not_in_new_version():
    """
    Verify if current_version fields are removed when fields are not in new_version.
    :return:
    """
    current_version = load_yaml("test_data_1.yaml")
    new_version = load_yaml("test_data_2.yaml")
    event = FakeEvent(current_version, new_version)
    assert not any(
        event.contains(
            [
                ("auto_check", False),
                (
                    "max_error",
                    {"bottle": [0.005, 0.005, 0.005], "can": [0.003, 0.003, 0.003]},
                ),
            ]
        )
    )


def test_simple_update_replace_value_only():
    """
    Verify if it only replaces the values of the current_version fields with the values from new_version;
    No fields are removed from or added to the current_version when mode is Simple update.
    :return:
    """
    current_version = load_yaml("test_data_1.yaml")
    new_version = load_yaml("test_data_4.yaml")
    event = FakeEvent(current_version, new_version, UpdateMode.Simple)
    assert all(
        event.contains(
            [
                ("origin_offset", [0.2, 0.1, 0.5]),
                ("auto_check", True),
                ("max_speed", 0.25),
            ]
        )
    ) and not all(
        event.contains(
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
    )


def load_yaml(file_name: str) -> dict:
    file = pathlib.Path().cwd() / "test" / "test_data" / file_name
    with file.open(mode="r") as fid:
        return yaml.full_load(fid)


if __name__ == "__main__":
    pytest.main()
