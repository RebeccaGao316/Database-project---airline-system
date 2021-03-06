insert into airline values('China Eastern');
	insert into airline values('Air Canada');


	insert into airport values('10000', 'JFK', 'New York');
	insert into airport values('10001', 'PVG', 'Shanghai'); 


	insert into customer values(
		'xg681@nyu.edu',
		'Xinyu Gao',
		 md5('12345'),
		'370',
		'Jay Street',
		'New York',
		'NY',
		'(100)000-0001',
		'E10000001',
		'2030-10-30',
		'China',
		'2001-1-1'
	);

	insert into customer values(
		'xl2457@nyu.edu',
		'Anthony Lu',
		md5('12346'),
		'370',
		'Jay Street',
		'New York',
		'NY',
		'(100)000-0002',
		'E10000002',
		'2030-10-29',
		'China',
		'2001-2-1'
	);

	insert into customer values(
		'zl2728@nyu.edu',
		'Zhilue Li',
		md5('12347'),
		'370',
		'Jay Street',
		'New York',
		'NY',
		'(100)000-0003',
		'E10000003',
		'2030-10-28',
		'China',
		'2001-3-1'
	);


	insert into airplane values(
		'A01',
		'China Eastern',
		1000
	);
	
	insert into airplane values(
		'A01',
		'Air Canada',
		500
	);
	
	insert into airplane values(
		'A02',
		'China Eastern',
		900
	);


	insert into staff values(
		'abc12',
		md5('11223'),
		'Jack',
		'Lee',
		'1990-10-1',
		'China Eastern'
	);

	insert into staff_phone values(
		'abc12',
		'(200)100-1001'
	);
	

	insert into flight values(
		'China Eastern',
		'2021-11-13',
		'10:30:00',
		'MU123',
		'2021-11-14',
		'18:30:00',
		780.34,
		'on-time',
		'A01',
		'10000',
		'10001'
	);

	insert into flight values(
		'China Eastern',
		'2021-11-15',
		'16:20:00',
		'MU124',
		'2021-11-15',
		'15:20:00',
		760.34,
		'delayed',
		'A02',
		'10001',
		'10000'
	);

	insert into flight values(
		'Air Canada',
		'2021-11-17',
		'16:00:00',
		'AC176',
		'2021-11-18',
		'16:45:00',
		810.23,
		'delayed',
		'A01',
		'10000',
		'10001'
	);


	insert into ticket values(
		0,
		850.33,
		'credit',
		'1111 2222 3333 4444',
		'2024-12-1',
		'2021-9-6',
		'18:00:30',
		'China Eastern',
		'2021-11-13',
		'10:30:00',
		'MU123',
		'xg681@nyu.edu'
	);

	insert into ticket values(
		1,
		920.67,
		'credit',
		'1111 2222 3333 4445',
		'2024-12-30',
		'2021-9-21',
		'13:00:30',
		'China Eastern',
		'2021-11-15',
		'16:20:00',
		'MU124',
		'xl2457@nyu.edu'
	);

	insert into ticket values(
		2,
		723.13,
		'debit',
		'1111 2222 3333 4446',
		'2024-12-15',
		'2021-10-6',
		'8:00:30',
		'Air Canada',
		'2021-11-17',
		'16:00:00',
		'AC176',
		'zl2728@nyu.edu'
	);
	