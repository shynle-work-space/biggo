CREATE USER 'accessuser'@'%' IDENTIFIED BY 'accesspwd';

CREATE DATABASE authdb;

GRANT ALL ON authdb.* TO 'accessuser'@'%' IDENTIFIED BY "accesspwd";

USE authdb;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  pwd VARCHAR(255) NOT NULL
);

INSERT INTO users (username, pwd) VALUES ('Mập', 'Mập khùng');
INSERT INTO users (username, pwd) VALUES ('Rex', 'Rex siu super');

REVOKE DROP ON authdb.* FROM 'accessuser'@'%';

FLUSH PRIVILEGES;


