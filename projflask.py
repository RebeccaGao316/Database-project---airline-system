
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

@app.route('/customerHome')
def customerHome():
    return render_template('customerHome.html')

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
    query = 'SELECT * FROM staff WHERE username = %s'
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
        ins = 'INSERT INTO staff VALUES(%s, %s,null,null,null,%s)'
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
    query = 'SELECT * FROM staff WHERE username = %s and password = %s'
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


    #cursor used to send queries
    cursor = conn.cursor()

    #query = 'INSERT INTO ticket (card_type,card_num,expire_date,purchase_date,' \
    #        'purchase_time,airline_name,d_date, d_time,flight_num,customer_email,sold_price,tID)'\
    #       'VALUES (%s,%s,%s,date.today(),datetime.now(),%s,%s,%s,%s,%s,100,20)'
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

@app.route('/createFlight')
def createFlight():
    return render_template('createFlight.html')

@app.route('/changeFlightStatus')
def changeFlightStatus():
    return render_template('changeFlightStatus.html')

@app.route('/createFlightInfo', methods=['GET', 'POST'])
def createFlightInfo():
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

    cursor = conn.cursor()
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