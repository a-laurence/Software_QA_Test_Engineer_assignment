#!/bin/bash

pip3 install --upgrade pip
pip3 install --user pipenv
python3 -m pipenv install --dev --skip-lock
python3 -m pipenv run pre-commit install

export CURRENT_VERSION=$1
export NEW_VERSION=$2
export UPDATE=$3

python3 -m pipenv run python version_updater/version_updater.py
