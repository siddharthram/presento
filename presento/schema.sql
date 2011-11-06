drop table if exists entries;

create table preso (
	id integer primary key autoincrement,
	creator string not null,
	pagecount integer not null
	);
	
create table content (
	id integer primary key autoincrement,
	pagenumber integer not null,
	presenter integer not null,
	FOREIGN KEY(presenter) REFERENCES preso(id)
	);
	