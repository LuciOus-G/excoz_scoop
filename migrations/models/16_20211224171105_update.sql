-- upgrade --
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-24 10:11:05.139579';
ALTER TABLE "core_organizations" ALTER COLUMN "org_logo" SET DEFAULT 'https://firebasestorage.googleapis.com/v0/b/worka-eshier.appspot.com/o/default_profil_pic.jpg?alt=media&token=80eca9c8-4a81-4fd1-a6c2-8d23ea87670e';
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-24 10:11:05.139579';
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-24 10:11:05.139579';
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-24 17:11:05.142577';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-24 10:11:05.139579';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-24 10:11:05.139579';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-24 10:11:05.139579';
-- downgrade --
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-23 20:00:02.509716';
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-24 03:00:02.512727';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 20:00:02.509716';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-23 20:00:02.509716';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 20:00:02.509716';
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-23 20:00:02.509716';
ALTER TABLE "core_organizations" ALTER COLUMN "org_logo" DROP DEFAULT;
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 20:00:02.509716';
