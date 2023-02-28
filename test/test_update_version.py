import pytest
import inspect
import yaml
import pathlib

from version_updater.update_version import VersionUpdater


class FakeEvent(VersionUpdater):
    def __init__(self, current_version, new_version, mode):
        super().__init__(current_version, new_version, mode)


def get_test_name():
    return inspect.stack()[2][3]


def get_test_data(test: str) -> tuple:
    test_file = pathlib.Path().cwd() / "test/test_data.yaml"
    with test_file.open(mode="r") as f:
        test_data = yaml.full_load(f)
    return test_data[test]["current_version"], test_data[test]["new_version"]


def get_fake_event(mode: str = "default") -> FakeEvent:
    test = get_test_name()
    curr, new = get_test_data(test)
    return FakeEvent(curr, new, mode)


def test_add_new_fields_not_in_current():
    """
    Verify if fields in new_version and its values are added to current_version if fields not in current_version.
    :return:
    """
    event = get_fake_event()
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
    event = get_fake_event()
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
    event = get_fake_event()
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
    Verify when mode is Simple update:
        - It only replaces the values of the current_version fields with the values from new_version;
        - No fields are removed from or added to the current_version.
    :return:
    """
    event = get_fake_event(mode="simple")
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


def test_brute_update():
    """
    Verify when mode is Brute update:
        - Removes fields in current_version if fields not in new_version.
        - Adds fields to current_version if field are in new_version and not in current_version.
        - Replaces values in current_version with the values in new_version.
    :return:
    """
    event = get_fake_event(mode="brute")
    assert all(
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
    ) and not all(event.contains([("origin_offset", [0.2, 0.1, 0.5])]))


if __name__ == "__main__":
    pytest.main()
