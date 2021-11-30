
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
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

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for customer register
@app.route('/customerRegister')
def customerRegister():
    return render_template('customerRegister.html')
#Define route for staff register
@app.route('/staffRegister')
def staffRegister():
    return render_template('staffRegister.html')

#Define route for customer login
@app.route('/customerLogin')
def customerLogin():
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

@app.route('/ticketPurchase')
def ticketPurchase():
    return render_template('customerPurchase.html')

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
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, null,null,null, null,null,null, null,null,null)'
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
    query = 'SELECT * FROM customer WHERE email = %s and password = %s'
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
    return render_template('flightSearch.html', username=username, posts=data1)

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
    query = 'SELECT * FROM flight WHERE d_date = %s ' \
            'and dep_airport_code = (select code from airport where airport.name = %s) ' \
            'and arr_airport_code = (select code from airport where airport.name = %s)'\
            'and exists (select * from flight where d_date = %s and ' \
            'dep_airport_code = (select code from airport where airport.name = %s) ' \
            'and arr_airport_code = (select code from airport where airport.name = %s))'

    cursor.execute(query, (dep_date,dep_airport,arr_airport,return_date,arr_airport,dep_airport))
    #stores the results in a variable
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('roundFlightSearch.html', username=username, posts=data1)

@app.route('/statusSearchProcess', methods=['GET', 'POST'])
def statusSearchProcess():

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
    return render_template('pastFlightStatus.html', username=username, posts=data1)





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