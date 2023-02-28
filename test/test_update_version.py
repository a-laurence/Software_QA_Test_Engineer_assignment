import pathlib

import pytest
import yaml

from version_updater.update_version import VersionUpdater, UpdateMode


class FakeEvent(VersionUpdater):
    def __init__(self, current_version, new_version):
        super().__init__(current_version, new_version, mode=UpdateMode.Default)


def test_add_new_fields_not_in_current():
    """
    If a field of new_version is not present in current_version,
    it should be added to current_version with its value set to the value from new_version.
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
    If a field of new_version is present in current_version,
    it should keep the value from current_version.
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
    If a field of current_version is not present in new_version,
    it should be removed from current_version.
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


def load_yaml(file_name: str) -> dict:
    file = pathlib.Path().cwd() / "test" / "test_data" / file_name
    with file.open(mode="r") as fid:
        return yaml.full_load(fid)


if __name__ == "__main__":
    print(pathlib.Path().cwd())
    pytest.main()
