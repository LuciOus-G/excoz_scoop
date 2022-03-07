-- upgrade --
ALTER TABLE "core_organizations" ALTER COLUMN "org_logo" DROP DEFAULT;
ALTER TABLE "core_organizations" ALTER COLUMN "org_logo" DROP NOT NULL;
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-23 18:33:29.422361';
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 18:33:29.422361';
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-24 01:33:29.425359';
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-23 18:33:29.422361';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 18:33:29.422361';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-23 18:33:29.422361';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 18:33:29.422361';
-- downgrade --
ALTER TABLE "glob_users" ALTER COLUMN "last_login" SET DEFAULT '2021-12-23 17:09:31.586446';
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-23 10:09:31.582447';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 10:09:31.582447';
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-23 10:09:31.582447';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 10:09:31.582447';
ALTER TABLE "core_organizations" ALTER COLUMN "org_logo" SET NOT NULL;
ALTER TABLE "core_organizations" ALTER COLUMN "org_logo" SET DEFAULT 'https://firebasestorage.googleapis.com/v0/b/worka-eshier.appspot.com/o/default_profil_pic.jpg?alt=media&token=80eca9c8-4a81-4fd1-a6c2-8d23ea87670e';
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-23 10:09:31.582447';
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-23 10:09:31.582447';
