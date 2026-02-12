from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "key"

# <><><> MAIN PAGE <><><>
@app.route("/")
def home():
    return render_template("home.html")

# <><><> QUIZ PAGES <><><>
@app.route("/quiz")
def quiz():
    return render_template("quiz_template.html", usr=session.get("user"))

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
    return render_template("qName.html", usr=session.get("user"))

@app.route("/quiz/weight", methods=["GET", "POST"])
def weight():
    """ asks user for weight and stores in session. redirects to results page.

    Returns:
        _type_: render_template or redirect
        renders weight question page or redirects to results page
    """
    if request.method == "POST":
        session["weight"] = request.form.get("weight", "").strip()
        return redirect(url_for('results'))
    return render_template("qWeight.html", usr=session.get("user"))
    
# goals question (pump/energy/endurance)
    
@app.route("/quiz/results", methods=["GET", "POST"])
def results():
    """ displays quiz results. placeholder for future slider adjustment page.

    Returns:
        _type_: render_template
        renders quiz results page with user name and weight displayed.
    """
    return render_template("qResults.html", usr=session.get("user"), weight=session.get("weight"))

# slider adjustment page

# product match page (database)

if __name__ == "__main__":
    app.run(debug=True)