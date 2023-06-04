from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="todo_app"
)
cursor = db.cursor()

# Create a table to store todo items
cursor.execute(
    "CREATE TABLE IF NOT EXISTS todos (id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255))")


@app.route("/")
def index():
    # Retrieve all todo items from the database
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    # Get the task from the form submission
    task = request.form["task"]

    # Insert the task into the database
    cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
    db.commit()

    # Redirect to the home page
    return redirect("/")


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # Delete the todo item with the specified ID
    cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    db.commit()

    # Redirect to the home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
