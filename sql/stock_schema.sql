create database if not exists stockdata; -- this is the main database
use stockdata;

create table if not exists tickers (
	tickerid int primary key not null,
	ticker varchar(50) not null
);

create table if not exists dates (
	dateid int primary key not null,
	datestring int not null
);

/*
	The table holding the main stock information.
*/
create table if not exists pricedata (
	tickerid int primary key not null,
	dateid int primary key not null,
	openbid float not null,
	openask float not null,
	closebid float not null,
	closeask float not null,
	volume int not null,
	CONSTRAINT `fk_ticker`
    	FOREIGN KEY (tickerid) REFERENCES tickers (tickerid),
	CONSTRAINT `fk_date`
    	FOREIGN KEY (dateid) REFERENCES tickers (dateid)
);

