-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS idoc_db;
CREATE USER IF NOT EXISTS 'idoc'@'localhost' IDENTIFIED BY 'user_pwd';
GRANT ALL PRIVILEGES ON `idoc_db`.* TO 'idoc'@'localhost';
GRANT CREATE, ALTER, DROP, REFERENCES ON *.* TO 'idoc'@'localhost';
GRANT INDEX ON `idoc_db`.* TO 'idoc'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'idoc'@'localhost';
FLUSH PRIVILEGES;
