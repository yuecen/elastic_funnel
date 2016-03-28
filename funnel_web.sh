#!/bin/bash
exec gunicorn --workers 5 --log-level INFO --bind 0.0.0.0:5578 wsgi:app