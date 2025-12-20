#!/bin/bash

iterations=${1:-3}
start_users=${2:-5}
step_users=${3:-5}
end_users=${4:-130}

for k in $(seq 1 $iterations); do
  for i in $(seq $start_users $step_users $end_users); do
    JVM_ARGS="-Xms10g -Xmx10g" "../apache-jmeter-5.6.3/bin/jmeter" -n -t Pi2_parametrised.jmx -l log.jtl -Jusers="$i" -Jiteration="$k"
    sleep 3
  done
done
