#!/bin/bash

pip3 install --upgrade pip
pip3 install --user pipenv
python3 -m pipenv install --dev --skip-lock
python3 -m pipenv run pre-commit install
