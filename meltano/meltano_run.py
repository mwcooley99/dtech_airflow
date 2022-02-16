#!/usr/bin/python
import os
import sys
import subprocess
from urllib.parse import urlparse

def set_env():
    # parse database url
    app_url = os.getenv("HEROKU_POSTGRESQL_GRAY_URL")
    parsed_url = urlparse(app_url)
    os.environ['CBL_APP_DATABASE_HOST'] = parsed_url.hostname
    os.environ['CBL_APP_DATABASE_USER'] = parsed_url.username
    os.environ['CBL_APP_DATABASE_PASSWORD'] = parsed_url.password
    os.environ['CBL_APP_DATABASE_NAME'] = parsed_url.path.lstrip('/')

    # os.environ.pop('VIRTUAL_ENV', None)

    # run command

if __name__ == '__main__':
    set_env()
    # TODO: combine the two *_run.py files into one and move to /opt/bin
    command = sys.argv[1:]
    command_str = ' '.join(command)
    subprocess.run(command)    