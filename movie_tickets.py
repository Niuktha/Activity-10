from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('movie_tickets.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                (id INTEGER PRIMARY KEY, title TEXT NOT NULL, director TEXT NOT NULL, genre TEXT NOT NULL, release_date TEXT NOT NULL, ticket_price REAL NOT NULL, available_seats INTEGER NOT NULL)''')
conn.commit()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM movies LIMIT 1")
    movie = cursor.fetchone()
    return render_template('index.html', movie=movie)

@app.route('/movies')
def movies():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    return render_template('movies.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['movie_title']
        director = request.form['movie_director']
        genre = request.form['movie_genre']
        release_date = request.form['release_date']
        ticket_price = request.form['ticket_price']
        available_seats = request.form['available_seats']
        cursor.execute("INSERT INTO movies (title, director, genre, release_date, ticket_price, available_seats) VALUES (?, ?, ?, ?, ?, ?)",
                       (title, director, genre, release_date, ticket_price, available_seats))
        conn.commit()
        return redirect(url_for('movies'))
    return render_template('add_movie.html')

@app.route('/update_movie/<int:id>', methods=['GET', 'POST'])
def update_movie(id):
    if request.method == 'POST':
        title = request.form['movie_title']
        director = request.form['movie_director']
        genre = request.form['movie_genre']
        release_date = request.form['release_date']
        ticket_price = request.form['ticket_price']
        available_seats = request.form['available_seats']
        cursor.execute("UPDATE movies SET title=?, director=?, genre=?, release_date=?, ticket_price=?, available_seats=? WHERE id=?",
                       (title, director, genre, release_date, ticket_price, available_seats, id))
        conn.commit()
        return redirect(url_for('movies'))
    cursor.execute("SELECT * FROM movies WHERE id=?", (id,))
    movie = cursor.fetchone()
    return render_template('update_movie.html', movie=movie)

@app.route('/delete_movie/<int:id>', methods=['POST'])
def delete_movie(id):
    cursor.execute("DELETE FROM movies WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for('movies'))

if __name__ == '__main__':
    app.run(debug=True)
