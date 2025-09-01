#!/bin/bash

# Check if the user provided a message
if [ -z "$1" ]; then
    echo "Error: No message provided"
    exit 1
fi

# Run the alembic revision command to generate a new migration
alembic revision --autogenerate -m "$1"

# Upgrade the database to the latest version
alembic upgrade head