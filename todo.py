from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Melish/Desktop/TodoApp/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos=Todo.query.all()
    return render_template("index.html",todos=todos)

@app.route("/add",methods=["POST"])
def add():
    title=request.form.get("title") #burdaki "title" index.htmldeki inputun name sidir ))
    newTodo=Todo(title=title,completed=False)
    db.session.add(newTodo)
    db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def complete(id):
    todo=Todo.query.filter_by(id=id).first()
    # if todo.completed==True:
    #     todo.completed=False
    # else:
    #     todo.completed=True
    
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for("index"))



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    completed = db.Column(db.Boolean)

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)