from flask import Flask, session, render_template, request, redirect, url_for, flash
from sqlite3 import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL

# Configure application
app = Flask(__name__)
# Connect to the db called users.db
db = SQL("sqlite:///users.db")

app.secret_key = 'your_secret_key'

# Direct 
@app.route("/")
def index():
    return redirect("/home")

# Home Route
@app.route('/home')
def home():
    user_id = session.get("user_id")
    username = session.get("username")
    return render_template("index.html", user_id=user_id, username=username)

# Login Route
@app.route ('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check for missing username or password
        if not username or not password:
            flash("Must provide username and password", "danger")
            return redirect("/login")
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1 and check_password_hash(rows[0]["hash"], password):
            session["user_id"] = rows[0]["id"]  # Store user ID in session
            session["username"] = username  # Store the username for log in greeting
            flash("Login successful!", "success")
            return redirect("/home")

        flash("Invalid username or password", "danger")
    
    return render_template("login.html")

# Register Route
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        email = request.form.get("email")

        # Validate inputs
        if not username or not password or not confirmation or not email:
            flash("Must provide all fields", "danger")
            return redirect("/register")

        # Check if passwords match
        if password != confirmation:
            flash("Passwords do not match", "danger")
            return redirect("/register")

        # Check if username or email already exists
        existing_user = db.execute("SELECT * FROM users WHERE username = ? OR email = ?", username, email)
        if existing_user:
            flash("Username or email already exists", "danger")
            return redirect("/register")

        # Insert the new user into the database
        try:
            user_id = db.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)",
                                 username, email, generate_password_hash(password))
        except IntegrityError:
            flash("Error: Username already exists", "danger")
            return redirect("/register")

        session["user_id"] = user_id
        session["username"] = username
        flash("Registration successful!", "success")
        return redirect("/home")
    
    return render_template("register.html")

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been successfully logged out.", "success")
    return redirect(url_for("home"))

# Contact Route
@app.route('/contact')
def contact():
    user_id = session.get("user_id")
    return render_template("contact.html", user_id=user_id)

# To do list app
@app.route("/addTask", methods=["POST"])
def addTask():
    # Get the users logged-in user's ID
    user_id = session.get("user_id")
    if not user_id:
        flash("You need to be logged in for this", "danger")
        return redirect("/login")
    
    # Get the task from the form 
    task = request.form.get("task")
    
    if task:
        db.execute("INSERT INTO tasks (user_id, task) VALUES (?,?)", user_id, task)
        flash("Task added successfully!", "success")
    else:
        flash("Task cannot be empty", "danger")
        
    return redirect("/todo")

@app.route("/todo")
def todo():
    user_id = session.get("user_id")
    if not user_id:
        # Prompts user to be logged in
        flash ("You need to log in first", "danger")
        return redirect("/login")
    # Displays tasks
    tasks = db.execute("SELECT * FROM TASKS WHERE user_id = ?", user_id)
    return render_template("todo.html", tasks=tasks)

@app.route("/markCompleted/<int:task_id>", methods=["POST"])
def markCompleted(task_id):
    # Update the task as completed in the db
    db.execute("UPDATE tasks SET completed = 1 WHERE id = ? ", task_id)
    flash("Task marked as completed!", "success")
    return redirect("/todo")

@app.route("/delete_task/<int:task_id>", methods=["POST"])
def deleteTask(task_id):
    # Delete the task from the DB
    db.execute("DELETE FROM tasks WHERE id = ?", task_id)
    flash("Task deleted successfully!", "success")
    return redirect("/todo")

@app.route("/pomodoro")
def pomodoro():
    return render_template("pomodoro.html")

if __name__== '__main__':
    app.run(debug=True)
