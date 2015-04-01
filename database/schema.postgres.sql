create table quotes (
	id serial primary key,
	body text,
	submitted_at timestamp,
	approved boolean default false
);
