#!/usr/bin/env bash
# exit on error
set -o errexit

# Install python dependencies
pip install -r TravelPlanner/requirements.txt

# Run migrations
python TravelPlanner/manage.py migrate --no-input

# Seed initial database values
python TravelPlanner/manage.py import_destinations TravelPlanner/destinations.csv
python TravelPlanner/manage.py import_attractions TravelPlanner/attractions.csv
python TravelPlanner/manage.py import_packages TravelPlanner/packages.csv
python TravelPlanner/manage.py import_seasons TravelPlanner/best_seasons.csv

# Collect static files
python TravelPlanner/manage.py collectstatic --no-input --clear
