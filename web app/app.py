from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import calc_ingredients as ci
import calc_products as cp
from torch.xpu import current_device

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

app.secret_key = "key"

# uri = os.getenv("DATABASE_URL")

# # REMOVE channel_binding (important for psycopg2)
# uri = uri.replace("&channel_binding=require", "")

# app.config["SQLALCHEMY_DATABASE_URI"] = uri

# app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
#     "pool_pre_ping": True,
#     "pool_recycle": 300,
# }

db = SQLAlchemy(app)

# @app.route("/test-db")
# def test_db():
#     print(os.getenv("DATABASE_URL"))
#     db.session.execute(text("SELECT 1"))
#     return "DB works"

# <><><><><><><><><><><><><> HOME PAGE <><><><><><><><><><><><><><><><>

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
    if request.method == "POST":                                # user submits name
        session["user"] = request.form.get("user", "").strip()  # get name from form and store in session
        session.permanent = True                                # make session permanent (lasts for 10 minutes)
        session["completed_steps"] = session.get("completed_steps", [])
        if "name" not in session["completed_steps"]:
            session["completed_steps"].append("name")
        return redirect(url_for('age'))                      # redirect to weight question page
    
    session["visited_steps"] = session.get("visited_steps", [])
    session["visited_steps"].append("name")
    return render_template("qName.html", 
                           usr=session.get("user"),
                           current_step="name"
                           )  
   

#TODO: create qAge.html
@app.route("/quiz/age", methods=["GET", "POST"])
def age():
    """ asks user for age and stores in session. redirects to sex question page.
    """
    if request.method == "POST":
        session["age"] = request.form.get("age", "")
        if "age" not in session["completed_steps"]:
            session["completed_steps"].append("age")
        return redirect(url_for('sex'))
    if "age" not in session["visited_steps"]:
        session["visited_steps"].append("age")
    return render_template("qAge.html",
                           usr=session.get("user"),
                           current_step="age"
                           )

# TODO: create qSex.html
@app.route("/quiz/sex", methods=["GET", "POST"])
def sex():
    """asks user for sex and stores it in session. redirects to weight page.

    """
    if request.method == "POST":
        session["sex"] = request.form.get("sex", "")
        if "sex" not in session["completed_steps"]:
            session["completed_steps"].append("sex")
        return redirect(url_for('weight'))
    if "sex" not in session["visited_steps"]:
        session["visited_steps"].append("sex")
    return render_template("qSex.html",
                           usr=session.get("user"),
                           current_step="sex"
                           )


@app.route("/quiz/weight", methods=["GET", "POST"])
def weight():
    """ asks user for weight and stores in session. redirects to goals page.
    """
    if request.method == "POST":
        session["weight"] = request.form.get("weight", "")
        if "weight" not in session["completed_steps"]:
            session["completed_steps"].append("weight")
        return redirect(url_for('goals'))
    if "weight" not in session["visited_steps"]:
        session["visited_steps"].append("weight")
    return render_template("qWeight.html", 
                           usr=session.get("user"),
                           current_step="weight"
                           )
  
  
@app.route("/quiz/goals", methods=["GET", "POST"])
def goals():
    """ asks user their workout goals & stores it in session
    """
    if request.method == "POST":
        selected_goals = request.form.getlist("goal")
        session["pumpGoal"]      = "pump"      in selected_goals
        session["energyGoal"]    = "energy"    in selected_goals
        session["focusGoal"]     = "focus"     in selected_goals
        session["enduranceGoal"] = "endurance" in selected_goals
        session["strengthGoal"]  = "strength"  in selected_goals
        if "goals" not in session["completed_steps"]:
            session["completed_steps"].append("goals")
        return redirect(url_for('stimulant'))
    if "goals" not in session["visited_steps"]:
        session["visited_steps"].append("goals")
    return render_template("qGoals.html",
                           usr=session.get("user"),
                           current_step="goals"
                           )


@app.route("/quiz/stimulant", methods=["GET", "POST"])
def stimulant():
    if request.method == "POST":
        session["stimulant"] = request.form.get("stimulant", "")
        if "stimulant" not in session["completed_steps"]:
            session["completed_steps"].append("stimulant")
        return redirect(url_for('results'))
    if "stimulant" not in session["visited_steps"]:
        session["visited_steps"].append("stimulant")
    return render_template("qStimulant.html",
                           usr=session.get("user"),
                           current_step="stimulant"
                           )


# <><><><><><><><><><><><> CUSTOMIZATION PAGES <><><><><><><><><><><><><>
@app.route("/quiz/results", methods=["GET", "POST"])
def results():
    """ displays quiz results. for debugging purposes.
    """
    ci.set_user_info(session.get("age", ""),
                     session.get("weight", -1),
                     session.get("sex", ""), 
                     [session.get("pumpGoal", False),
                      session.get("energyGoal", False),
                      session.get("focusGoal", False),
                      session.get("enduranceGoal", False),
                      session.get("strengthGoal", False)],
                     session.get("stimulant", -1))
    caffeine = ci.calculate_caffeine()
    return render_template("qResults.html",
                            usr=session.get("user"),
                            weight=session.get("weight"),
                            stimulant=session.get("stimulant"),
                            pumpGoal=session.get("pumpGoal"),
                            energyGoal=session.get("energyGoal"),
                            focusGoal=session.get("focusGoal"),
                            enduranceGoal=session.get("enduranceGoal"),
                            strengthGoal=session.get("strengthGoal"),
                            caffeine=caffeine
                            )
                    

@app.route("/quiz/customize", methods=["GET", "POST"])
def customize():
    """displays customization page w/ sliders

    """
    if request.method == "POST":
        session["custom_caffeine"]    = request.form.get("custom_caffeine",   -1)
        session["custom_beta"]        = request.form.get("custom_beta",       -1)
        session["custom_creatine"]    = request.form.get("custom_creatine",   -1)
        session["custom_theanine"]    = request.form.get("custom_theanine",   -1)
        session["custom_betaine"]     = request.form.get("custom_betaine",    -1)
        session["custom_taurine"]     = request.form.get("custom_taurine",    -1)
        session["custom_citrulline"]  = request.form.get("custom_citrulline", -1)
        session["custom_tyrosine"]    = request.form.get("custom_tyrosine",   -1)
        session["custom_agmatine"]     = request.form.get("custom_agmatine",  -1)
        return redirect(url_for('products'))
    return render_template("qCustomize.html",
                            usr=session.get("user"),
                            current_step="customize",
                            caffeine=100,
                            beta=1.6,
                            creatine=5,
                            recommended=['caffeine', 'beta', 'creatine']
                            )

# <><><><><><><><><><><><> PRODUCTS PAGE <><><><><><><><><><><><><><><>
    
@app.route("/products")
def products(): 
    """
    NEW AND IMPROVED PRODUCTS FUNCTION
    """
    # establish connection w/ database
    query = text("SELECT * FROM preworkout")
    result = db.session.execute(query)

    products = [dict(row._mapping) for row in result]
    ingredients = {"caffeine"    : session.get("custom_caffeine", 0),
                   "beta_alanine": session.get("custom_betaAlanine", 0),
                   "creatine"    : session.get("custom_creatine", 0)} 
    
    perfect, close, similar = cp.categorize_products(products, ingredients)
    length = cp.get_length(ingredients)
    return render_template("products.html",
                           perfect=perfect,
                           close=close,
                           similar=similar,
                           length=length ,
                           caff=session.get("custom_caffeine", 0),
                           beta=session.get("custom_betaAlanine", 0),
                           cre=session.get("custom_creatine", 0)
    )


        


if __name__ == "__main__":
    app.run(debug=True)