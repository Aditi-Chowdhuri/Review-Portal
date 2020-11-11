from flask import Flask, render_template, redirect, session, request
import random
import sqlite3

app = Flask(__name__)
app.secret_key=str(random.random())

@app.route('/', methods=['GET', 'POST'])
def defaul():
    # Any python statements
    fruits = ["strawberry", "mango", "blueberry"]
    age=20
    pattern = ["*"*i for i in range(1,21)]
    return render_template("index.html", fruits=fruits, age=age, pattern=pattern)

@app.route('/signup', methods=['GET', 'POST'])
def signu():
    try:
        _=session["username"]
        return redirect("/login")
    except:
        if request.method=="POST":
            pw_hash = bcrypt.generate_password_hash(request.form["password"])
            conn = sqlite3.connect("database.db")
            conn.execute("INSERT INTO user VALUES(\"%s\", \"%s\", \"%s\")"% (request.form["username"], request.form["email"], request.form["password"]))
            conn.commit()
            session["username"] = request.form["username"]
            return redirect("/landing")
        return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def logi():
    try:
        _=session["username"]
        return redirect("/landing")
    except:
        if request.method=="POST":
            name = request.form["username"]
            pas = request.form["password"]
            conn = sqlite3.connect("database.db")
            login = conn.execute("SELECT * FROM user WHERE username = \"%s\" AND password = \"%s\""% (name, pas))
            counter = 0
            for i in login:
                counter+=1
            if counter>0:
                session["username"] = name
                return redirect("/landing")
            else:
                return redirect("/login")
        return render_template("login.html")

@app.route('/landing')
def landin():
    try:
        _=session["username"]
        return render_template("landing.html", username=session["username"])
    except:
        return redirect("/login")

@app.route('/form', methods=['GET', 'POST'])
def forms():
    try:
        _=session["username"]
        if request.method=="POST":
            conn = sqlite3.connect("database.db")
            conn.execute("INSERT INTO review VALUES(\"%s\", \"%s\")"% (request.form["field1"], request.form["review"]))
            conn.commit()
            return redirect("/review")
        return render_template("form.html")
    except KeyError:
        return redirect("/login")

@app.route('/review')
def revie():
    try:
        _=session["username"]
        conn = sqlite3.connect("database.db")
        rev = []
        name = conn.execute("SELECT * FROM review")
        for row in name:
            rev.append(row)
        return render_template("review.html", rev=rev)
    except:
        return redirect("/login")

@app.route('/logout')
def logou():
    session.clear()
    return redirect("/login")

@app.route('/home')
def hom():
    session["username"]="aditi"
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)