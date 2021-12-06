
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import date

app = Flask(__name__)
#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='air_ticket_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
@app.route('/')
def hello():
    return render_template('publicHomepage.html')

#Define route for customer register
@app.route('/customerRegister')
def customerRegister():
    return render_template('customerRegister.html')
#Define route for staff register
@app.route('/staffRegister')
def staffRegister():
    return render_template('staffRegister.html')


#Define route for customer login
@app.route('/customerLogin', methods=['GET', 'POST'])
def customerLogin():
    print("wehere")
    if(session.get('username')):
        return redirect(url_for('customerHome'))
    else:
        return render_template('customerLogin.html')
#Define route for staff login
@app.route('/staffLogin')
def staffLogin():
    return render_template('staffLogin.html')

@app.route('/publicCheck')
def publicCheck():
    return render_template('publicCheck.html')

@app.route('/flightSearch')
def flightSearch():
    return render_template('flightSearch.html')

@app.route('/roundFlightSearch')
def roundFlightSearch():
    return render_template('roundFlightSearch.html')

@app.route('/pastFlightStatus')
def pastFlightStatus():
    return render_template('pastFlightStatus.html')

@app.route('/staffHome')
def staffHome():
    return render_template('staffHome.html')

@app.route('/viewFlights')
def viewFlights():
    return render_template('viewFlights.html')

@app.route('/viewTopDes')
def viewTopDes():
    return render_template('topDest.html')

@app.route('/viewRevenue')
def viewRevenue():
    return render_template('staffViewRevenue.html')

@app.route('/addAirplane')
def addAirplane():
    return render_template('addAirplane.html')

@app.route('/customerHome')
def customerHome():
    return render_template('customerHome.html')

@app.route('/createFlight')
def createFlight():
    return render_template('createFlight.html')

@app.route('/changeFlightStatus')
def changeFlightStatus():
    return render_template('changeFlightStatus.html')

@app.route('/flightView')
def flightView():
    return render_template('customerView.html')

@app.route('/customerFlightSearch')
def customerFlightSearch():
    return render_template('customerSearch.html')



@app.route('/flightRate')
def flightRate():
    return render_template('customerRate.html')

@app.route('/moneyTrack')
def moneyTrack():
    return render_template('customerSpending.html')

@app.route('/viewFlightRatings')
def viewFlightRatings():
    return render_template('viewFlightRatings.html')

@app.route('/viewFrequentCustomer')
def viewFrequentCustomer():
    return render_template('viewFrequentCustomer.html')

@app.route('/viewReports')
def viewReports():
    return render_template('viewTicketReport.html')

@app.route('/addAirport')
def addAirport():
    return render_template('addAirport.html')


#Authenticates the register
#the username is a email
@app.route('/customerRegisterAuth', methods=['GET', 'POST'])
def customerRegisterAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['userpassword']
    name = request.form['name']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE email = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    error = None
#use fetchall() if you are expecting more than 1 data row
    if(data):
        #If the previous query returns data, then user exists
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, md5(%s), null,null,null, null,null,null, null,null,null)'
        cursor.execute(ins, (username, name, password))
        conn.commit()
        cursor.close()
        return render_template('publicHomepage.html')


@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staffRegisterAuth():
    #grabs information from the forms
    username = request.form['staffname']
    password = request.form['staffpassword']
    airlineName = request.form['airlineName']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM staff WHERE username = md5(%s)'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    if(data):
        #If the previous query returns data, then user exists
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = 'INSERT INTO staff VALUES(%s, md5(%s),null,null,null,%s)'
        cursor.execute(ins, (username, password, airlineName))
        conn.commit()
        cursor.close()
        return render_template('publicHomepage.html')


#Authenticates the register
#the username is a email
@app.route('/customerLoginAuth', methods=['GET', 'POST'])
def customerLoginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in ??
        session['username'] = username
        return redirect(url_for('customerHome'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('customerLogin.html', error=error)


@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM staff WHERE username = %s and password = md5(%s)'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in ??
        session['username'] = username
        return redirect(url_for('staffHome'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('staffLogin.html', error=error)

@app.route('/flightSearchProcess', methods=['GET', 'POST'])
def flightSearchProcess():
    if(session.get('username') == True):
        username = session['username']


    #grabs information from the forms
    dep_date = request.form['dep_date']
    dep_airport = request.form['dep_airport']
    arr_airport = request.form['arr_airport']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM flight WHERE d_date = %s ' \
            'and dep_airport_code = (select code from airport where airport.name = %s) ' \
            'and arr_airport_code = (select code from airport where airport.name = %s)'

    cursor.execute(query, (dep_date,dep_airport,arr_airport))
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    if(session.get('username') == True):
        return render_template('flightSearch.html', username=username, posts=data1)
    return render_template('flightSearch.html',  posts=data1)

@app.route('/roundFlightSearchProcess', methods=['GET', 'POST'])
def roundFlightSearchProcess():

    username = session['username']

    #grabs information from the forms
    dep_date = request.form['dep_date']
    dep_airport = request.form['dep_airport']
    arr_airport = request.form['arr_airport']
    return_date = request.form['return_date']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query1 = 'SELECT * FROM flight WHERE d_date = %s ' \
            'and dep_airport_code = (select code from airport where airport.name = %s) ' \
            'and arr_airport_code = (select code from airport where airport.name = %s)'
    query2 = 'select * from flight where d_date = %s and ' \
            'dep_airport_code = (select code from airport where airport.name = %s) ' \
            'and arr_airport_code = (select code from airport where airport.name = %s)'

    cursor.execute(query1, (dep_date,dep_airport,arr_airport))
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.execute(query2, (return_date,arr_airport,dep_airport))
    #stores the results in a variable
    data2 = cursor.fetchall()
    for each in data2:
        print(each)
    cursor.close()
    return render_template('roundFlightSearch.html', username=username, posts1=data1, posts2 = data2)

@app.route('/statusSearchProcess', methods=['GET', 'POST'])
def statusSearchProcess():
    if(session.get('username') == True):
        username = session['username']

    #grabs information from the forms
    airlineName = request.form['airlineName']
    flightNum = request.form['flightNum']
    arrivalDate = request.form['arrivalDate']
    departureDate = request.form['departureDate']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM flight where airline_name = %s and flight_num = %s and a_date = %s and d_date = %s'

    cursor.execute(query, (airlineName,flightNum,arrivalDate,departureDate))
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    if(session.get('username') == True):
        return render_template('pastFlightStatus.html', username=username, posts=data1)
    return render_template('pastFlightStatus.html', posts=data1)


@app.route('/checkFutureFlights', methods=['GET', 'POST'])
def checkFutureFlights():
    username = session['username']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'select * from ticket where customer_email = %s and d_date > current_date or (d_date = current_date and d_time > current_time)'
    #stores the results in a variable
    cursor.execute(query,(username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('customerView.html', username=username, posts=data1)

@app.route('/purchaseTicket',methods=['GET', 'POST'])
def purchaseTicket():
    username = session['username']
    #grabs information from the forms
    airlineName = request.form['airlineName']
    flightNum = request.form['flightNum']
    departureTime = request.form['d_time']
    departureDate = request.form['d_date']
    cardType = request.form['cardType']
    cardNum = request.form['cardNum']
    expDate = request.form['expDate']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'select count(*) as number_seat from ticket natural join flight ' \
            'where flight_num = %s and airline_name = %s and d_date = %s and d_time = %s '
    #stores the results in a variable
    cursor.execute(query,(flightNum,airlineName,departureDate,departureTime))
    currentSell = cursor.fetchone()
    query = 'select distinct number_seat from flight natural join airline natural join airplane ' \
            'where flight_num = %s and airline_name = %s and d_date = %s and d_time = %s '
    cursor.execute(query,(flightNum,airlineName,departureDate,departureTime))
    totalNum = cursor.fetchone();
    query = 'select base_price from flight ' \
            'where flight_num = %s and airline_name = %s and d_date = %s and d_time = %s '
    cursor.execute(query,(flightNum,airlineName,departureDate,departureTime))
    basePrice = cursor.fetchone();
    basePrice = float(basePrice["base_price"])
    if(float(currentSell["number_seat"]) == float(totalNum["number_seat"])):
        return render_template('404.html')
    if(float(currentSell["number_seat"]) > 0.75 * float(totalNum["number_seat"])):
        price = 1.25*basePrice
    else:
        price = basePrice

    #query = 'INSERT INTO ticket (card_type,card_num,expire_date,purchase_date,' \
    #        'purchase_time,airline_name,d_date, d_time,flight_num,customer_email,sold_price,tID)'\
     #       'VALUES (%s,%s,%s,date.today(),datetime.now(),%s,%s,%s,%s,%s,100,20)'
    query = 'INSERT INTO ticket VALUES ((select (MAX(tID)+1) from ticket as t),%s,%s,%s,%s, current_date(),current_time() ,%s,%s,%s,%s,%s)'
    cursor.execute(query,(price,cardType,cardNum,expDate,airlineName,departureDate,departureTime,flightNum,username))
    conn.commit()
    cursor.close()
    return render_template('purchaseDone.html')



@app.route('/pastFlightHistory', methods=['GET', 'POST'])
def pastFlightHistory():

    username = session['username']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM ticket as t left outer join rate as r ' \
            'on (t.airline_name = r.airline_name and t.d_date = r.d_date and ' \
            't.d_time = r.d_time and t.flight_num = r.flight_num and ' \
            't.customer_email = r.customer_email)' \
            'WHERE t.customer_email = %s and ' \
            '(t.d_date < current_date() or (t.d_date = current_date() and t.d_time < current_time()))'

    cursor.execute(query, (username))
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('customerRate.html', username=username, posts=data1)
@app.route('/rateAndComment',methods=['GET', 'POST'])
def rateAndComment():
    username = session['username']
    #grabs information from the forms
    airlineName = request.form['airlineName']
    flightNum = request.form['flightNum']
    departureTime = request.form['d_time']
    departureDate = request.form['d_date']
    star = request.form['star']
    comment = request.form['comment']
    error = None


    #cursor used to send queries
    cursor = conn.cursor()
    #check 0 whether the info indicate a flight
    #check 1 whether there is no comment and star for this trip
    check0 = 'select * from ticket where customer_email = %s' \
             ' and airline_name = %s and d_date = %s and d_time = %s ' \
             'and flight_num = %s'
    cursor.execute(check0,(username, airlineName,departureDate,departureTime,flightNum))
    checkdata = cursor.fetchall()
    if(not checkdata):
        error = "This is not a valid flight"
        return render_template('customerRate.html', error = error)

    check1 = 'select * from rate where customer_email = %s' \
             ' and airline_name = %s and d_date = %s and d_time = %s ' \
             'and flight_num = %s'
    cursor.execute(check1,(username, airlineName,departureDate,departureTime,flightNum))
    checkdata = cursor.fetchall()
    if(checkdata):
        error = "You have already rate for this!"
        return render_template('customerRate.html', error = error)




    query = 'insert into rate VALUES(%s,%s,%s,%s,%s,%s,%s)'
    cursor.execute(query,(airlineName,departureDate,departureTime,flightNum,username,comment,star))
    conn.commit()
    cursor.close()
    return render_template('customerRate.html')

@app.route('/spendingPastYear', methods=['GET', 'POST'])
def spendingPastYear():

    username = session['username']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = ' select sum(sold_price) as sumPrice from ticket ' \
            'where customer_email  = %s and (purchase_date > current_date() - interval 1 year) '
    cursor.execute(query, username)
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('customerSpending.html', username=username, posts1=data1)


@app.route('/spendingInRange', methods=['GET', 'POST'])
def spendingInRange():

    username = session['username']
    beginDate = request.form['beginDate']
    endDate = request.form['endDate']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = ' select sum(sold_price) as sumPrice from ticket ' \
            'where customer_email  = %s and purchase_date >= %s and purchase_date <= %s '
    cursor.execute(query, (username,beginDate,endDate))
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('customerSpending.html', username=username, posts2=data1)


@app.route('/spendingChartDefault', methods=['GET', 'POST'])
def spendingChartDefault():

    username = session['username']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = ' select month(purchase_date) as m, year(purchase_date) as y, sum(sold_price) as sumPrice ' \
            'from ticket ' \
            'where customer_email  = %s ' \
            'group by month(purchase_date), year(purchase_date)'
    cursor.execute(query, (username))
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('customerSpending.html', username=username, posts3=data1)

@app.route('/spendingChartInRange', methods=['GET', 'POST'])
def spendingChartInRange():

    username = session['username']
    #cursor used to send queries
    cursor = conn.cursor()
    beginDate = request.form['beginDate']
    endDate = request.form['endDate']
    #executes query
    query = ' select month(purchase_date) as m, year(purchase_date) as y, sum(sold_price) as sumPrice ' \
            'from ticket ' \
            'where customer_email  = %s and purchase_date >= %s and purchase_date <= %s' \
            'group by month(purchase_date), year(purchase_date)'
    cursor.execute(query, (username,beginDate,endDate))
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('customerSpending.html', username=username, posts4=data1)


@app.route('/viewFutureFlights', methods=['GET', 'POST'])
def viewFutureFlights():
    username = session['username']
    # cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')

    # executes query
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    query2 = 'SELECT flight_num, d_date, d_time from flight WHERE airline_name = %s and d_date > current_date() and d_date < current_date () + interval 1 month ; '
    cursor.execute(query2, (airline_name))
    # stores the results in a variable
    data = cursor.fetchall()
    for each in data:
        print(each)
    error = None
    cursor.close()
    return render_template('viewFlights.html', username=username, chart1=data, error = error)

@app.route('/flightsBasedOnDate', methods=['GET', 'POST'])
def flightsBasedOnDate():
    username = session['username']
    start_date = request.form['StartDate']
    end_date = request.form['EndDate']
    # cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    # executes query
    query2 = 'SELECT flight_num, d_date, d_time FROM flight WHERE airline_name = %s and d_date > %s and d_date < %s'
    cursor.execute(query2, (airline_name, start_date, end_date))
    # stores the results in a variable
    data1 = cursor.fetchall()
    # use fetchall() if you are expecting more than 1 data row
    if (data1):
        for each in data1:
            print(each)
        error = None
        cursor.close()
        return render_template('viewFlights.html', username=username, error=error, chart2=data1)
    else:
        return render_template('viewFLights.html', username=username, error='No flights in this period!')

@app.route('/flightsBasedOnLocation', methods=['GET', 'POST'])
def flightsBasedOnLocation():
    username = session['username']

    departure_airport = request.form['departure_airport']
    arrival_airport = request.form['arrival_airport']
    # cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    # executes query
    query2 = 'SELECT flight_num, d_date, d_time FROM flight WHERE ' \
             'airline_name = %s and '\
             'dep_airport_code = (select distinct code from airport where name = %s) ' \
             'and arr_airport_code = (select code from airport where name = %s);'
    cursor.execute(query2, (airline_name, departure_airport, arrival_airport))
    # stores the results in a variable
    data1 = cursor.fetchall()
    # use fetchall() if you are expecting more than 1 data row
    if (data1):
        for each in data1:
            print(each)
        error = None
        cursor.close()
        return render_template('viewFlights.html', username=username, error=error, chart3=data1)
    else:
        return render_template('viewFLights.html', username=username, error='No flights found!')

@app.route('/customersOfFlight', methods=['GET', 'POST'])
def customersOfFlight():
    username = session['username']
    flight_num = request.form['flight_num']
    d_date = request.form['d_date']
    d_time = request.form['d_time']
    # cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    # executes query
    query2 = 'SELECT DISTINCT name, email FROM customer, ticket WHERE airline_name = %s and flight_num = %s and d_date = %s and d_time = %s and email = customer_email'
    cursor.execute(query2, (airline_name, flight_num, d_date, d_time))
    # stores the results in a variable
    data1 = cursor.fetchall()
    # use fetchall() if you are expecting more than 1 data row
    if (data1):
        for each in data1:
            print(each)
        error = None
        cursor.close()
        return render_template('viewFlights.html', username=username, error=error, chart4=data1)
    else:
        return render_template('viewFLights.html', username=username, error='This flight does not exist')
@app.route('/createFlightInfo', methods=['GET', 'POST'])
def createFlightInfo():
    username = session['username']
    airline_name = request.form['airline_name']
    d_date = request.form['departure_date']
    d_time = request.form['departure_time']
    flight_num = request.form['flight_number']
    a_date = request.form['arrival_date']
    a_time = request.form['arrival_time']
    base_price = request.form['base_ticket_price']
    status = request.form['status']
    airplane_i_num = request.form['airplane_identification_number']
    arr_code = request.form['arrival_airport_code']
    dep_code = request.form['departure_airport_code']

    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query = 'SELECT * FROM flight Where airline_name = %s and d_date = %s and d_time = %s and flight_num = %s and status = %s'
    cursor.execute(query,(airline_name, d_date, d_time, flight_num, status))
    data = cursor.fetchone()
    error = None

    if(data):
        error = "This flight already exists"
        return render_template('createFlight.html', error = error)
    else:
        ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %d, %s, %s, %s, %s)'
        cursor.execute(ins, (airline_name, d_date, d_time, flight_num, a_date, a_time, int(base_price), status, airplane_i_num, arr_code, dep_code))
        conn.commit()
        cursor.close()
        return render_template('staffHome.html')

@app.route('/changeFlightStatusInfo', methods=['GET', 'POST'])
def changeFlightStatusInfo():
    flight_num = request.form['flight_number']
    new_status = request.form['new_status']
    username = session['username']
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query = 'SELECT * FROM flight WHERE flight_num = %s'
    cursor.execute(query, (flight_num))
    data = cursor.fetchone()
    error = None

    if(data):
        ins = 'UPDATE flight SET status = %s WHERE flight_num = %s'
        cursor.execute(ins,(new_status, flight_num))
        conn.commit()
        cursor.close()
        return render_template('staffHome.html')
    else:
        error = "This flight does not exist"
        return render_template('changeFlightStatus.html', error = error)



@app.route('/addAirplaneInfo', methods=['GET', 'POST'])
def addAirplaneInfo():
    username = session['username']
    iden_num = request.form['Identification_number']
    number_seat = request.form['number_of_seats']

    cursor = conn.cursor()
    query = 'SELECT airline_name FROM staff where username = %s'
    cursor.execute(query,(username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']

    query2 = 'SELECT * FROM airplane where iden_num = %s and airline_name = %s'
    cursor.execute(query2, (iden_num, airline_name))
    data2 = cursor.fetchone()

    if(data2):
        return render_template('addAirplane.html', error = 'airplane already exists')
    else:
        ins = 'INSERT into airplane VALUES(%s, %s, %s)'
        cursor.execute(ins,(iden_num, airline_name, number_seat))
        conn.commit()
        cursor.close()
        return render_template('addAirplaneSuccess.html')

@app.route('/addAirplaneSuccess', methods=['GET', 'POST'])
def addAirplaneSuccess():
    username = session['username']
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')

    query = 'SELECT airline_name FROM staff where username = %s'
    cursor.execute(query,(username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']

    query2 = 'SELECT * FROM airplane where airline_name = %s'
    cursor.execute(query2, (airline_name))

    data2 = cursor.fetchall()
    for each in data2:
        print(each)
    cursor.close()
    return render_template('addAirplaneSuccess.html', username=username, postsa=data2)


@app.route('/popularThreeMonth', methods=['GET', 'POST'])
def popularThreeMonth():

    username = session['username']

    #cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    #executes query
    query = 'select dep_airport_code, (select city from airport where code = dep_airport_code) as city ' \
            'from ticket natural join flight ' \
            'where d_date > current_date() - interval 3 month and airline_name = %s' \
            'group by dep_airport_code ' \
            'order by count(*) desc limit 3'
    cursor.execute(query,airline_name)
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('topDest.html', username=username, posts1=data1)

@app.route('/popularYear', methods=['GET', 'POST'])
def popularYear():

    username = session['username']

    #cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    #executes query
    query = 'select dep_airport_code, (select city from airport where code = dep_airport_code) as city ' \
            'from ticket natural join flight ' \
            'where d_date > current_date() - interval 1 year and airline_name = %s' \
            'group by dep_airport_code ' \
            'order by count(*) desc limit 3'
    cursor.execute(query, airline_name)
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('topDest.html', username=username, posts2=data1)

@app.route('/revenueMonth', methods=['GET', 'POST'])
def revenueMonth():

    username = session['username']

    #cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    #executes query
    query = 'select sum(sold_price) as revenue from ticket ' \
            'where purchase_date > current_date() - interval 1 month' \
            ' and airline_name = %s'
    cursor.execute(query,airline_name)
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('staffViewRevenue.html', username=username, posts1=data1)

@app.route('/revenueYear', methods=['GET', 'POST'])
def revenueYear():

    username = session['username']

    #cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    #executes query
    query = 'select sum(sold_price) as revenue from ticket where purchase_date > current_date() - interval 1 year' \
            ' and airline_name = %s'
    cursor.execute(query,airline_name)
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('staffViewRevenue.html', username=username, posts2=data1)

@app.route('/staffViewRatings', methods=['GET', 'POST'])
def staffViewRatings():
    username = session['username']
    flight_num = request.form['flight_num']
    d_date = request.form['d_date']
    d_time = request.form['d_time']
    #cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    print(airline_name)
    #executes query
    query2 = 'SELECT avg(star) as num FROM rate WHERE airline_name = %s and flight_num = %s and d_date = %s and d_time = %s'
    cursor.execute(query2, (airline_name, flight_num, d_date, d_time))
    #stores the results in a variable
    data1 = cursor.fetchall()
    #use fetchall() if you are expecting more than 1 data row
    query3 = 'SELECT star, comment FROM rate WHERE airline_name = %s and flight_num = %s and d_date = %s and d_time = %s '
    cursor.execute(query3, (airline_name, flight_num, d_date, d_time))
    data2 = cursor.fetchall()
    if (data1 and data2):
        for each in data1:
            print(each)
        for each in data2:
            print(each)
        error = None
        cursor.close()
        return render_template('viewFlightRatings.html', username = username, error= error, posts1 = data1, chart1 = data2)
    else:
        return render_template('viewFlightRatings.html', username = username, error = 'This flight does not exist' )


@app.route('/frequentCustomer', methods=['GET', 'POST'])
def frequentCustomer():
    username = session['username']
    # cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    # executes query
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    query2 = 'SELECT distinct name, email from customer, ticket WHERE airline_name = %s and email = customer_email and purchase_date > current_date () - interval 1 year GROUP BY customer_email ORDER BY COUNT(*) DESC LIMIT 1; '
    cursor.execute(query2,(airline_name))
    # stores the results in a variable
    data = cursor.fetchall()
    for each in data:
        print(each)
    cursor.close()
    return render_template('viewFrequentCustomer.html', username=username, chart1=data)

@app.route('/flightsCustomerTaken', methods=['GET', 'POST'])
def flightsCustomerTaken():
    username = session['username']
    user_email = request.form['email']
    #cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    #executes query
    query1 = 'SELECT airline_name FROM staff WHERE username = %s'
    cursor.execute(query1, (username))
    airline_name = cursor.fetchone()
    airline_name = airline_name['airline_name']
    query2 = 'SELECT flight_num, d_date, d_time FROM ticket WHERE airline_name = %s and customer_email = %s;'
    cursor.execute(query2, (airline_name, user_email))
    #stores the results in a variable
    data = cursor.fetchall()
    if (data):
        for each in data:
            print(each)
        cursor.close()
        error = None
        return render_template('viewFrequentCustomer.html', username=username, chart2 = data, error=error)
    else:
        return render_template('viewFrequentCustomer.html', username=username, error='This customer does not exist')




@app.route('/addAirportInfo', methods=['GET', 'POST'])
def addAirportInfo():
    username = session['username']
    code = request.form['airport_code']
    name = request.form['airport_name']
    city = request.form['airport_city']

    cursor= conn.cursor()
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')



    query = 'SELECT * FROM airport where code = %s'
    cursor.execute(query,(code))

    data = cursor.fetchone()

    if(data):
        return render_template('addAirport.html', error = 'Airport already exists')
    else:
        ins = 'INSERT into airport VALUES(%s, %s, %s)'
        cursor.execute(ins, (code, name, city))
        conn.commit()
        cursor.close()
        return render_template('staffHome.html')


@app.route('/ticketYearReport', methods=['GET', 'POST'])
def ticketYearReport():

    username = session['username']

    #cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')

#executes query
    query = ' select count(*) as num  from ticket ' \
            'where purchase_date > current_date() - interval 1 year and airline_name = ' \
            '(select airline_name from staff where username = %s)'
    cursor.execute(query,(username))
    #stores the results in a variable
    data1 = cursor.fetchall()
    query = ' select month(purchase_date) as m, year(purchase_date) as y, count(*) as num ' \
            'from ticket ' \
            'where purchase_date > current_date() - interval 1 year and airline_name = (select airline_name from staff where username = %s)' \
            'group by month(purchase_date), year(purchase_date)'
    cursor.execute(query,(username))
    #stores the results in a variable
    data2 = cursor.fetchall()

    for each in data1:
        print(each)
    for each in data2:
        print(each)
    cursor.close()
    return render_template('viewTicketReport.html', username=username, posts1=data1, chart1 = data2)

@app.route('/ticketMonthReport', methods=['GET', 'POST'])
def ticketMonthReport():

    username = session['username']

    #cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    #executes query
    query = ' select count(*) as num  from ticket ' \
            'where purchase_date > current_date() - interval 1 month and airline_name = ' \
            '(select airline_name from staff where username = %s)'
    cursor.execute(query,(username))
    #stores the results in a variable
    data1 = cursor.fetchall()
    query = ' select month(purchase_date) as m, year(purchase_date) as y, count(*) as num ' \
            'from ticket ' \
            'where purchase_date > current_date() - interval 1 month and airline_name = (select airline_name from staff where username = %s)' \
            'group by month(purchase_date), year(purchase_date)'
    cursor.execute(query,(username))
    #stores the results in a variable
    data2 = cursor.fetchall()
    for each in data1:
        print(each)
    for each in data2:
        print(each)
    cursor.close()
    return render_template('viewTicketReport.html', username=username, posts2=data1, chart2 = data2)

@app.route('/ticketRangeReport', methods=['GET', 'POST'])
def ticketRangeReport():

    username = session['username']
    begin_date = request.form['beginDate']
    end_date = request.form['endDate']
    #cursor used to send queries
    cursor = conn.cursor()
    #sanity check whether the user is a staff
    query0 = 'select * from staff where username = %s'
    cursor.execute(query0, (username))
    sanityData = cursor.fetchall()
    if(not sanityData):
        return render_template('customerConstraint.html')
    #executes query
    query = ' select count(*) as num from ticket ' \
            'where purchase_date >= %s and  purchase_date <= %s and airline_name = ' \
            '(select airline_name from staff where username = %s)'
    cursor.execute(query,(begin_date, end_date, username))
    #stores the results in a variable
    data1 = cursor.fetchall()
    query = ' select month(purchase_date) as m, year(purchase_date) as y, count(*) as num ' \
            'from ticket ' \
            'where purchase_date >= %s and  purchase_date <= %s and airline_name = (select airline_name from staff where username = %s)' \
            'group by month(purchase_date), year(purchase_date)'
    cursor.execute(query,(begin_date, end_date, username))
    #stores the results in a variable
    data2 = cursor.fetchall()
    for each in data1:
        print(each)
    for each in data2:
        print(each)
    cursor.close()
    return render_template('viewTicketReport.html', username=username, posts3=data1, chart3 = data2)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/goodbye')

@app.route('/goodbye')
def goodbye():
    return render_template('logout.html')



app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)