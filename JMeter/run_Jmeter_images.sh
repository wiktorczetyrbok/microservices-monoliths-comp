#!/bin/bash
set -e

iterations=${1:-3}
start_users=${2:-5}
step_users=${3:-5}
end_users=${4:-130}
language=${5:?language not set}
app_type=${6:?app_type not set}

JMETER_BIN="../apache-jmeter-5.6.3/bin/jmeter"
JMX_FILE="Pi2_parametrised_images.jmx"

for k in $(seq 1 "$iterations"); do
  for i in $(seq "$start_users" "$step_users" "$end_users"); do
    echo "[JMeter] iteration=$k users=$i language=$language app_type=$app_type"

    JVM_ARGS="-Xms10g -Xmx10g" "$JMETER_BIN" \
      -n \
      -t "$JMX_FILE" \
      -Jusers="$i" \
      -Jiteration="$k" \
      -Jlanguage="$language" \
      -Japp_type="$app_type"

    sleep 3
  done
done
