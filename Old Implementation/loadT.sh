#!/bin/bash

db="spotify.sqlite"

sqlite3 $db < empty-tables.sql
sqlite3 $db < load-tpch.sql

