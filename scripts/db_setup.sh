#!/bin/sh
export PG_USER="postgres"
psql -c "CREATE DATABASE inventory"
psql inventory -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"