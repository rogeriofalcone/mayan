#!/bin/bash
# Run the gunicorn service

# Make sure we're in the right virtual env and location
source /home/nucleos/.virtualenvs/production/bin/activate
source /home/nucleos/.virtualenvs/production/bin/postactivate

cd /home/nucleos/production

exec gunicorn -c /home/nucleos/production/deploy/gunicorn.conf.py nucleos.wsgi:application