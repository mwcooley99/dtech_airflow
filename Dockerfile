FROM python:3.7.12-slim
ENV AIRFLOW_HOME=/airflow

# add users home directory to the path
ENV PATH=/home/devuser/.local.bin:${PATH}

# Add user
RUN groupadd -g 5000 devuser && \
    useradd -g 5000 -d /home/devuser -u 5000 -m devuser
RUN pip install --no-cache-directory --upgrade pip

USER devuser

RUN pip install --user poetry

COPY ./envar_shim.sh /envar_shim.sh
ENTRYPOINT [ "/envar_shim.sh" ]