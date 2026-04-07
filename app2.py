from flask import Flask, render_template, session, request, redirect, jsonify
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

        users.insert({"username" : username, "password" : password, "post" : []})
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

@app.route("/media", methods = ["GET", "POST"])
def media():
    if "user" not in session:
        return redirect("/login")
    
    user = users.get(User.username == session["user"])
    all_users = users.all() 
    
    if user is None:
        session.clear()
        return redirect("/login")

    posts = user.get("post", [])

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            content = request.form.get("content")
            new_post = {"content": content}
            posts.append(new_post)
            users.update({"post": posts}, User.username == session["user"])
            return redirect("/media")

    return render_template("media.html", user=session["user"], post=posts, all_users=all_users)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
