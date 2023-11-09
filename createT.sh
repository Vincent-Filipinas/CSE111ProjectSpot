#!/bin/bash

rm -f score.res
rm -f tpch.sqlite
touch tpch.sqlite


sqlite3 tpch.sqlite < create-schema-tpch.sql
#sqlite3 tpch.sqlite < check-schema-tpch.sql > output.out

