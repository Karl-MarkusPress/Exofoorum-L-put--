CREATE TABLE users (
    id serial PRIMARY KEY,
    username text NOT NULL,
    password text NOT NULL
);
INSERT INTO users (username, password)
VALUES ('Karl', 'Karl200412!') 

CREATE TABLE posts (
        id serial PRIMARY KEY,
        CreatorID int4 NOT NULL references users(id),
        Title text NOT NULL,
        Comments text NOT NULL
    );
CREATE TABLE Wiki(
    id serial PRIMARY KEY,
    CreatorID int4 NOT NULL references users(id),
    Content text NOT NULL,
    Species text NOT NULL
);
CREATE TABLE Comments (
    id serial PRIMARY KEY,
    CreatorID int4 NOT NULL references users(id),
    Comments text NOT NULL,
    PostID int4 NOT NULL references posts(id)
);
CREATE TABLE images(
    id serial PRIMARY KEY,
    PostID int4 references posts(id),
    Title text NOT NULL,
    WikiPageContentID int4 references Wiki(id),
    CommentsID int4 references Comments(id),
    Contents bytea NOT NULL
);