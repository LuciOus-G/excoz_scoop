-- upgrade --
CREATE TABLE IF NOT EXISTS "core_organizations" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "created" DATE NOT NULL  DEFAULT '2021-12-20T16:22:53.499830',
    "modified" DATE NOT NULL  DEFAULT '2021-12-20T16:22:53.499830',
    "name" VARCHAR(255) NOT NULL,
    "is_subscribe" BOOL NOT NULL  DEFAULT False,
    "date_expire" DATE
);;
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-20 16:22:53.499830';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 16:22:53.499830';
ALTER TABLE "core_orders" ADD "organization_id_id" BIGINT NOT NULL;
ALTER TABLE "core_orders" DROP COLUMN "name";
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 16:22:53.499830';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-20 16:22:53.499830';
ALTER TABLE "core_orders" ADD CONSTRAINT "fk_core_ord_core_org_4fd557cc" FOREIGN KEY ("organization_id_id") REFERENCES "core_organizations" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "core_orders" DROP CONSTRAINT "fk_core_ord_core_org_4fd557cc";
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-20 15:34:01.592702';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 15:34:01.592702';
ALTER TABLE "core_orders" ADD "name" VARCHAR(255) NOT NULL;
ALTER TABLE "core_orders" DROP COLUMN "organization_id_id";
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 15:34:01.592702';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-20 15:34:01.592702';
DROP TABLE IF EXISTS "core_organizations";
