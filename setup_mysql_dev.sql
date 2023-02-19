--
---- Creates a MySQL server with:
----   Database hbnb_dev_db.
----   User hbnb_dev with password hbnb_dev_pwd in localhost.
----   Grants all privileges for hbnb_dev on hbnb_dev_db.
----   Grants SELECT privilege for hbnb_dev on performance_schema.
--
--CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
--CREATE USER
--    IF NOT EXISTS 'hbnb_dev'@'localhost'
--    IDENTIFIED BY 'hbnb_dev_pwd';
--GRANT ALL PRIVILEGES
--   ON `hbnb_dev_db`.*
--   TO 'hbnb_dev'@'localhost'
--GRANT SELECT
--   ON `performance_schema`.*
--   TO 'hbnb_dev'@'localhost'
--FLUSH PRIVILEGES;



#!/bin/bash

# Create database if it does not exist
echo "Creating database hbnb_dev_db if it does not exist..."
mysql -u root -e "CREATE DATABASE IF NOT EXISTS hbnb_dev_db;"

# Create user if it does not exist
echo "Creating user hbnb_dev if it does not exist..."
mysql -u root -e "CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';"

# Grant privileges to the user for the database
echo "Granting privileges to user hbnb_dev for database hbnb_dev_db..."
mysql -u root -e "GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';"

# Grant SELECT privilege to the user for performance_schema
echo "Granting SELECT privilege to user hbnb_dev for performance_schema..."
mysql -u root -e "GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';"