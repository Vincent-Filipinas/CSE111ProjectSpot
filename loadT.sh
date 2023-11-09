#!/bin/bash

rm -f score.res
rm -f output/*

score=0
qnum=15
db="tpch.sqlite"

sqlite3 $db < empty-tables.sql
sqlite3 $db < load-tpch.sql

