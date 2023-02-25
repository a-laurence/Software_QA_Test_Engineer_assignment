# Software QA Test Engineer Assignment

## Context:

As a Software Test Engineer, you will create test scripts to assess the functional
quality of robot components. That requires you to have the ability to evaluate a
feature to design relevant tests.

This assignment aims to evaluate some of the following technical requirements:
- Coding skill
- Testing skill


## Assignment

Create an application that takes as an input two YAML files, `current_version`
and `new_version`, and updates `current_version` as follows:
- If a field of `new_version` is not present in `current_version`, it should be
  added to `current_version` with its value set to the value from `new_version`.
- If a field of `new_version` is present in `current_version`, it should keep the
  value from `current_version`.
- If a field of `current_version` is not present in `new_version`, it should be
  removed from `current_version`.

In addition, the user can use optional arguments to:
- Force the update of `current_version` by only replacing the values of the
  currently existing fields with the values from `new_version`
- Force the update of `current_version` by replacing the values of the currently
  existing fields with the values from `new_version` and adding or removing the
  fields according  to the requirement mentioned above.

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

