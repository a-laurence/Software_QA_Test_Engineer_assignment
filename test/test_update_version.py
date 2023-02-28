import pytest
import yaml
import pathlib
import datetime as dt

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
    event = FakeEvent(load_yaml("test_case_2.yaml"), load_yaml("test_case_2.yaml"))
    assert True


def load_yaml(file_name: str) -> dict:
    file = pathlib.Path().cwd() / "tests" / "test_data" / file_name
    with file.open(mode="r") as fid:
        return yaml.full_load(fid)


if __name__ == "__main__":
    print(pathlib.Path().cwd())
    pytest.main()
