#!/bin/bash

# Set environment variables (if needed)
export FLASK_APP=app.py  # Ensure this matches your Flask file
export FLASK_ENV=production  # Change to development if debugging

# Start the Flask app using Gunicorn (production-ready server)
gunicorn --bind 0.0.0.0:10000 app:app  # Change 'app' to match your Flask filename
