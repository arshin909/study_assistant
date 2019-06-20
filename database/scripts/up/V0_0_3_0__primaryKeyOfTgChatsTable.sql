create unique index tg_chats_id_student_id_uindex
	on tg_chats (id, student_id);

alter table tg_chats
	add constraint tg_chats_pk
		primary key (id, student_id);