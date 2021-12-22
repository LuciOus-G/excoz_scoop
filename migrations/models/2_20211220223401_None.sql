-- upgrade --
CREATE TABLE IF NOT EXISTS "glob_users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "created" DATE NOT NULL  DEFAULT '2021-12-20T15:34:01.592702',
    "modified" DATE NOT NULL  DEFAULT '2021-12-20T15:34:01.592702',
    "first_name" VARCHAR(25) NOT NULL,
    "last_name" VARCHAR(20) NOT NULL,
    "email" VARCHAR(250) NOT NULL UNIQUE,
    "password" VARCHAR(512) NOT NULL,
    "salt" VARCHAR(512) NOT NULL,
    "origin_scoop" INT NOT NULL,
    "phone_number" VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS "core_orders" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "created" DATE NOT NULL  DEFAULT '2021-12-20T15:34:01.592702',
    "modified" DATE NOT NULL  DEFAULT '2021-12-20T15:34:01.592702',
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
