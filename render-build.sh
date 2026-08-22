#!/usr/bin/env bash
# exit on error
set -o errexit

# Install python dependencies
pip install -r TravelPlanner/requirements.txt

# Run migrations
python TravelPlanner/manage.py migrate --no-input

# Seed initial database values
python TravelPlanner/manage.py import_destinations
python TravelPlanner/manage.py import_attractions
python TravelPlanner/manage.py import_packages
python TravelPlanner/manage.py import_seasons

# Collect static files
python TravelPlanner/manage.py collectstatic --no-input --clear
