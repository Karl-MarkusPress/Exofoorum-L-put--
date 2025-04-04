CREATE TABLE users (
    id serial PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL
);

INSERT INTO users (username, password) VALUES ('Karl', 'Karl200412!')
