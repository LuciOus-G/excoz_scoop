-- upgrade --
ALTER TABLE "core_orders" DROP CONSTRAINT "fk_core_ord_core_org_4fd557cc";
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-20 16:24:23.466237';
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 16:24:23.466237';
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-20 16:24:23.466237';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 16:24:23.466237';
ALTER TABLE "core_orders" RENAME COLUMN "organization_id_id" TO "organization_id";
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-20 16:24:23.466237';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 16:24:23.466237';
ALTER TABLE "core_orders" ADD CONSTRAINT "fk_core_ord_core_org_18dd28f9" FOREIGN KEY ("organization_id") REFERENCES "core_organizations" ("id") ON DELETE CASCADE;
-- downgrade --
ALTER TABLE "core_orders" DROP CONSTRAINT "fk_core_ord_core_org_18dd28f9";
ALTER TABLE "glob_users" ALTER COLUMN "created" SET DEFAULT '2021-12-20 16:23:36.288283';
ALTER TABLE "glob_users" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 16:23:36.288283';
ALTER TABLE "core_orders" RENAME COLUMN "organization_id" TO "organization_id_id";
ALTER TABLE "core_orders" ALTER COLUMN "created" SET DEFAULT '2021-12-20 16:23:36.288283';
ALTER TABLE "core_orders" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 16:23:36.288283';
ALTER TABLE "core_organizations" ALTER COLUMN "created" SET DEFAULT '2021-12-20 16:23:36.288283';
ALTER TABLE "core_organizations" ALTER COLUMN "modified" SET DEFAULT '2021-12-20 16:23:36.288283';
ALTER TABLE "core_orders" ADD CONSTRAINT "fk_core_ord_core_org_4fd557cc" FOREIGN KEY ("organization_id_id") REFERENCES "core_organizations" ("id") ON DELETE CASCADE;
