from flask import Flask, render_template, request,redirect, url_for
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    """A Model for an Item in the Todo List

    Args:
        db (_type_): database model

    Returns:
        __repr__: string rep.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r' % self.id

@app.route('/', methods=["POST","GET"])
def index():
    """Main page for App

    Returns:
        page: home page
    """
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error:{e}")
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    """delete an item from the todo list

    Args:
        id (int): uuid for each item in the todo list

    Returns:
        redirect: delete and return to home
    """
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()  
        return redirect("/")
    except Exception as e:
        return f"Error:{e}"

@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    """update an item from the todo list

    Args:
        id (int): uuid for each item in the todo list

    Returns:
        redirect: update and return to home
    """
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return "Error"
    else:
        return render_template("update.html", task=task)

if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)