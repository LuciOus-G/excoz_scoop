-- upgrade --
ALTER TABLE "core_organizations" ADD "prefix" VARCHAR(255)  UNIQUE;
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-23 10:09:25.477605';
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 10:09:25.477605';
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-23 10:09:25.477605';
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-23 17:09:25.482603';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 10:09:25.477605';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-23 10:09:25.477605';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 10:09:25.477605';
-- downgrade --
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-22 18:15:20.020665';
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-23 01:15:20.023664';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-22 18:15:20.020665';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-22 18:15:20.020665';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-22 18:15:20.020665';
ALTER TABLE "core_organizations" DROP COLUMN "prefix";
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-22 18:15:20.020665';
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-22 18:15:20.020665';
