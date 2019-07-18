#!/bin/bash

dataVal=`date '+%Y%m%d'`

python _ganalyticsSenmonWeek.py $dataVal &
pid=$!
wait $pid

python _ganalyticsSenmonWeek.py $dataVal &
pid=$!
wait $pid
