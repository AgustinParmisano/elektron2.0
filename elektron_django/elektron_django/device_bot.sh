#!/bin/bash
i=0
while [[ 1 -eq 1 ]]; do
  let i++
  dt=$(date '+%d/%m/%Y %H:%M:%S');
  rd=$(shuf -i 0-100 -n 1)
  msg='{"device":' + $i + ', "date":' + $dt + ', "data_value":' + $rd + '}'
  mosquitto_pub -t "sensors/new_data" -m $msg
  if [[ $i -eq 5 ]]; then
    i=0
  fi
  sleep 3
done
