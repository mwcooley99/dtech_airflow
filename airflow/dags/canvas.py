import os
from datetime import timedelta, datetime
import subprocess
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import task
from airflow.operators.python import PythonOperator


@task(task_id="start_time")
def get_start_time():
    return {"date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}

with DAG(dag_id="canvas_sync", start_date=days_ago(1), schedule_interval="@daily", catchup=False, concurrency=1) as dag:
    start_time = get_start_time()
    canvas_data_pull = BashOperator(
            # TODO: decide if updating db env is worth the extra python script.
            task_id="meltano_canvas",
            bash_command="""
                cd /opt/meltano
                unset VIRTUAL_ENV
                poetry run python meltano_run.py meltano elt tap-canvas target-postgres --select=terms
            """
            )

    # TODO: make this a soft-delete
    delete_cleanup = PostgresOperator(
            task_id="delete_cleanup",
            postgres_conn_id="cbl_app_database_url",
            sql="""
                -- Must add each canvas table that has "hard deletes"
                delete from raw_canvas.terms where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
                -- delete from raw_canvas.outcome_results where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
                -- delete from raw_canvas.courses where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
                -- delete from raw_canvas.enrollments where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
                -- delete from raw_canvas.sections where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';
                -- delete from raw_canvas.users where _sdc_batched_at <= '{{ ti.xcom_pull(task_ids="start_time")["date"] }}';

            """
        )
    start_time >> canvas_data_pull >> delete_cleanup
