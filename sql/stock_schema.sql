create database if not exists stockdata;
use stockdata;
create table if not exists pricedata (
	ticker varchar(50) primary key not null,
	date int not null,
	openbid float not null,
	openask float not null,
	closebid float not null,
	closeask float not null,
	volume int not null
);
