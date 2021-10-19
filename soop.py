from enum import unique
from flask import Flask, render_template, url_for, redirect, flash, request
from flask.globals import session
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import  UserMixin, current_user
import re



pattern=re.compile(r"")

app=Flask(__name__, template_folder='temp')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='sathi'
db=SQLAlchemy(app)


class chat(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column('name',db.String(100))
    email=db.Column('email',db.String(100),unique=True)
    user_name=db.Column('user_name',db.String(200),unique=True)
    
    password=db.Column('password',db.String(100))
    gender=db.Column('gender',db.String(200))
    education=db.Column('education',db.String(200))

    def __init__(self,name,email,password,user_name,gender,education):
        self.name=name
        self.email=email
        self.user_name=user_name
        self.password=password
        self.gender=gender
        self.education=education

    def is_active(self):
        return True


@app.route('/', methods=["GET","POST"])
def signup():
    if request.method=='POST':
        name=request.form['nm']
        email=request.form["email"]
        user_name=request.form["user_name"]
        password=request.form['password']
        gender=request.form["male"]
        education=request.form['education']
        
        user=chat.query.filter_by(email=email).first()
        user_name=chat.query.filter_by(user_name=user_name).first()
        if len(name)<2:
            flash('name must be > 2')
        elif len(email)<4:
            flash('email Too Short. Must be > 4')
        
        if 15 > len(password)<7:
            flash('password must be b/w 7-15')
        elif re.search(r'[!@#$%&]',password) is None:
            flash('password shoult contain atleast one Special_character')
        elif re.search(r'[1-9]',password) is None:
            flash('should contain one number')
        elif re.search(r'[a-z]',password) is None:
            flash('should contain latters')
        else:   
            if user:
                flash('this email already exist ! login here')
                return redirect(url_for('login'))
            

            flash('Signup Success',category='success')
            add_items=chat(name,email,password,user_name,gender,education)
            db.session.add(add_items)
            db.session.commit()
            
            return redirect(url_for('login'))

    return render_template("signup.html",user=current_user)


@app.route('/home')

def home():
    
    a=chat.query.all()
    
    
    return render_template('home.html',user=current_user)


@app.route('/login', methods=["GET",'POST'])
def login():
    if request.method=='POST':
    
        email=request.form['email']
        password=request.form['password']
        user=chat.query.filter_by(email=email).first()
        pas=chat.query.filter_by(password=password).first()
        
        if user :
            if pas :
                flash('Login successfull')
                
                return redirect(url_for('home'))
            else:
                flash('incorrect login, try again')
                
        else:
            flash('user not exist Create your account')
            return redirect(url_for('signup'))


    
    return render_template('login.html',user=current_user)

if __name__=="__main__":
    # db.create_all()
    app.run(debug=True)