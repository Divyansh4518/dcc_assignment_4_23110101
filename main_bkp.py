from flask import Flask, redirect, url_for, request, Response, render_template
from sqlalchemy import text
from sqlalchemy import create_engine, text
import sqlalchemy
import pymysql
from flask_mysqldb import MySql
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy to work with our Flask application
db = SQLAlchemy(app)

# Define a model for the 'genre' table
class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return f'<Genre {self.id}: {self.name}>'

@app.route('/')
def main_page():
    # Retrieve data from the 'genre' table
    genres = Genre.query.all()
    return render_template('index.html', genres=genres)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="0.0.0.0", port="80", debug = True) 
