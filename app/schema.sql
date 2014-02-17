drop table if exists twitter;
drop table if exists github;


create table twitter (
	id integer primary key autoincrement,
	url string not null,
    image_url string not null,
    excerpt string not null,
    source string not null,
    updated timestamp not null,
    last_refresh timestamp not null,
    title string);

create table github (
		id integer primary key autoincrement,
		url string not null,
        image_url string not null,
        excerpt string not null,
        updated timestamp not null,
        last_refresh timestamp not null,
        title string,
        author string);
        	 
