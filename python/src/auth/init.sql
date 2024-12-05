CREATE USER if not exists 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';
-- CREATE USER 'auth_user'@'%' IDENTIFIED BY 'Auth123';
-- CREATE USER 'auth_user'@'desktop-vc620s6.mshome.net' IDENTIFIED BY 'Auth123';
CREATE DATABASE if not exists auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';
-- GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'%';
-- GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'desktop-vc620s6.mshome.net';
USE auth;

CREATE TABLE if not exists user(
	id int not null auto_increment primary key,
	email varchar(255) not null unique,
	password varchar(255) not null
);

insert IGNORE into user (email, password) values ('pajkatt2013@163.com', 'Admin123');
