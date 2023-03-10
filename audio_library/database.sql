create table program (
    id integer primary key,
    name text not null,
    audio_data bytea not null
);

create table music (
    id integer not null references program(id),
    genre text not null
);

create table queue (
    pos integer primary key,
    program_id integer not null references program(id)
);

create table news_scraped(
    title text primary key,
    time integer not null
);

create sequence serial_num;
