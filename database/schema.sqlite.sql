create table quotes (
	id integer primary key,
	body text,
	submitted_at timestamp,
	approved boolean default false
);
