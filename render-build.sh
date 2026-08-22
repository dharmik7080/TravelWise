#!/usr/bin/env bash
# exit on error
set -o errexit

# Install python dependencies
pip install -r TravelPlanner/requirements.txt

# Run migrations
python TravelPlanner/manage.py migrate --no-input

# Seed initial database values
python TravelPlanner/manage.py seed_data

# Train the ML models
python TravelPlanner/manage.py train_predictor

# Collect static files
python TravelPlanner/manage.py collectstatic --no-input --clear
