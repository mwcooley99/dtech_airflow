FROM python:3.7.12-slim
ENV AIRFLOW_HOME=/opt/airflow

# add users home directory to the path
ENV PATH=/home/devuser/.local/bin:${PATH}
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libpq-dev \
    build-essential
# Add user
RUN groupadd -g 5000 devuser && \
    useradd -g 5000 -d /home/devuser -u 5000 -m devuser

USER devuser

RUN pip install --no-cache-dir --user poetry

COPY --chown=devuser:devuser ./envar_shim.sh /envar_shim.sh
COPY --chown=devuser:devuser airflow /opt/airflow
COPY --chown=devuser:devuser meltano /opt/meltano

RUN cd /opt/airflow && poetry install

RUN cd /opt/meltano && poetry install
RUN cd /opt/meltano && poetry run meltano install

WORKDIR /home/devuser
ENTRYPOINT [ "/envar_shim.sh" ]