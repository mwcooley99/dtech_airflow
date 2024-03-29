FROM python:3.8.12-slim
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

# Install airflow in the global python dist
ARG AIRFLOW_VERSION=2.2.3
ARG PYTHON_VERSION=3.8
ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.8.txt"
RUN python -m pip install --upgrade pip
RUN pip install --user "apache-airflow[postgres]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}" \
    pipx
RUN pip install --user python-json-logger

# Install poetry
# RUN python3 -m pip install --user pipx
RUN python3 -m pipx ensurepath
RUN pipx install --force poetry 

# Copy file
COPY --chown=devuser:devuser ./envar_shim.sh /envar_shim.sh
COPY --chown=devuser:devuser airflow /opt/airflow
COPY --chown=devuser:devuser meltano /opt/meltano


# Set up meltano poetry environment
RUN cd /opt/meltano && poetry install
RUN cd /opt/meltano && poetry run meltano install --clean


WORKDIR /home/devuser
ENTRYPOINT [ "/envar_shim.sh" ]