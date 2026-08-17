#!/bin/sh
set -eu

: "${FASTAPI_HOST:=fastapi}"

envsubst '${FASTAPI_HOST}' < /etc/prometheus/prometheus.yml.template > /etc/prometheus/prometheus.yml

exec /bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/prometheus \
  --web.listen-address=0.0.0.0:9090
