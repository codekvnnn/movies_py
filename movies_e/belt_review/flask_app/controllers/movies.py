from flask_app import app 
from flask import render_template, redirect,session,request 
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/movies/dashboard')
def dashboard():
    data={
        'id': session['logged_in_id']
    }
    return render_template('dashboard.html', movie.Movie.get_all_movies(), one_user=user.User.get_user_by_id(data))

@app.route('/movies/new')
def new_movie():
    return render_template('new_movie.html')

@app.route('/movies/create', methods=['POST'])
def create_movie():
    if not movie.Movie.validate_movie(request.form):
        return redirect('/movies/new')
    movie.Movie.save_movie(request.form)
    