from flask import Flask, render_template, session, request, redirect, jsonify
from tinydb import TinyDB, Query

app = Flask(
    __name__,
    template_folder="templates3",
    static_folder="static3"
)
app.secret_key = "adminCode08"

db = TinyDB("database2.json")
users = db.table("users")
User = Query()

@app.route("/")
def homePage():
    if "user" in session:
        return redirect("/market")
    return redirect("/login")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.search(User.username == username):
            return "Uporabnik že obstaja"

        users.insert({"username" : username, "password" : password})
        return redirect("/login")
    else:
        return render_template("register.html")
    
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.get(User.username == username)
        
        if user and user["password"] == password:
            session["user"] = username
            return redirect("/market")
        else:
            return "Napačen login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/market")
def market():
    if "user" not in session:
        return redirect("/login")

    current_user = users.get(User.username == session["user"])

    if current_user is None:
        session.clear()
        return redirect("/login")
    
    if request.method == "POST":
        action = request.form.get("action")
    
    return render_template("market.html", user=session["user"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)