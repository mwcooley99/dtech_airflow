#!/bin/bash

if [[ $DYNO == "web"* ]]; then
    python meltano_run.py start_webserver
elif  [[ $DYNO == "worker"* ]]; then
    python meltnao_run.py start_scheduler
fi