generatedata-import
===================

My quick'n dirty solution for importing mysql databases into generatedata.
Currently it makes all columns numeric, with autoincrement on PK. It is really a quickly done thing for my personal usage, but it can be helpful for someone else too.

This script converts a MySQL database structure into INSERT queries, ready to be inserted to Generatedata database. The SQL is put on stdout.

    usage: generatedata-import.py [-h] -s SERVER -u USER -p PASSWORD -d DB
      -s SERVER, --server SERVER
      -u USER, --user USER
      -p PASSWORD, --password PASSWORD
  	  -d DB, --db DB

Example:
    ./generatedata-import.py -s localhost -u db_user -p my_pass -d db > generated.sql


Requirements
============
SQL Alchemy and MySQL Python binding must be installed.
