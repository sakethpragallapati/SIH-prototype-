from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection, init_db, get_topic_content
import os
import sqlite3

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management and flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, name) VALUES (?, ?)', (username, name))
            conn.commit()
            flash('Information saved successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another.', 'error')
        finally:
            conn.close()

        return redirect(url_for('success'))

    return render_template('index1.html')

@app.route('/success')
def success():
    return render_template('index2.html')

@app.route('/levels')
def levels():
    return render_template('levels.html')

@app.route('/executive/level1')
def executive_level1():
    content = get_topic_content('Article 52')
    return render_template('executive/executive_level1.html', topic_content=content)

@app.route('/legislative/level1')
def legislative_level1():
    # Update this route to fetch legislative content as needed
    return render_template('legislative_level1.html')

@app.route('/judiciary/level1')
def judiciary_level1():
    # Update this route to fetch judiciary content as needed
    return render_template('judiciary_level1.html')

@app.route('/executive/level1/quiz')
def executive_level1_quiz():
    return render_template('executive/executive_level1quiz.html')

@app.route('/quiz')
def quiz():
    return render_template('/executive/quiz.html')



if __name__ == '__main__':
    init_db()
    app.run(debug=True)