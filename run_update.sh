#!/bin/bash

pip3 install --upgrade pip
pip3 install --user pipenv
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 -m pipenv install --dev --skip-lock
python3 -m pipenv run pre-commit install

logger () {
  printf "[$(date +"%Y-%m-%d %T")] $@\n"
}

if [ $# -lt 2 ]; then
  logger "ERROR - No enough arguments. Given $#, required at least 2 YAML files"
  exit 1
fi

# Check if at least two YAML files are given
for (( i=1; i<=2; i++ )); do
  if ! [ -f ${!i} ]; then
    logger "ERROR - ${!i} is not a valid YAML! Please provide a valid YAML file."
    exit 1
  else
     logger "INFO - Found a valid YAML file: ${!i}"
  fi
done

# Get optional arguments
UPDATE=""
DEBUG=""
for (( i=3; i<=$#; i++ )); do
  j=$((i+1))
  case "${!i}" in
    "--mode")
      UPDATE="${!j}";;
    "--log-level")
      DEBUG="${!j}";;
    *)
      ;;
  esac
done

export CURRENT_VERSION=$1
export NEW_VERSION=$2
export UPDATE
export DEBUG

logger "INFO - Starting Version Updater with given inputs:"
echo -e " current_version: $1 \n new_version: $2 \n update: $UPDATE \n debug: $DEBUG"

python3 -m pipenv run python version_updater/update_version.py
