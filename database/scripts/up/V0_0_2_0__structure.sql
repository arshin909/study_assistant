ALTER TABLE "public"."media_resources" ALTER COLUMN "path" DROP NOT NULL;

CREATE TABLE "public"."tg_file_storage" (
  "file_id" text COLLATE "pg_catalog"."default" NOT NULL,
  "date_time" timestamp(6) NOT NULL DEFAULT now(),
  "media_resource_id" int4 NOT NULL,
  CONSTRAINT "tg_file_storage_pkey" PRIMARY KEY ("file_id")
)
;

ALTER TABLE "public"."tg_file_storage" OWNER TO "postgres";

ALTER TABLE "public"."tg_file_storage" ADD CONSTRAINT "tg_file_storage_media_resources_id_fk" FOREIGN KEY ("media_resource_id") REFERENCES "public"."media_resources" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

CREATE UNIQUE INDEX "tg_file_storage_date_time_media_resource_id_uindex" ON "public"."tg_file_storage" USING btree (
  "date_time" "pg_catalog"."timestamp_ops" ASC NULLS LAST,
  "media_resource_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

CREATE UNIQUE INDEX "tg_file_storage_file_id_uindex" ON "public"."tg_file_storage" USING btree (
  "file_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);