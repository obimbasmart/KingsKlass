-- prepares a MySQL test server for the project

CREATE DATABASE IF NOT EXISTS kingsklass_test_db;
CREATE USER IF NOT EXISTS 'kingsklass_test'@'localhost' IDENTIFIED BY 'kingsklass_test_pwd';
GRANT ALL PRIVILEGES ON `kingsklass_test_db`.* TO 'kingsklass_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'kingsklass_test'@'localhost';
FLUSH PRIVILEGES;