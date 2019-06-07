INSERT INTO "public"."semesters"("id", "start_date", "duration") VALUES (1, '2019-05-17', 182);

INSERT INTO "public"."groups"("id", "name") VALUES (1, '[test]Group1');

INSERT INTO "public"."groups"("id", "name") VALUES (2, '[test]Group2');

INSERT INTO "public"."students"("id", "group_id", "first_name", "last_name", "patronymic", "gradebook_identy") VALUES (1, 1, 'Александр', 'Иванов', 'Александрович', 'г1-1');

INSERT INTO "public"."students"("id", "group_id", "first_name", "last_name", "patronymic", "gradebook_identy") VALUES (2, 1, 'Дмитрий', 'Смирнов', 'Иванович', 'г1-2');

INSERT INTO "public"."students"("id", "group_id", "first_name", "last_name", "patronymic", "gradebook_identy") VALUES (3, 2, 'Максим', 'Кузнецов', 'Александрович', 'г2-1');

INSERT INTO "public"."students"("id", "group_id", "first_name", "last_name", "patronymic", "gradebook_identy") VALUES (4, 2, 'Сергей', 'Попов', 'Кикторович', 'г2-2');

INSERT INTO "public"."students"("id", "group_id", "first_name", "last_name", "patronymic", "gradebook_identy") VALUES (5, 2, 'Ыксан', 'Гежулба', NULL, 'г2-3');

INSERT INTO "public"."courses"("id", "name", "semester_id") VALUES (1, 'Теория', 1);

INSERT INTO "public"."courses"("id", "name", "semester_id") VALUES (2, 'Практика', 1);

INSERT INTO "public"."group-cource_rels"("group_id", "cource_id") VALUES (1, 1);

INSERT INTO "public"."media_resources"("id", "name", "path") VALUES (1, 'Лекция1.pdf', 'files\{guid}');

INSERT INTO "public"."lessons"("id", "group_id", "cource_id", "date_time") VALUES (1, 1, 1, '2019-05-17 13:47:45.061016');

INSERT INTO "public"."lesson-media_resources_rels"("lesson_id", "media_resource_id") VALUES (1, 1);
