from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_mysql_username'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_mysql_database'
mysql = MySQL(app)


@app.route('/')
def index():
    # Fetch all records from the database
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()

    return render_template('index.html', users=users)


@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']

        # Insert data into the database
        cur = mysql.connection.cursor()
        cur.execute(
            'INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']

        # Update data in the database
        cur.execute('UPDATE users SET name=%s, email=%s WHERE id=%s',
                    (name, email, user_id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))

    # Fetch user data from the database
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cur.fetchone()
    cur.close()

    return render_template('edit.html', user=user)


@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    # Delete user from the database
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = %s', (user_id,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
