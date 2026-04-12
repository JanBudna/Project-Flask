from flask import Flask, render_template, session, request, redirect, jsonify
from tinydb import TinyDB, Query
import os
from werkzeug.utils import secure_filename

app = Flask(
    __name__,
    template_folder="templates2",
    static_folder="static2"
)
app.secret_key = "adminCode08"
UPLOAD_FOLDER = "static2/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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

@app.route("/media", methods=["GET", "POST"])
def media():
    if "user" not in session:
        return redirect("/login")

    current_user = users.get(User.username == session["user"])

    if current_user is None:
        session.clear()
        return redirect("/login")

    all_users = users.all()
    posts = current_user.get("post", [])

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            content = request.form.get("content")
            file = request.files.get("image")
            image_path = ""

            if file and file.filename != "":
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                image_path = filepath

            new_post = {"content": content, "image": image_path, "likes": 0, "liked_by": []}
            posts.append(new_post)
            users.update({"post": posts}, User.username == session["user"])
            return redirect("/media")

        elif action == "like":
            username = session["user"]
            user_id = int(request.form.get("user_id"))
            post_id = int(request.form.get("post_id"))
            all_users = users.all()

            if 0 <= user_id < len(all_users):
                user_posts = all_users[user_id].get("post", [])
                if 0 <= post_id < len(user_posts):
                    post = user_posts[post_id]

                    if "liked_by" not in post:
                        post["liked_by"] = []

                    if username in post["liked_by"]:
                        return jsonify({"status": "error", "message": "Already liked"})
                    
                    post["liked_by"].append(username)
                    post["likes"] = post.get("likes", 0) + 1
                    users.update({"post": user_posts}, User.username == all_users[user_id]["username"])
                    return jsonify({"status": "success", "likes": post["likes"]})

            return jsonify({"status": "error"})

    return render_template("media.html", user=session["user"], post=posts, all_users=all_users)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
