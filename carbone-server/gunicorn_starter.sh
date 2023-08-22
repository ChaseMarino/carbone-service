#!/bin/sh

/usr/local/bin/gunicorn server:app -w 4 --threads 4 -b 0.0.0.0:8080
