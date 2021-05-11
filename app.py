from flask import Flask , render_template , request, redirect ,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_MODIFICATIONS']= False
db=SQLAlchemy(app)

class ToDo(db.Model):
    s_no =db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500),  nullable=False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.s_no} - {self.title}"

@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo=ToDo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route('/show')
def product():
    alltodo=ToDo.query.all()

    return "its production"

@app.route('/update/<int:s_no>',methods=['GET','POST'])
def update(s_no):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=ToDo.query.filter_by(s_no= s_no).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo=ToDo.query.filter_by(s_no= s_no).first()
    return render_template("update.html", todo=todo)



@app.route('/delete/<int:s_no>')
def delete(s_no):
    todo=ToDo.query.filter_by(s_no=s_no).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)
