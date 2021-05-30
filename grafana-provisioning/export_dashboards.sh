#!/bin/bash

#set -o errexit
#set -o pipefail
set -x

HOST="localhost"
FULLURL="http://admin:admin@$HOST"

set -o nounset

echo "Exporting Grafana dashboards from $HOST"
for dash in $(curl -s "$FULLURL/api/search?query=&" | jq -r '.[] | select(.type == "dash-db") | .uid'); do
        curl -s "$FULLURL/api/dashboards/uid/$dash" | jq -r . > dashboards/${dash}.json
        slug=$(cat dashboards/${dash}.json | jq -r '.meta.slug')
        mv dashboards/${dash}.json dashboards/${dash}-${slug}.json
done
