from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)  # New column for completion
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

# Home Page - Add & Display Tasks
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# Toggle Task Completion
@app.route('/complete/<int:id>')
def complete(id):
    task = Todo.query.get_or_404(id)
    try:
        task.completed = not task.completed  # Toggle between True/False
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem updating that task'

# Delete a Task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

# Create the database if it doesn't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
