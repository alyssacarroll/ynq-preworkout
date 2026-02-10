from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

user = ""
lbs = ""

# <><><> MAIN PAGE <><><>
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/quiz")
def quiz():
    return render_template("quiz_template.html", usr=user)

@app.route("/quiz/name", methods=["GET", "POST"])
def name():
    global user
    if request.method == "POST":
        user = request.form.get("user", "").strip()
        return redirect(url_for('quiz'))
    return render_template("qName.html")

@app.route("/quiz/weight", methods=["GET", "POST"])
def weight():
    global lbs
    if request.method == "POST":
        lbs = request.form.get("weight", "").strip()
        return redirect(url_for('results'))
    return render_template("qWeight.html")
    
@app.route("/quiz/results", methods=["GET", "POST"])
def results():
    return render_template("qResults.html", weight=lbs)

if __name__ == "__main__":
    app.run(debug=True)