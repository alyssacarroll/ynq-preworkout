from unittest import case

from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
import mysql.connector

app = Flask(__name__)
app.secret_key = "key"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)

DB_NAME = "dlsd_preworkout_products"
TABLE_NAME = "preworkout"
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
    if request.method == "POST":                                # user submits name
        session["user"] = request.form.get("user", "").strip()  # get name from form and store in session
        session.permanent = True                                # make session permanent (lasts for 10 minutes)
        session["completed_steps"] = session.get("completed_steps", [])
        if "name" not in session["completed_steps"]:
            session["completed_steps"].append("name")
        return redirect(url_for('goals'))                      # redirect to weight question page
    return render_template("qName.html", 
                           usr=session.get("user"),
                           current_step="name"
                           )  
   

#TODO
def age():
    return -1
    
    
# TODO
def sex():
    return -1


# @app.route("/quiz/weight", methods=["GET", "POST"])
# def weight():
#     """ asks user for weight and stores in session. redirects to results page.
#     """
#     if request.method == "POST":
#         session["weight"] = request.form.get("weight", "").strip()
#         return redirect(url_for('goals'))
#     return render_template("qWeight.html", 
#                            usr=session.get("user"))
  
  
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
    return render_template("qGoals.html",
                           usr=session.get("user"),
                           current_step="goals"
                           )

# TODO: change to stimulant level
@app.route("/quiz/stimulant", methods=["GET", "POST"])
def stimulant():
    if request.method == "POST":
        session["stimulant"] = request.form.get("stimulant", "")
        if "stimulant" not in session["completed_steps"]:
            session["completed_steps"].append("stimulant")
        return redirect(url_for('customize'))
    return render_template("qStimulant.html",
                           usr=session.get("user"),
                           current_step="stimulant"
                           )


# <><><><><><><><><><><><> CUSTOMIZATION PAGES <><><><><><><><><><><><><>
@app.route("/quiz/results", methods=["GET", "POST"])
def results():
    """ displays quiz results. placeholder for future slider adjustment page.
    """
    caffeine_min, caffeine_max, beta_alanine_min, beta_alanine_max, creatine_min, creatine_max = calculate_ranges()
    return render_template("qResults.html",
                            usr=session.get("user"),
                            # weight=session.get("weight"),
                            stimulant=session.get("stimulant"),
                            pumpGoal=session.get("pumpGoal"),
                            energyGoal=session.get("energyGoal"),
                            focusGoal=session.get("focusGoal"),
                            enduranceGoal=session.get("enduranceGoal"),
                            strengthGoal=session.get("strengthGoal"),
                            caffeine_min=caffeine_min,
                            caffeine_max=caffeine_max,
                            beta_alanine_min=beta_alanine_min,
                            beta_alanine_max=beta_alanine_max,
                            creatine_min=creatine_min,
                            creatine_max=creatine_max
                            )
                    

@app.route("/quiz/customize", methods=["GET", "POST"])
def customize():
    """displays slider page

    """
    if request.method == "POST":
        session["custom_caffeine"] = request.form.get("custom_caffeine", "").strip()
        session["custom_betaAlanine"] = request.form.get("custom_betaAlanine", "").strip()
        session["custom_creatine"] = request.form.get("custom_creatine", "").strip()
        return redirect(url_for('products'))
    caffeine_min, caffeine_max, beta_alanine_min, beta_alanine_max, creatine_min, creatine_max = calculate_ranges()
    return render_template("qCustomize.html",
                            usr=session.get("user"),
                            weight=session.get("weight"),
                            stimulant=session.get("stimulant"),
                            current_step="customize",
                            caffeine_min=caffeine_min,
                            caffeine_max=caffeine_max,
                            beta_alanine_min=beta_alanine_min,
                            beta_alanine_max=beta_alanine_max,
                            creatine_min=creatine_min,
                            creatine_max=creatine_max
                            )

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

    cur.execute("SELECT * FROM " + TABLE_NAME)  
    products = cur.fetchall()

    # close database connection
    cur.close()
    conn.close()

    caffeine_min, caffeine_max, beta_alanine_min, beta_alanine_max, creatine_min, creatine_max = calculate_ranges()

    return render_template("products.html",
                            products=products,
                            caffeine=session.get("custom_caffeine"),
                            beta_alanine=session.get("custom_betaAlanine"),
                            creatine=session.get("custom_creatine"),
                            caffeine_min=caffeine_min,
                            caffeine_max=caffeine_max,
                            beta_alanine_min=beta_alanine_min,
                            beta_alanine_max=beta_alanine_max,
                            creatine_min=creatine_min,
                            creatine_max=creatine_max
    )


# <><><><><><><><><><><><> CALCULATIONS <><><><><><><><><><><><><><><>

def calculate_ingredient_weights():
    """ calculates ingredient amounts based on quiz responses and stores in session
    
    2-9 mg/kg caffeine, 0.03 g creatine, 0.3 g beta-alanine
    """
    
    stim = session.get("stimulant")
    pumpGoal      = session.get("pumpGoal")
    energyGoal    = session.get("energyGoal")
    focusGoal     = session.get("focusGoal")
    enduranceGoal = session.get("enduranceGoal")
    strengthGoal  = session.get("strengthGoal")
    
    # initial calculations
    caffeine         = 0                    
    beta_alanine     = 0                        
    creatine         = 0                      
    agmatine_sulfate = 0                        
    citrulline_malate= 0                        
    l_citrulline     = 0                        
    l_theanine       = 0                        
    l_tyrosine       = 0                        
    taurine          = 0                        
    betaine          = 0                        
                    
    # factoring in goals
    if pumpGoal:
        l_citrulline += 1           
        agmatine_sulfate += 1       
        citrulline_malate += 1     
    if energyGoal:
        if not (stim == "none" or stim == "low"):            
            caffeine += 1  
        creatine += 1               
        beta_alanine += 1  
    if focusGoal:
        l_theanine += 1             
        l_tyrosine += 1             
        taurine += 1                
    if enduranceGoal:
        beta_alanine += 1           
    if strengthGoal:
        creatine += 1               
        l_citrulline += 1           
        beta_alanine += 1           
        betaine += 1 
                       
    # factoring in preferences
    match stim:
        case "none":
            caffeine = 0
        case "low":
            caffeine += 1
        case "moderate":
            caffeine += 2
        case "high":
            caffeine += 3
        case "any":
            caffeine += 0

    return caffeine, beta_alanine, creatine
           
def calculate_ranges():
    """ calculates ingredient ranges based on ingredient weights and stores in session
        TODO: calculate ranges -- maybe split into different methods
    """
    caffeine, beta_alanine, creatine = calculate_ingredient_weights()
    
    # convert weight to kg
    # kg = int(session.get("weight")) * 0.453592
    
    caffeine_min = 0
    caffeine_max = 0
    if caffeine == 1:
        caffeine_min = 50
        caffeine_max = 100
    elif caffeine == 2:
        caffeine_min = 100
        caffeine_max = 200
    elif caffeine == 3:
        caffeine_min = 200
        caffeine_max = 300
    elif caffeine == 4:
        caffeine_min = 300
        caffeine_max = 500
    
    beta_alanine_min = 0
    beta_alanine_max = 0
    if beta_alanine == 1:
        beta_alanine_min = 1
        beta_alanine_max = 2.5
    if beta_alanine == 2:
        beta_alanine_min = 2.5
        beta_alanine_max = 3.9
    if beta_alanine == 3:
        beta_alanine_min = 4.5
        beta_alanine_max = 6.4
    
    creatine_min = 0
    creatine_max= 0
    if creatine == 1:
        creatine_min = 3
        creatine_max = 5
    if creatine == 2:
        creatine_min = 5
        creatine_max = 15
    
    agmatine_sulfate_min = 0
    agmatine_sulfate_max = 0
    
    citrulline_malate_min = 0
    citrulline_malate_max = 0
    
    l_citrulline_min = 0
    l_citrulline_max = 0
    
    l_theanine_min = 0
    l_theanine_max = 0
    
    l_tyrosine_min = 0
    l_tyrosine_max = 0
    
    taurine_min = 0
    taurine_max = 0
    
    betaine_min = 0
    betaine_max = 0
    
    return caffeine_min, caffeine_max, beta_alanine_min, beta_alanine_max, creatine_min, creatine_max
           


if __name__ == "__main__":
    app.run(debug=True)