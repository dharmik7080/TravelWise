#!/usr/bin/env bash
# exit on error
set -o errexit

# Install python dependencies
pip install -r TravelPlanner/requirements.txt

# Run migrations
python TravelPlanner/manage.py migrate --no-input

# Seed initial database values
python TravelPlanner/manage.py import_destinations TravelPlanner/data/destinations.csv
python TravelPlanner/manage.py import_attractions TravelPlanner/data/attractions.csv
python TravelPlanner/manage.py import_packages TravelPlanner/data/packages.csv
python TravelPlanner/manage.py import_seasons TravelPlanner/data/best_seasons.csv

# Train the Machine Learning Predictor models
python TravelPlanner/ml/train_model.py

# Collect static files
python TravelPlanner/manage.py collectstatic --no-input --clear
