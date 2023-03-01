# Software QA Test Engineer Assignment

## Pre-requisite
python 3.9
```

```

## About
This is an application that takes two YAML files input, `current_version`
and `new_version`, and updates `current_version`.

### Update Modes
#### Default Update
- Adds `new_version` field and its value to `current_version` if field not in `current_version`.
- Keeps the value from `current_version` if `new_version` field is in `current_version`.
- Removes `current_version` field if field not in `new_version`.
#### Simple Update
- Only replaces the values in `current_version` if corresponding fields are in `new_version`.
#### Brute Update
- Adds `new_version` field and its value to `current_version` if field not in `current_version`.
- Removes `current_version` field if field not in `new_version`.
- Replaces the values in `current_version` if corresponding fields are in `new_version`.

## Usage
Your application must be compatible with the provided `config.yaml`. We will use
similar config files for the evaluation. You are free to create additional yaml
files for your development or tests.

Your application must provide feedback to the user via a logger. The user can
change the logging level by providing optional arguments. The error messages must
be explicit enough for a non-developer to understand the problem.

In addition, you must provide tests that will assess the correct behaviour of the
application. Your tests should, at least, verify all the requirements listed above.

Finally, you must provide a way to install the application and all its dependencies
and the documentation explaining how to use it.

Coding requirement:
- You must use Python (3.8 or more recent) for both the application and the tests
- You must use a test framework such as [Pytest](https://docs.pytest.org/)
- The documentation must be provide as a README

Note:
- You can use any yaml library such as [PyYaml](https://pyyaml.org/wiki/PyYAML)
- You can use any logging library such as [daiquiri](https://daiquiri.readthedocs.io/en/latest/)


We expected the test to takes about 2~4 hours to complete the assignment.


## How to submit

Your work needs to be available on a public repository. We should be able to
install your application, its dependency, and we can run your application from a
terminal.


##  Evaluation

We will clone the repository and install the application in our test environment.
After analyzing your code, we will run your provided tests and the tests we have
prepared.

Your work will be evaluated according to the following criterias (list non-exhaustive):
- The quality of your code, its clarity, its explicitness, and its structure
- Does the applications meet all the requirements
- The test coverage
- How easy the install of the application is
- How user-friendly is the application to use
- The quality of the documentation

> _Important note regarding the test coverage_:
>
> We know that it is possible to create a multitude of tests of a single
> application. Focus on the essential tests that you will find relevant and avoid
> testing strange corner cases.

