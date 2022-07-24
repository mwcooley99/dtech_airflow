#!/usr/bin/env make

.PHONY: deploy
deploy:
	docker build -f Dockerfile.scheduler -t cooley/airflow-scheduler:lastest -f Dockerfile.scheduler .
	docker tag docker.io/cooley/airflow-scheduler:lastest registry.heroku.com/dtech-airflow/scheduler
	docker push registry.heroku.com/dtech-airflow/scheduler

	docker build -f Dockerfile.web -t cooley/airflow-web:lastest -f Dockerfile.web .
	docker tag docker.io/cooley/airflow-web:lastest registry.heroku.com/dtech-airflow/web
	docker push registry.heroku.com/dtech-airflow/web

	heroku container:release web scheduler
