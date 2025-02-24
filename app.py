print("Flask app is starting...")

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pet_haven.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ---------------------- MODELS ---------------------- #

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email_id = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(10))
    address = db.Column(db.String(50))
    user_type = db.Column(db.String(20))  # Pet Owner, Service Provider, Admin
    is_active = db.Column(db.Boolean, default=True)

class Service(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50))

class ServiceProvider(db.Model):
    __tablename__ = 'service_provider'
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    state = db.Column(db.String(30))
    city = db.Column(db.String(30))
    hourly_rate = db.Column(db.String(15))
    experience = db.Column(db.String(255))
    description = db.Column(db.String(255))
    document_folder = db.Column(db.String(255))
    status = db.Column(db.String(20))  # Pending, Accepted, Rejected

# ---------------------- ROUTES ---------------------- #

@app.route('/')
def home():
    return render_template('registration_login_page.html')

@app.route('/register', methods=['POST'])
def register():
    user_name = request.form['username']
    email = request.form['email']
    password = generate_password_hash(request.form['password'])
    user_type = request.form['user_type']

    new_user = User(user_name=user_name, email_id=email, password=password, user_type=user_type)
    db.session.add(new_user)
    db.session.commit()

    # If Service Provider, handle document upload
    if user_type == 'Service Provider':
        service_id = request.form['service_id']
        documents = request.files.getlist('documents')
        upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], email)
        os.makedirs(upload_folder, exist_ok=True)

        for doc in documents:
            doc.save(os.path.join(upload_folder, doc.filename))

        service_provider = ServiceProvider(
            service_id=service_id,
            user_id=new_user.user_id,
            state=request.form['state'],
            city=request.form['city'],
            hourly_rate=request.form['hourly_rate'],
            experience=request.form['experience'],
            description=request.form['description'],
            document_folder=upload_folder,
            status='Pending'
        )
        db.session.add(service_provider)
        db.session.commit()

    flash('Registration successful!')
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email_id=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.user_id
        session['user_type'] = user.user_type
        flash('Login successful!')
        return redirect(url_for('home'))
    else:
        flash('Invalid credentials!')
        return redirect(url_for('home'))

# ---------------------- MAIN ---------------------- #

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
