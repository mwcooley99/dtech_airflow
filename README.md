# heroku build commands need to add to a build script of some sort
docker build -f Dockerfile.scheduler -t cooley/airflow-scheduler:lastest -f Dockerfile.scheduler .
docker tag docker.io/cooley/airflow-scheduler:lastest registry.heroku.com/dtech-airflow/scheduler
docker push registry.heroku.com/dtech-airflow/scheduler

docker build -f Dockerfile.web -t cooley/airflow-web:lastest -f Dockerfile.web .
docker tag docker.io/cooley/airflow-web:lastest registry.heroku.com/dtech-airflow/web
docker push registry.heroku.com/dtech-airflow/web

heroku container:release web scheduler

# Dockerfile improvements

- Try combining the initial layers as written [here](https://docs.docker.com/develop/develop-images/multistage-build/#use-a-previous-stage-as-a-new-stage)
- Additionally consider moving back to the meltano Docker image...not sure it's worth it...but might be worth considering.
- Confirm that the meltano installs aren't cached in a way that I don't want. In particular, I'm a little concerned it's not noticing changes to the taps.