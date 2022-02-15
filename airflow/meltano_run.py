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

    # run command

if __name__ == '__main__':
    set_env()
    command = sys.argv[1:]
    if command[0] == "start_webserver":
        subprocess.run("cd /opt/airflow && poetry run airflow webserver --port $PORT" , shell=True)
    elif command[0] == "start_scheduler":
        subprocess.run("cd /opt/airflow && poetry run airflow scheduler", shell=True)
    else:
        subprocess.run(command)
        