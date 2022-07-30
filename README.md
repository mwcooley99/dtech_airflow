# heroku build commands need to add to a build script of some sort

```
docker build -f Dockerfile.scheduler -t cooley/airflow-scheduler:lastest -f Dockerfile.scheduler .
docker tag docker.io/cooley/airflow-scheduler:lastest registry.heroku.com/dtech-airflow/scheduler
docker push registry.heroku.com/dtech-airflow/scheduler

docker build -f Dockerfile.web -t cooley/airflow-web:lastest -f Dockerfile.web .
docker tag docker.io/cooley/airflow-web:lastest registry.heroku.com/dtech-airflow/web
docker push registry.heroku.com/dtech-airflow/web

heroku container:release web scheduler
```

# Dockerfile improvements TODOs

- [ ] Add a makefile for ^^^ OR add CI/CD of some sort for the push
- [ ] Try combining the initial layers as written [here](https://docs.docker.com/develop/develop-images/multistage-build/#use-a-previous-stage-as-a-new-stage)
- [ ] Additionally consider moving back to the meltano Docker image...not sure it's worth it...but might be worth considering.
- [x] Confirm that the meltano installs aren't cached in a way that I don't want. In particular, I'm a little concerned it's not noticing changes to the taps. **This is just the push is using cached layers I think**
- [ ] Clean up all the extra mess in the meltano directory

# Getting Started

1. Create database

    ```bash
    docker compose up -d meltano-db
    ```

1. Create the meltano schema in the database

    ```sql
    create schema meltano;
    ```

1. create the airflow metadata tables

    ```bash
    airflow db init
    ```

1. create the airflow admin user (values below are for dev only)

    ```bash
    airflow users create \
        --username admin \
        --firstname Peter \
        --lastname Parker \
        --role Admin \
        --email spiderman@superhero.org
    ```