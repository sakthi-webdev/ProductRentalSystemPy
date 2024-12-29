from flask import Flask, render_template, request, session, flash

import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


@app.route('/')
def home():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb ")
    data = cur.fetchall()
    return render_template('index.html', data=data)


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("you are successfully Login")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route('/NewProduct')
def NewProduct():
    return render_template('NewProduct.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/newproduct", methods=['GET', 'POST'])
def newproduct():
    if request.method == 'POST':
        pname = request.form['pname']

        ptype = request.form['ptype']

        price = request.form['price']
        offer = request.form['offer']
        info = request.form['info']
        qty = request.form['qty']
        Deposit = request.form['Deposit']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)

        print(price)
        print(offer)

        offeramount = float(price) * (float(offer) / 100)
        print(offeramount)

        total = float(price) - float(offeramount)

        print(total)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into protb values('','" + pname + "','" + ptype + "','" + str(
                price) + "','" + str(offer) + "','" + str(total) + "','" + info + "','" + savename + "','" + str(
                qty) + "','" + Deposit + "')")
        conn.commit()
        conn.close()

        flash('Product  Info Save Successfully!')
        return render_template('NewProduct.html')


@app.route("/ProductInfo")
def ProductInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  ")
    data = cur.fetchall()
    return render_template('ProductInfo.html', data=data)


@app.route("/Approved")
def Approved():
    id = request.args.get('id')
    uname = request.args.get('uname')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cursor = conn.cursor()
    cursor.execute(
        "update   carttb set status='Approved' where id='" + str(id) + "'")
    conn.commit()
    conn.close()

    flash('Product  Approved  Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from regtb where username='" + uname + "'")
    data = cursor.fetchone()
    if data:
        mob = data[2]

    sendmsg(mob, 'Rent Approved')
    return SalesInfo()


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


@app.route("/SalesInfo")
def SalesInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where   Status='waiting' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where   Status='Approved' or  Status='Paid' ")
    data3 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb ")
    data2 = cur.fetchall()

    return render_template('SalesInfo.html', data1=data1, data2=data2, data3=data3)


@app.route("/Remove")
def Remove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from protb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product  info Remove Successfully!')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  ")
    data = cur.fetchall()
    return render_template('ProductInfo.html', data=data)


@app.route("/hsearch")
def hsearch():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb where ptype='" + id + "'  ")
    data = cur.fetchall()
    return render_template('index.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']

        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")
    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash('Username or Password is wrong')
            return render_template('UserLogin.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and password='" + password + "'")
            data = cur.fetchall()
            flash("you are successfully logged in")
            return render_template('UserHome.html', data=data)


@app.route('/UserHome')
def UserHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT username FROM regtb  where username='" + session['uname'] + "' ")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route('/Search')
def Search():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  ")
    data = cur.fetchall()
    return render_template('Search.html', data=data)


@app.route("/csearch", methods=['GET', 'POST'])
def csearch():
    if request.method == 'POST':
        ptype = request.form['ptype']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM protb where  ProductType='" + ptype + "' ")
        data = cur.fetchall()

        return render_template('Search.html', data=data)


@app.route("/add")
def add():
    flash("Please Login")
    return render_template('index.html')


@app.route("/Add")
def Add():
    id = request.args.get('id')
    session['pid'] = id

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM protb where  id='" + id + "'")
    data = cursor.fetchone()

    if data:
        name = data[1]
        desc = data[6]
        amount = data[5]
        image = data[7]




    else:
        return 'Incorrect username / password !'

    return render_template('FullInfo.html', name=name, desc=desc, amount=amount, image=image)


@app.route("/addcart", methods=['GET', 'POST'])
def addcart():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        pid = session['pid']
        uname = session['uname']
        qty = request.form['qty']
        # pmode = request.form['pmode']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb  where  id='" + str(pid) + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[1]
            Producttype = data[2]
            price = data[5]
            cQty = data[8]

            Image = data[7]

            deposit = data[9]

        else:
            return 'No Record Found!'

        tprice = float(price) * float(qty)

        clqty = float(cQty) - float(qty)

        if clqty < 0:

            flash('Low  Product ')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM protb  where id='" + pid + "' ")
            data = cur.fetchall()
            return render_template('AddCart.html', data=data)

        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT  count(*) As count  FROM booktb ")
            data = cursor.fetchone()
            if data:
                bookno = data[0]
                print(bookno)

                if bookno == 'Null' or bookno == 0:
                    bookno = 1
                else:
                    bookno += 1

            else:
                return 'Incorrect username / password !'

            bookno = 'BOOKID' + str(bookno)

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO carttb VALUES ('','" + uname + "','" + ProductName + "','" + Producttype + "','" + str(
                    price) + "','" + str(qty) + "','" + str(tprice) + "','" +
                Image + "','" + date + "','waiting','" + bookno + "','" + deposit + "')")
            conn.commit()
            conn.close()

            flash('Book   Successfully waiting For Admin Approval')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM protb  ")
            data = cur.fetchall()
            return render_template('Search.html', data=data)


@app.route("/Cart")
def Cart():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='Approved' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice ,sum(Deposit) as Deposit  FROM  carttb where UserName='" + uname + "' and Status='Approved' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]
        Deposit = data1[2]
    else:
        return 'No Record Found!'

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice, Deposit=Deposit)


@app.route("/RemoveCart")
def RemoveCart():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from carttb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product Remove Successfully!')

    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='Approved' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='Approved' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)


@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        uname = session['uname']
        cname = request.form['cname']
        Cardno = request.form['cno']
        Cvno = request.form['cvno']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='Approved' ")
        data1 = cursor.fetchone()
        if data1:
            tqty = data1[0]
            tprice = data1[1]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) As count  FROM booktb ")
        data = cursor.fetchone()
        if data:
            bookno = data[0]
            print(bookno)

            if bookno == 'Null' or bookno == 0:
                bookno = 1
            else:
                bookno += 1

        else:
            return 'Incorrect username / password !'

        bookno = 'BOOKID' + str(bookno)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cursor = conn.cursor()
        cursor.execute(
            "update   carttb set status='paid',Bookid='" + bookno + "' where UserName='" + uname + "' and Status='Approved' ")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO booktb VALUES ('','" + uname + "','" + bookno + "','" + str(tqty) + "','" + str(
                tprice) + "','" + cname + "','" + Cardno + "','" + Cvno + "','" + date + "')")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='paid' ")
        data1 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
        data2 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + uname + "'")
        data33 = cursor.fetchone()
        if data33:
            mob = data33[2]

        sendmsg(mob, 'Product On the Way')

    return render_template('UserBook.html', data1=data1, data2=data2)


@app.route("/BookInfo")
def BookInfo():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='paid' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
    data2 = cur.fetchall()
    return render_template('UserBook.html', data1=data1, data2=data2)


@app.route("/Return11")
def Return11():
    id = request.args.get('id')
    uname = request.args.get('uname')
    dd = request.args.get('dd')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1productrentaldb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from regtb where username='" + uname + "'")
    data = cursor.fetchone()
    if data:
        mob = data[2]

    sendmsg(mob, 'Your Deposit Amount  Refund! Amount'+str(dd))
    return  BookInfo()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
