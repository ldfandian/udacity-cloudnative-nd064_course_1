import sqlite3
import sys
import logging
import threading

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Utils class to establish database connection, and track total connection count
class DatabaseConnection(object):
    counterLock = threading.Lock()
    connectionCount = 0
    connectionTotal = 0

    def __enter__(self):
        # Function to get a database connection.
        # This function connects to database with the name `database.db`
        self.connection = sqlite3.connect('database.db')
        self.connection.row_factory = sqlite3.Row
        with DatabaseConnection.counterLock:
            DatabaseConnection.connectionCount += 1
            DatabaseConnection.connectionTotal += 1
        return self.connection

    def __exit__(self, type, value, trace):
        self.connection.close()
        with DatabaseConnection.counterLock:
            DatabaseConnection.connectionCount -= 1

# Function to get the count of all posts
def get_post_count():
    with DatabaseConnection() as connection:
        count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
        return count

# Function to get all post
def get_all_posts():
    with DatabaseConnection() as connection:
        posts = connection.execute('SELECT * FROM posts').fetchall()
        return posts

# Function to get a post using its ID
def get_post(post_id):
    with DatabaseConnection() as connection:
        post = connection.execute('SELECT * FROM posts WHERE id = ?',
                            (post_id,)).fetchone()
        return post

# Function to get a post using its ID
def create_post(title, content):
    with DatabaseConnection() as connection:
        connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                        (title, content))
        connection.commit()
        return

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    posts = get_all_posts()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info('A non-existing article is accessed and a 404 page is returned.')
        return render_template('404.html'), 404
    else:
        app.logger.info('An existing article is retrieved. Title: ' + post["title"])
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('The "About Us" page is retrieved.')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            create_post(title, content)
            app.logger.info('A new article is created. Title: ' + title)
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route("/status")
def getStatus():
    response = app.response_class(
        response=json.dumps(
            {
                "result":"OK - healthy"
            }
        ),
        status=200,
        mimetype='application/json'
    )

    return response

@app.route("/metrics")
def getMetrics():
    # read the count of total posts
    countPosts = get_post_count()

    response = app.response_class(
        response=json.dumps(
            {
                "status":"success",
                "code":0,
                "data":{
                    "db_connection_count": DatabaseConnection.connectionCount,
                    "db_connection_total": DatabaseConnection.connectionTotal,
                    "post_count": countPosts
                }
            }
        ),
        status=200,
        mimetype='application/json'
    )

    return response

# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    app.run(host='0.0.0.0', port='3111')
