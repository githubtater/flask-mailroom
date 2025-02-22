import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
try:
    app.secret_key = os.environ.get('SECRET_KEY').encode()
except AttributeError:
    print('Environment variable not found: SECRET_KEY')

@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        donor_name = Donor.get_or_none(Donor.name == request.form['name'])
        if donor_name is None:
            donor_name = Donor(name=request.form['name'])
            donor_name.save()
        Donation(donor=donor_name, value=request.form['donation']).save()
        return redirect(url_for('all'))

    return render_template('create.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='localhost', port=port)

