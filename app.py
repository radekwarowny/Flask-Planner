import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# local db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_site.db1'
# heroku db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


@app.route('/')
@app.route('/home')
def home():
    # show all todos
    tasks = Todo.query.all()
    return render_template('home.html', title='Home', tasks=tasks)


@app.route('/features')
def features():
    return render_template('features.html', title='Features')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")
    task = Todo(title=title, complete=False)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/update/<int:task_id>')
def update(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    task.complete = not task.complete
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:task_id>')
def delete(task_id):
    task = Todo.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)