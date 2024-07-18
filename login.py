from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.secret_ley = 'vanilla'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class user(db.Model):
    username = db.Column(db.String(99), primary_key=True)
    password = db.Column(db.String(99))
    fName = db.Column(db.String(99))
    lName = db.Column(db.String(99))

@app.route('/', methods=["GET", "POST"])
def index():
    db.create_all()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        login = user.query.filter_by(username = username, password = password).first()

        print(login)

        if login is not None:
            return redirect(url_for('secretpage'))
        
    return render_template ('index.html')

@app.route('/signup', methods=['post', 'get'])
def signup():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('firstName')
        lastname = request.form.get('lastName')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        passOne = False
        passTwo = False
        passThree = False

        eightCharacters = False

        for cap in password:
            if cap.isupper():
                print ("pass1")
                passOne = True
                break

        for lower in password:
            if lower.islower():
                print ("pass2")
                passTwo = True
                break
        
        if passOne != True:
            message += " Contain a uppercase! "

        if passTwo != True:
            message += " Contain a lowercase! "

        if password[-1].isnumeric():
            print ("pass3")
            passThree = True
        else:
            message += " End with a number! "

        if len(password) < 8:
            message += " Have eight characters! "
        else:
            eightCharacters = True

        if password != cpassword:
            print("No match!")
            message = "Passwords do not match!"

        if passOne == True:
            if passTwo == True:
                if passThree == True:
                    if eightCharacters == True:
                        if password == cpassword:
                            registration = user(fName = firstname, lName = lastname, username = username, password = password)
                            db.session.add(registration)
                            db.session.commit()

                            return redirect(url_for('thankyou'))

    return render_template('signup.html', message = message)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/secretpage')
def secretpage():
    return render_template('secretpage.html')

if __name__ == '__main__':
    app.run(debug=True)