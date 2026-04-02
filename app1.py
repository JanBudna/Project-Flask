from flask import Flask, render_template, request, session, redirect
from tinydb import TinyDB, Query

app = Flask(
    __name__,
    template_folder="templates1",
    static_folder="static1"
)
app.secret_key = "adminCode08"

db = TinyDB("database.json")
users = db.table("users")
User = Query()

@app.route("/")
def homePage():
    if "user" in session:
        return redirect("/dashboard")
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
            return redirect("/dashboard")
        else:
            return "Napačen login"

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")

    user = users.get(User.username == session["user"])

    if user is None:
        session.clear()
        return redirect("/login")

    notes = user.get("notes", [])

    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            content = request.form["content"]
            title = request.form["title"]
            if not title:
                return "Title is required!"
            
            new_note = {"title": title, "content": content}
            notes.append(new_note)

        elif action == "delete":
            note_id = int(request.form["note_id"])
            if 0 <= note_id < len(notes):
                notes.pop(note_id)

        users.update({"notes": notes}, User.username == session["user"])
        return redirect("/dashboard")

    return render_template("dashboard.html", user=session["user"], notes=notes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)