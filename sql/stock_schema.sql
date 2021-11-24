create database if not exists stockdata; -- this is the main database
use stockdata;

create table if not exists tickers (
	tickerid int primary key not null auto_increment,
	ticker varchar(50) not null,
	constraint unique_ticker unique(ticker)
);

create table if not exists dates (
	dateid int primary key not null auto_increment,
	datestring int not null,
    constraint unique_datestring unique(datestring)
);

/*
	The table holding the main stock information.
*/
create table if not exists pricedata (
	tickerid int not null,
	dateid int not null,
	openbid float not null,
	openask float not null,
	closebid float not null,
	closeask float not null,
	volume bigint not null,
	primary key(tickerid, dateid),
	CONSTRAINT `fk_ticker`
    	FOREIGN KEY (tickerid) REFERENCES tickers (tickerid),
	CONSTRAINT `fk_date`
    	FOREIGN KEY (dateid) REFERENCES dates (dateid)
);

create table if not exists all_data (
    datestring varchar(50) not null,
    ticker varchar(50) not null,
    openbid float null,
    high float null,
    low float null,
    closebid float null,
    volume float null,
    dividends float null,
    splits float null,
    obv float null,
    macd float null,
    macd_trend float null,
    rsi float null,
    primary key(datestring, ticker)
);