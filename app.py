from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
app = Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db  = SQLAlchemy(app)



class Todo(db.Model):
     sno = db.Column(db.Integer,primary_key =True )
     title= db.Column(db.String(200), nullable = False)
     description = db.Column(db.String(200),nullable= False )
     time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 

     def __repr__(self) -> str:
                return f"{self.sno} - {self.title}"


@app.route("/")
def landing():
    return render_template('landing.html')

@app.route("/todos")
def todos():
    alltodo = Todo.query.all()
    return render_template('index.html', alltodo=alltodo)

@app.route("/add_task", methods = ['GET','POST'])
def add_task():
    if request.method == 'POST':
        todo_title = request.form['title']
        description_todo = request.form['description']
        data = Todo(title=todo_title,description=description_todo)
        db.session.add(data)
        db.session.commit()
        return redirect("/view_tasks")
    return render_template('add_task.html')

@app.route("/view_tasks")
def view_tasks():
    alltodo = Todo.query.all()
    return render_template('view_tasks.html', alltodo=alltodo)

@app.route("/search")
def search():
        query = request.args.get('query', '')
        if query:
               search_term = f"%{query}%"
               search_results = Todo.query.filter(
                      (Todo.title.like(search_term)) | 
                      (Todo.description.like(search_term))
               ).all()
        else:
               search_results = []
        
        return render_template('search_results.html', 
                              todos=search_results, 
                              query=query)

@app.route("/update/<int:sno>" , methods = ['GET','POST'])
def update (sno):
        
        if request.method == 'POST':
               todo_title = request.form['title']
               description_todo = request.form['description']
               data = Todo.query.filter_by(sno=sno).first()
               data.title = todo_title
               data.description = description_todo
               db.session.add(data)
               db.session.commit()
               return redirect("/view_tasks")
        todo =Todo.query.filter_by(sno=sno).first()
        return render_template('update.html',todo=todo)
       


@app .route("/delete/<int:sno>")
def delete (sno):
        todo =Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/view_tasks")

if __name__ == "__main__":
   app.run(debug =True)