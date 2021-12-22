-- upgrade --
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-21 18:21:46.253654';
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-21 18:21:46.253654';
CREATE TABLE IF NOT EXISTS "glob_user_organizations" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "organization_id" BIGINT NOT NULL REFERENCES "core_organizations" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "glob_users" ("id") ON DELETE CASCADE
);;
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-21 18:21:46.253654';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-21 18:21:46.253654';
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-22 01:21:46.257651';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-21 18:21:46.253654';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-21 18:21:46.253654';
-- downgrade --
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-21 18:21:31.050812';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-21 18:21:31.050812';
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-22 01:21:31.054798';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-21 18:21:31.050812';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-21 18:21:31.050812';
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-21 18:21:31.050812';
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-21 18:21:31.050812';
DROP TABLE IF EXISTS "glob_user_organizations";
