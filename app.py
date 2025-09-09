from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'gizli_anahtar'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'reservations.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    salon = db.Column(db.String(100), nullable=False)

salons = [
    "Sefaköy Kültür Merkezi",
    "Cennet Kültür Merkezi",
    "Atakent Kültür Merkezi"
]

hours = [
    "09:00-10:00",
    "10:00-11:00",
    "11:00-12:00",
    "12:00-13:00",
    "13:00-14:00",
    "14:00-15:00",
    "15:00-16:00",
    "16:00-17:00",
    "17:00-18:00"
]

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    reservations = Reservation.query.all()
    return render_template('index.html', reservations=reservations, salons=salons, hours=hours)

@app.route('/reserve', methods=['POST'])
def reserve():
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']
    salon = request.form['salon']

    existing = Reservation.query.filter_by(salon=salon, date=date, time=time).first()
    if existing:
        flash(f"{salon} bu tarih ve saat aralığında doludur. Lütfen başka bir zaman veya salon seçiniz.", 'danger')
        return redirect(url_for('index'))

    reservation = Reservation(name=name, date=date, time=time, salon=salon)
    db.session.add(reservation)
    db.session.commit()

    flash("Rezervasyon başarıyla eklendi!", 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
