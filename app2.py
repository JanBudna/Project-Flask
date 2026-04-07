from flask import Flask, render_template, session, request, redirect
from tinydb import TinyDB, Query

app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)
app.secret_key = "adminCode08"

db = TinyDB("database1.json")
users = db.table("users")
User = Query()

@app.route("/")
def homePage():
    if "user" in session:
        return redirect("/media")
    return redirect("/login")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.search(User.username == username):
            return "Uporabnik že obstaja"

        users.insert({"username" : username, "password" : password, "notes" : []})
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
            return redirect("/media")
        else:
            return "Napačen login"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/media")
def media():
    return render_template("media.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
