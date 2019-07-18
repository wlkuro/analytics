#!/bin/bash

dataVal=`date '+%Y%m%d'`

python _ganalyticsSenmonDay.py $dataVal &
pid=$!
wait $pid

python _ganalyticsSenmonDay.py $dataVal &
pid=$!
wait $pid
