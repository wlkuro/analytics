#!/bin/bash

dataVal=`date '+%Y%m%d'`
<<<<<<< HEAD
python /home/mac/nuxt-express-template/_ganalyticsSenmonWeek.py $dataVal
=======

python _ganalyticsSenmonWeek.py $dataVal &
pid=$!
wait $pid

python _ganalyticsSenmonWeek.py $dataVal &
pid=$!
wait $pid
>>>>>>> 6edfc938cd9b20ae6ce4065f8d67da831bf8789b
