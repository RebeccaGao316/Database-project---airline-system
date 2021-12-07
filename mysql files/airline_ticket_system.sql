

create table airline(
name varchar(20),
primary key (name)
);

create table airplane(
iden_num varchar(5),
airline_name varchar(20),
number_seat numeric(4,0) not null,
primary key (iden_num, airline_name),
foreign key (airline_name) references airline(name)
);

create table staff(
username varchar(20),
password varchar(64) not null,
first_name varchar(20),
last_name varchar(20),
date_of_birth date,
airline_name varchar(20) not null,
primary key (username),
foreign key (airline_name) references airline(name)
);

create table staff_phone(
username varchar(20),
phone_num varchar(20) not null,
primary key (username, phone_num),
foreign key (username) references staff(username));

create table airport(
code varchar(5),
name varchar(10) not null,
city varchar(20),
primary key (code)
);

create table customer(
email varchar(40),
name varchar(40) not null,
password varchar(64) not null,
building_num varchar(5),
street varchar(20),
city varchar(20),
state varchar(5),
phone_num varchar(20),
passport_num varchar(20),
passport_exp date,
passport_country varchar(20),
date_of_birth date,
primary key (email)
);



create table flight(
airline_name varchar(20),
d_date date,
d_time time,
flight_num varchar(5),
a_date date,
a_time time,
base_price numeric(5,2) not null,
status varchar(10),
airplane_i_num varchar(5) not null,
arr_airport_code varchar(5),
dep_airport_code varchar(5),
primary key (airline_name, d_date, d_time, flight_num),
foreign key (airline_name) references airline(name),
foreign key (airplane_i_num) references airplane(iden_num),
foreign key (arr_airport_code) references airport(code),
foreign key (dep_airport_code) references airport(code)
);


create table rate(
airline_name varchar(20),
d_date date,
d_time time,
flight_num varchar(5),
customer_email varchar(30),
comment varchar(200),
star numeric(1,0),
primary key (airline_name, d_date, d_time, flight_num, customer_email),
foreign key (airline_name, d_date, d_time, flight_num) references flight(airline_name, d_date, d_time, flight_num),
foreign key (customer_email) references customer(email)
);


create table ticket(
tID int,
sold_price numeric(5,2),
card_type varchar(10),
card_num varchar(20),
expire_date date,
purchase_date date,
purchase_time time,
airline_name varchar(20) not null,
d_date date not null,
d_time time not null,
flight_num varchar(5),
customer_email varchar(30),
primary key (tID),
foreign key (airline_name, d_date, d_time, flight_num) references flight(airline_name, d_date, d_time, flight_num),
foreign key (customer_email) references customer(email)
);
