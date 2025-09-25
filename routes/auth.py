
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.user import User, db
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from extensions.mail import mail

auth = Blueprint('auth', __name__)
s = URLSafeTimedSerializer('your-secret-key')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt='password-reset-salt')
            link = url_for('auth.reset_with_token', token=token, _external=True)
            msg = Message('Password Reset Request', recipients=[email])
            msg.body = f'Click the link to reset your password: {link}'
            mail.send(msg)
            flash('Password reset email sent.')
        else:
            flash('Email not found.')
    return render_template('reset_password.html')

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The reset link is invalid or has expired.')
        return redirect(url_for('auth.reset_password'))

    if request.method == 'POST':
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(request.form['password'])
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
    return render_template('reset_with_token.html')
