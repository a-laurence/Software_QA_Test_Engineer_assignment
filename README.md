# Software QA Test Engineer Assignment

## Pre-requisite
```
# Requires
python 3.9

# Packages
pyyaml
ruamel.yaml
daiquiri
pathlib
pytest<7.1

# Dev Packages
pre-commit
black

# Packaging Tool
pipenv
```

## About
This is an application that takes two YAML files input, `current_version`
and `new_version`, and updates `current_version`.

### Update Modes
#### 1. Default Update
- Adds `new_version` field-value to `current_version` if field not in `current_version`.
- Keeps the value from `current_version` if `new_version` field is in `current_version`.
- Removes `current_version` field if field not in `new_version`.
#### 2. Simple Update
- Only replaces the values in `current_version` if corresponding fields are in `new_version`.
#### 3. Brute Update
- Adds `new_version` field-value to `current_version` if field not in `current_version`.
- Removes `current_version` field if field not in `new_version`.
- Replaces the values in `current_version` if corresponding fields are in `new_version`.
-
## Usage
1. Start the program by running the `run_update.sh` and pass two YAML files as arguments.
`run_update.sh` is a wrapper script, it creates the virtual environment, parse the arguments, and start the app once executed.
Optional arguments should be passed with flags. `--mode` to set Update Mode, and `--log-level` to set logging level.
When there are no optional arguments, defaults are `DEBUG` for logging level and `default` for update mode.<br><br>
Example is shown below:
```
# no optional arguments
./run_update current_version.yaml new_version.yaml

# with optional arguments
./run_update current_version.yaml new_version.yaml --mode simple --log-level debug
```
2. Check result in the `out` folder.

## Testing
1. Start the test by running the `run_test.sh`
2. Test data and test software are located in the `test` directory.
3. The `VUExtenstion` class provides support in evaluating the test.<br>`contains_all()` to assert all expected output.<br>`contains_any()` to assert any of the expected output.
4. Test data ara saved in `test_data.yaml` file. Test data should be in a map format where test_name is the key.<br><br>
Below is the example of writing a test data:
```
# format
test_name:
  current_version:
    key: value

  new_version:
    key: value

# example
test_brute_update:
  current_version:
    max_speed: 0.20

  new_version:
    max_speed: 0.15
```
