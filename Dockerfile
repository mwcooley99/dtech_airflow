ARG MELTANO_IMAGE=meltano/meltano:latest
FROM $MELTANO_IMAGE

WORKDIR /project

# Install any additional requirements
# COPY ./requirements.txt . 
# RUN pip install -r requirements.txt

# Install all plugins into the `.meltano` directory
COPY ./meltano/meltano.yml /project/meltano.yml 
RUN meltano install

# Pin `discovery.yml` manifest by copying cached version to project root
RUN cp -n .meltano/cache/discovery.yml . 2>/dev/null || :

# Don't allow changes to containerized project files
# ENV MELTANO_PROJECT_READONLY 1

# Copy over remaining project files
COPY ./meltano/orchestrate /project/orchestrate
COPY ./envar_shim.sh /envar_shim.sh
COPY ./meltano/meltano_run.py /project/meltano_run.py

ENTRYPOINT ["/envar_shim.sh"]
CMD ["start.sh"]
