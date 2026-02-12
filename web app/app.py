from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "key"

# <><><> MAIN PAGE <><><>
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/quiz")
def quiz():
    return render_template("quiz_template.html", usr=session.get("user"))

@app.route("/quiz/name", methods=["GET", "POST"])
def name():
    # what happens when user submits their name
    if request.method == "POST":
        session["user"] = request.form.get("user", "").strip()
        return redirect(url_for('weight'))
    return render_template("qName.html", usr=session.get("user"))

@app.route("/quiz/weight", methods=["GET", "POST"])
def weight():
    if request.method == "POST":
        session["weight"] = request.form.get("weight", "").strip()
        return redirect(url_for('results'))
    return render_template("qWeight.html", usr=session.get("user"))
    
@app.route("/quiz/results", methods=["GET", "POST"])
def results():
    return render_template("qResults.html", usr=session.get("user"), weight=session.get("weight"))

if __name__ == "__main__":
    app.run(debug=True)