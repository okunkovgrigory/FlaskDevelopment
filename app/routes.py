# -*- coding: utf-8 -*-
from collections import namedtuple
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

Message = namedtuple('Message', 'text tag')
messages = []


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Denis'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Oksana'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Аnfis'},
            'body': 'My favourite car is Porsche!!'
        }
    ]

    return render_template('index.html', title='Home', posts=posts)


@app.route('/add_messages', methods=['GET', 'POST'])
def add_messages():
    text = request.form['text']
    tag = request.form['tag']
    messages.append(Message(text, tag))
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f'Неверное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(index))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Post #1'},
        {'author': user, 'body': 'Post #2'}
    ]
    return render_template('user.html', title=user.username, user=user, posts=posts)

