#!/bin/bash

rm -f score.res
rm -f tpch.sqlite
touch tpch.sqlite


sqlite3 spotify.sqlite < create-schema-tpch.sql
#sqlite3 spotify.sqlite < check-schema-tpch.sql > output.out

