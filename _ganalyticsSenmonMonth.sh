#!/bin/bash

dataVal=`date '+%Y%m%d'`

python _ganalyticsSenmonMonth.py $dataVal &
pid=$!
wait $pid

python _ganalyticsSenmonMonth.py $dataVal &
pid=$!
wait $pid
