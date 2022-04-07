from flask import Flask, request, flash, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import re

from person_data import TELEGRAM, WHATS_UP, VK_PAGE, DB_CONFIG

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eiwbi8839183y84iuqh39731hx'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONFIG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


class Client(db.Model):
    __tablename__ = 'clients'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40))
    email=db.Column(db.String(40))
    message = db.Column(db.String(150))


@app.route('/', methods=['POST', 'GET'])
def base():
    if request.method == 'POST':
        rec = request.form
        # name = rec.get('name')
        # email = rec.get('email')
        # message = rec.get('message')
        if len(rec.get('name')) < 2:
            flash('Your name must be at least 3 characters in length', category='danger')
        elif not re.fullmatch(regex, rec.get('email')):
            flash("Your e-mail isn't correct.", category='danger')
        else:
            flash('Your message sent.', category='success')
    return render_template('base.html', telegram=TELEGRAM, whats_up=WHATS_UP, vk_page=VK_PAGE)


if __name__ == '__main__':
    from errors import *

    app.run(debug=True, host='0.0.0.0', port=5001)
