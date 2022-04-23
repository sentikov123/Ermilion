CREATE USER admin WITH password 'postgres';
CREATE DATABASE prod_db;
GRANT ALL PRIVILEGES ON DATABASE prod_db TO admin;

CREATE TABLE main_category (id serial , name VARCHAR(20), slug VARCHAR(20), primary key(id));

CREATE TABLE main_post (id int,
                   title VARCHAR(20), slug VARCHAR(20),
                   text text, category int,
                   image VARCHAR(200), publish_date VARCHAR(20),
                   primary key(id),
                   constraint fk_category FOREIGN KEY (category) REFERENCES main_category (id));

INSERT INTO main_category(name, slug)
VALUES ('Интернет', 'internet'), ('Медицины', 'medicina'), ('Наука', 'nauka'),
 ('Технологии', 'tech'),  ('Прогресс', 'progress'),  ('Автомобили', 'auto'),  ('Гаджеты', 'gadjets');

