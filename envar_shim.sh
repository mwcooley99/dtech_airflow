#!/bin/bash
echo "exporting environment variables..."
export DATABASE_URL_FORMATTED=${DATABASE_URL/postgres/postgresql}
export MELTANO_DATABASE_URI=${DATABASE_URL_FORMATTED}?options=-csearch_path%3Dmeltano
export CBL_APP_DATABASE_URL=${HEROKU_POSTGRESQL_GRAY_URL/postgres/postgresql}

export AIRFLOW__CORE__SQL_ALCHEMY_CONN=$DATABASE_URL_FORMATTED
export AIRFLOW_CONN_CBL_APP_DATABASE_URL=$CBL_APP_DATABASE_URL
export AIRFLOW__CORE__FERNET_KEY=$AIRFLOW__CORE__FERNET_KEY
echo "running command..."
exec "$@"