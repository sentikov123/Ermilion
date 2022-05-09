CREATE USER admin WITH password 'postgres';
CREATE DATABASE prod_db;
GRANT ALL PRIVILEGES ON DATABASE prod_db TO admin;

