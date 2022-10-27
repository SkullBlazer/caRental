from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Iwonttellany1!"
app.config['MYSQL_DB'] = "test"
db = MySQL(app)
login = False

@app.route('/login', methods=['GET', 'POST'])
def index():
    global login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM customer;")
        bid = cur.rowcount + 1
        try:
            phone = request.form['phone']
            email = request.form['email']
            cur.execute('INSERT INTO customer (custid, custname, custemail, custpass, custphone) VALUES\
            (%s, %s, %s, %s, %s);', (bid, username, email, password, phone))
        except KeyError:
            cur.execute('SELECT * FROM customer WHERE custname = %s AND custpass = %s;', (username, password))
            cur.fetchall()
            if cur.rowcount == 0:
                cur.close()
                return render_template('invalid.html')
            else:
                login = True
                cur.close()
                return redirect(url_for('logged_in'))
        db.connection.commit()
        cur.close()
        return "Success!"
    return render_template('index.html')

@app.route('/users')
def users():
    cur = db.connection.cursor()
    users = cur.execute("SELECT * FROM customer;")

    if users > 0:
        userDetails = cur.fetchall()
        cur.close()
        return render_template('users.html', userDetails=userDetails)
    cur.close()

@app.route('/u')
def logged_in():
    if login:
        return render_template('site2.html')
    else:
        return redirect(url_for('index'))

@app.route('/home')
def home():
    global login
    if login:
        return render_template('site2.html')
    else:
        return render_template('site.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE aname = %s AND apass = %s;', (username, password))
        cur.fetchall()
        if cur.rowcount == 0:
            cur.close()
            return render_template('admininvalid.html')
        else:
            cur.close()
            return redirect(url_for('logged_in'))
    return render_template('admin.html')

@app.route('/')
def redir():
    return redirect(url_for('home'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == "POST":
        name = request.form['name']
        start = request.form['start']
        stop = request.form['stop']
        return redirect(url_for('model'))
    return render_template('book.html')

@app.route('/model')
def model():
    return render_template('model.html')

@app.route('/confirmation')
def confirm():
    return render_template('confirmation.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/product/1')
def product1():
    return render_template('products/product1.html')

@app.route('/product/2')
def product2():
    return render_template('products/product2.html')

@app.route('/product/3')
def product3():
    return render_template('products/product3.html')

@app.route('/product/4')
def product4():
    return render_template('products/product4.html')

@app.route('/product/5')
def product5():
    return render_template('products/product5.html')

@app.route('/product/6')
def product6():
    return render_template('products/product6.html')

@app.route('/sdetails/1')
def sdetails1():
    return render_template('details/details1.html')

@app.route('/sdetails/2')
def sdetails2():
    return render_template('details/details2.html')

@app.route('/sdetails/3')
def sdetails3():
    return render_template('details/details3.html')

if __name__ == "__main__":
    app.run(debug=True)