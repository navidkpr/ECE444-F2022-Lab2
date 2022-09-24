from crypt import methods
from datetime import datetime
import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from dotenv import load_dotenv
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, StopValidation, Regexp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('APP_SECRET_KEY', 'very_very_secret_key')
bootstrap = Bootstrap(app)
moment = Moment(app)

class UofTEmail:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not field.data or field.data == "":
            return
        if "@" not in field.data:
            message = field.gettext("Please include '@' in the email address. '{}'. is missing '@'.".format(field.data))
        else:
            message = self.message

        field.errors[:] = []
        raise StopValidation(message)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email_address= StringField('What is your UofT email address?', validators=[UofTEmail()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email_address = session.get('email_address')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email_address is not None and old_email_address != form.email_address.data:
            flash('Looks like you have changed your UofT email!')
        session['name'] = form.name.data
        session['email_address'] = form.email_address.data
        return redirect(url_for('index'))
    return render_template('index.html',
        form = form, name = session.get('name'), email_address = session.get('email_address'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    load_dotenv()
    app.run(debug = (os.getenv('ENV', 'production') == 'development'))