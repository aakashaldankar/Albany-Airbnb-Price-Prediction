#!/bin/sh
set -eu

: "${PROMETHEUS_HOST:=prometheus}"

envsubst '${PROMETHEUS_HOST}' \
  < /etc/grafana/provisioning/datasources/datasource.yml.template \
  > /etc/grafana/provisioning/datasources/datasource.yml

exec /run.sh "$@"
