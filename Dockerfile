FROM python:3.7.12-slim
ENV AIRFLOW_HOME=/opt/airflow

# add users home directory to the path
ENV PATH=/home/devuser/.local.bin:${PATH}

# Add user
RUN groupadd -g 5000 devuser && \
    useradd -g 5000 -d /home/devuser -u 5000 -m devuser
RUN pip install --no-cache-dir --upgrade pip


USER devuser

RUN pip install --user poetry
ENV PATH="${PATH}:/root/.poetry/bin"
COPY --chown=devuser:devuser ./envar_shim.sh /envar_shim.sh
COPY --chown=devuser:devuser airflow/poetry.lock airflow/pyproject.toml ${AIRFLOW_HOME}/
# RUN cd /opt/airflow && poetry install 
WORKDIR /home/devuser
ENTRYPOINT [ "/envar_shim.sh" ]