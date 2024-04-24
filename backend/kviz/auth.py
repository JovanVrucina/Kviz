import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from kviz.database import get_db

#Create blueprint auth
bp = Blueprint('auth', __name__, url_prefix='/auth') 

#Registration
@bp.route('/register', methods=('GET', 'POST'))
def register():

    #Fetches email and password from form 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required!'
        elif not password:
            error = 'Password is required!'
        
        if error is None:
            try:

                #Inserting email and password (password hash) into the database
                db.execute(
                    "INSERT INTO user (email, password) VALUES (?, ?)",
                    (email, generate_password_hash(password)),              
                )
                db.commit()
            except db.IntegrityError:

                #If the email already exists, it creates an error
                error = f"Email {email} is already registered"
            else:

                #If using GET method, it will redirect to login page
                return redirect(url_for('auth.login')) 
            
        #Showing the errror to the user
        flash(error)

    return render_template('auth/register.html')

#Login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        #Gets email and password from form
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            #Looks for email in the database, fetches only one row
            'SELECT * FROM user WHERE email = ?',
            (email,).fetchone() 
        )

        if user is None:
            error = 'Incorrect email'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        
        if error is None:
            #Sends the user id cookie to browser
            session.clear() 
            session['user_id'] = user['id']
            return redirect(url_for('index'))
    #Shows user the error    
    flash(error)

    return render_template('auth/login.html')

