-- upgrade --
ALTER TABLE "core_organizations" ADD "folder_id" VARCHAR(255);
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-22 17:14:00.417721';
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-22 17:14:00.417721';
ALTER TABLE "core_organizations" ALTER COLUMN "org_logo" SET DEFAULT 'https://firebasestorage.googleapis.com/v0/b/worka-eshier.appspot.com/o/default_profil_pic.jpg?alt=media&token=80eca9c8-4a81-4fd1-a6c2-8d23ea87670e';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-22 17:14:00.417721';
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-22 17:14:00.417721';
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-23 00:14:00.421731';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-22 17:14:00.417721';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-22 17:14:00.417721';
-- downgrade --
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-22 11:31:16.761973';
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-22 11:31:16.761973';
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-22 18:31:16.764971';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-22 11:31:16.761973';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-22 11:31:16.761973';
ALTER TABLE "core_organizations" DROP COLUMN "folder_id";
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-22 11:31:16.761973';
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-22 11:31:16.761973';
ALTER TABLE "core_organizations" ALTER COLUMN "org_logo" DROP DEFAULT;
