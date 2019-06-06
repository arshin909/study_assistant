CREATE SEQUENCE "public"."courses_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

CREATE SEQUENCE "public"."groups_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

CREATE SEQUENCE "public"."lessons_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

CREATE SEQUENCE "public"."media_resources_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

CREATE SEQUENCE "public"."semesters_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

CREATE SEQUENCE "public"."students_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

CREATE TABLE "public"."courses" (
  "id" int4 NOT NULL DEFAULT nextval('courses_id_seq'::regclass),
  "name" text COLLATE "pg_catalog"."default" NOT NULL,
  "semester_id" int4 NOT NULL,
  CONSTRAINT "courses_pkey" PRIMARY KEY ("id")
)
;

ALTER TABLE "public"."courses" OWNER TO "postgres";

CREATE TABLE "public"."group-cource_rels" (
  "group_id" int4 NOT NULL,
  "cource_id" int4 NOT NULL,
  CONSTRAINT "group-cource_rels_group_id_cource_id_pk" PRIMARY KEY ("group_id", "cource_id")
)
;

ALTER TABLE "public"."group-cource_rels" OWNER TO "postgres";

CREATE TABLE "public"."groups" (
  "id" int4 NOT NULL DEFAULT nextval('groups_id_seq'::regclass),
  "name" text COLLATE "pg_catalog"."default" NOT NULL,
  CONSTRAINT "groups_pkey" PRIMARY KEY ("id")
)
;

ALTER TABLE "public"."groups" OWNER TO "postgres";

CREATE TABLE "public"."lesson-media_resources_rels" (
  "lesson_id" int4 NOT NULL,
  "media_resource_id" int4 NOT NULL,
  CONSTRAINT "lesson-media_resources_rels_lesson_id_media_resource_id_pk" PRIMARY KEY ("lesson_id", "media_resource_id")
)
;

ALTER TABLE "public"."lesson-media_resources_rels" OWNER TO "postgres";

CREATE TABLE "public"."lessons" (
  "id" int4 NOT NULL DEFAULT nextval('lessons_id_seq'::regclass),
  "group_id" int4 NOT NULL,
  "cource_id" int4 NOT NULL,
  "date_time" timestamp(6) NOT NULL DEFAULT now(),
  CONSTRAINT "lessons_pkey" PRIMARY KEY ("id")
)
;

ALTER TABLE "public"."lessons" OWNER TO "postgres";

CREATE TABLE "public"."media_resources" (
  "id" int4 NOT NULL DEFAULT nextval('media_resources_id_seq'::regclass),
  "name" text COLLATE "pg_catalog"."default" NOT NULL,
  "path" text COLLATE "pg_catalog"."default" NOT NULL,
  CONSTRAINT "media_resources_pkey" PRIMARY KEY ("id")
)
;

ALTER TABLE "public"."media_resources" OWNER TO "postgres";

CREATE TABLE "public"."semesters" (
  "id" int4 NOT NULL DEFAULT nextval('semesters_id_seq'::regclass),
  "start_date" date DEFAULT now(),
  "duration" int4 NOT NULL DEFAULT 182,
  CONSTRAINT "semesters_pkey" PRIMARY KEY ("id")
)
;

ALTER TABLE "public"."semesters" OWNER TO "postgres";

COMMENT ON COLUMN "public"."semesters"."duration" IS 'days';

CREATE TABLE "public"."student_performance" (
  "student_id" int4 NOT NULL,
  "lesson_id" int4 NOT NULL,
  "points" int4 NOT NULL DEFAULT 0,
  CONSTRAINT "student_performance_student_id_lesson_id_pk" PRIMARY KEY ("student_id", "lesson_id")
)
;

ALTER TABLE "public"."student_performance" OWNER TO "postgres";

CREATE TABLE "public"."student_visits" (
  "student_id" int4 NOT NULL,
  "lesson_id" int4 NOT NULL,
  "visited" bool NOT NULL DEFAULT true,
  CONSTRAINT "table_name_student_id_lesson_id_pk" PRIMARY KEY ("student_id", "lesson_id")
)
;

ALTER TABLE "public"."student_visits" OWNER TO "postgres";

CREATE TABLE "public"."students" (
  "id" int4 NOT NULL DEFAULT nextval('students_id_seq'::regclass),
  "group_id" int4 NOT NULL,
  "first_name" text COLLATE "pg_catalog"."default" NOT NULL,
  "last_name" text COLLATE "pg_catalog"."default" NOT NULL,
  "patronymic" text COLLATE "pg_catalog"."default",
  "gradebook_identy" text COLLATE "pg_catalog"."default" NOT NULL,
  CONSTRAINT "students_pkey" PRIMARY KEY ("id")
)
;

ALTER TABLE "public"."students" OWNER TO "postgres";

CREATE TABLE "public"."tg_chats" (
  "id" int4 NOT NULL,
  "student_id" int4
)
;

ALTER TABLE "public"."tg_chats" OWNER TO "postgres";

COMMENT ON COLUMN "public"."tg_chats"."id" IS 'chat id';

ALTER TABLE "public"."courses" ADD CONSTRAINT "courses_semesters_id_fk" FOREIGN KEY ("semester_id") REFERENCES "public"."semesters" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."group-cource_rels" ADD CONSTRAINT "group-cource_rels_courses_id_fk" FOREIGN KEY ("cource_id") REFERENCES "public"."courses" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."group-cource_rels" ADD CONSTRAINT "group-cource_rels_groups_id_fk" FOREIGN KEY ("group_id") REFERENCES "public"."groups" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."lesson-media_resources_rels" ADD CONSTRAINT "lesson-media_resources_rels_lessons_id_fk" FOREIGN KEY ("lesson_id") REFERENCES "public"."lessons" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."lesson-media_resources_rels" ADD CONSTRAINT "lesson-media_resources_rels_media_resources_id_fk" FOREIGN KEY ("media_resource_id") REFERENCES "public"."media_resources" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."lessons" ADD CONSTRAINT "lessons_courses_id_fk" FOREIGN KEY ("cource_id") REFERENCES "public"."courses" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."lessons" ADD CONSTRAINT "lessons_groups_id_fk" FOREIGN KEY ("group_id") REFERENCES "public"."groups" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."student_performance" ADD CONSTRAINT "student_performance_lessons_id_fk" FOREIGN KEY ("lesson_id") REFERENCES "public"."lessons" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."student_performance" ADD CONSTRAINT "student_performance_students_id_fk" FOREIGN KEY ("student_id") REFERENCES "public"."students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."student_visits" ADD CONSTRAINT "table_name_lessons_id_fk" FOREIGN KEY ("lesson_id") REFERENCES "public"."lessons" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."student_visits" ADD CONSTRAINT "table_name_students_id_fk" FOREIGN KEY ("student_id") REFERENCES "public"."students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."students" ADD CONSTRAINT "students_groups_id_fk" FOREIGN KEY ("group_id") REFERENCES "public"."groups" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE "public"."tg_chats" ADD CONSTRAINT "tg_chats_students_id_fk" FOREIGN KEY ("student_id") REFERENCES "public"."students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

SELECT setval('"public"."courses_id_seq"', 2, true);

ALTER SEQUENCE "public"."courses_id_seq"
OWNED BY "public"."courses"."id";

ALTER SEQUENCE "public"."courses_id_seq" OWNER TO "postgres";

SELECT setval('"public"."groups_id_seq"', 2, true);

ALTER SEQUENCE "public"."groups_id_seq"
OWNED BY "public"."groups"."id";

ALTER SEQUENCE "public"."groups_id_seq" OWNER TO "postgres";

SELECT setval('"public"."lessons_id_seq"', 1, true);

ALTER SEQUENCE "public"."lessons_id_seq"
OWNED BY "public"."lessons"."id";

ALTER SEQUENCE "public"."lessons_id_seq" OWNER TO "postgres";

SELECT setval('"public"."media_resources_id_seq"', 1, true);

ALTER SEQUENCE "public"."media_resources_id_seq"
OWNED BY "public"."media_resources"."id";

ALTER SEQUENCE "public"."media_resources_id_seq" OWNER TO "postgres";

SELECT setval('"public"."semesters_id_seq"', 1, true);

ALTER SEQUENCE "public"."semesters_id_seq"
OWNED BY "public"."semesters"."id";

ALTER SEQUENCE "public"."semesters_id_seq" OWNER TO "postgres";

SELECT setval('"public"."students_id_seq"', 5, true);

ALTER SEQUENCE "public"."students_id_seq"
OWNED BY "public"."students"."id";

ALTER SEQUENCE "public"."students_id_seq" OWNER TO "postgres";

CREATE UNIQUE INDEX "courses_id_uindex" ON "public"."courses" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

CREATE UNIQUE INDEX "courses_name_semester_id_uindex" ON "public"."courses" USING btree (
  "name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "semester_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

CREATE UNIQUE INDEX "group-cource_rels_group_id_cource_id_uindex" ON "public"."group-cource_rels" USING btree (
  "group_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "cource_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

CREATE UNIQUE INDEX "groups_id_uindex" ON "public"."groups" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

CREATE UNIQUE INDEX "groups_name_uindex" ON "public"."groups" USING btree (
  "name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

CREATE UNIQUE INDEX "lesson-media_resources_rels_lesson_id_media_resource_id_uindex" ON "public"."lesson-media_resources_rels" USING btree (
  "lesson_id" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "media_resource_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

CREATE UNIQUE INDEX "lessons_id_uindex" ON "public"."lessons" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

CREATE UNIQUE INDEX "semesters_id_uindex" ON "public"."semesters" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

CREATE UNIQUE INDEX "students_id_uindex" ON "public"."students" USING btree (
  "id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

ALTER TABLE students ADD COLUMN telegram_id varchar(15) NOT NULL;
ALTER TABLE students ADD CONSTRAINT telegram_id_unique UNIQUE(telegram_id);
CREATE UNIQUE INDEX telegram_id_index ON students(telegram_id);

CREATE SEQUENCE "public"."teachers_id_seq"

CREATE TABLE "public"."teachers" (
  "id" int4 NOT NULL DEFAULT nextval('teachers_id_seq'::regclass),
  "first_name" text COLLATE "pg_catalog"."default" NOT NULL,
  "last_name" text COLLATE "pg_catalog"."default" NOT NULL,
  "telegram_id" text COLLATE "pg_catalog"."default" NOT NULL,
  CONSTRAINT "teachers_pkey" PRIMARY KEY ("id")
)

ALTER TABLE teachers ADD CONSTRAINT teachers_telegram_id_unique UNIQUE(telegram_id);
ALTER TABLE semesters DROP COLUMN duration
ALTER TABLE courses ADD COLUmn duration integer
ALTER TABLE courses ADD COLUmn author integer
ALTER TABLE "public"."courses" ADD CONSTRAINT "courses_author_id_fk" FOREIGN KEY ("author") REFERENCES "public"."teachers" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE teachers add column patronymic text;