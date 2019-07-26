#!/bin/bash

dataVal=`date '+%Y%m%d'`
<<<<<<< HEAD
python /home/mac/nuxt-express-template/_ganalyticsSenmonMonth.py $dataVal
=======

python _ganalyticsSenmonMonth.py $dataVal &
pid=$!
wait $pid

python _ganalyticsSenmonMonth.py $dataVal &
pid=$!
wait $pid
>>>>>>> 6edfc938cd9b20ae6ce4065f8d67da831bf8789b
