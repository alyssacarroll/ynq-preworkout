from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "key"

DB_NAME = "dlsd_preworkout_products"
DB_PASSWORD = "password"


# <><><><><><><><><><><><><> MAIN PAGE <><><><><><><><><><><><><><><><>
@app.route("/")
def home():
    return render_template("home.html")

# <><><><><><><><><><><><><> QUIZ PAGES <><><><><><><><><><><><><><><>

@app.route("/quiz/name", methods=["GET", "POST"])
def name():
    """ asks user for name and stores in session. redirects to weight question page.

    Returns:
        _type_: render_template or redirect
        renders name question page or redirects to weight question page
    """
    if request.method == "POST": # user submits name
        session["user"] = request.form.get("user", "").strip()  # get name from form and store in session
        return redirect(url_for('weight'))  # redirect to weight question page
    return render_template("qName.html", 
                           usr=session.get("user"))  
   

#TODO
def age():
    return -1
    
    
# TODO
def sex():
    return -1


@app.route("/quiz/weight", methods=["GET", "POST"])
def weight():
    """ asks user for weight and stores in session. redirects to results page.
    """
    if request.method == "POST":
        session["weight"] = request.form.get("weight", "").strip()
        return redirect(url_for('stimulant'))
    return render_template("qWeight.html", 
                           usr=session.get("user"))
  
  
@app.route("/quiz/goals", methods=["GET", "POST"])
def goals():
    """ asks user their workout goals & stores it in session
    """
    if request.method == "POST":
        # TODO: store goals in session
        session["pumpGoal"] = False
        session["energyGoal"] = False
        session["enduranceGoal"] = False
    # TODO: create qGoals.html
    return -1

# TODO: change to stimulant level
@app.route("/quiz/stimulant", methods=["GET", "POST"])
def stimulant():
    if request.method == "POST":
        session["stimulant"] = request.form.get("stimulant", "")
        return redirect(url_for('results'))
    return render_template("qStimulant.html",
                           usr=session.get("user"))


# <><><><><><><><><><><><> CUSTOMIZATION PAGES <><><><><><><><><><><><><>
@app.route("/quiz/results", methods=["GET", "POST"])
def results():
    """ displays quiz results. placeholder for future slider adjustment page.
    """
    return render_template("qResults.html",
                            usr=session.get("user"),
                            weight=session.get("weight"),
                            stimulant=session.get("stimulant"))


@app.route("/quiz/customize", methods=["GET", "POST"])
def customize():
    """displays slider page

    """
    if request.method == "POST":
        session["custom_caffeine"] = request.form.get("custom_caffeine", "").strip()
        return redirect(url_for('products'))
    return render_template("qCustomize.html",
                            usr=session.get("user"),
                            weight=session.get("weight"),
                            stimulant=session.get("stimulant"))

# <><><><><><><><><><><><> PRODUCTS PAGE <><><><><><><><><><><><><><><>
@app.route("/products")
def products(): 
    # establish connection w/ database
    conn = mysql.connector.connect(
       host="localhost",
       user="root",
       password=DB_PASSWORD,
       database=DB_NAME
    )
    cur = conn.cursor(dictionary=True)  # cursor that collects data

    cur.execute("SELECT * FROM preworkout_powders")
    products = cur.fetchall()

    # close database connection
    cur.close()
    conn.close()

    return render_template("products.html",
                            products=products,
                            caffeine=session.get("custom_caffeine")
    )

if __name__ == "__main__":
    app.run(debug=True)