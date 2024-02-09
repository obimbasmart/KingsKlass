-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS kingsklass_dev_db;
CREATE USER IF NOT EXISTS 'kingsklass_dev'@'localhost' IDENTIFIED BY 'kingsklass_dev_pwd';
GRANT ALL PRIVILEGES ON `kingsklass_dev_db`.* TO 'kingsklass_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'kingsklass_dev'@'localhost';
FLUSH PRIVILEGES;