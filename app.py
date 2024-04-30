# -*- coding: utf-8 -*-
from alembic import op
import sqlalchemy as sa
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configura l'applicazione Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# La funzione upgrade viene eseguita quando viene eseguito l'aggiornamento del database
def upgrade():
    # Utilizza op.add_column per aggiungere una nuova colonna al modello User
    op.add_column('user', sa.Column('surname', sa.String(length=100), nullable=False))


# La funzione downgrade viene eseguita quando viene eseguito il rollback dell'aggiornamento del database
def downgrade():
    # Utilizza op.drop_column per rimuovere la colonna 'surname' dal modello User
    op.drop_column('user', 'surname')

# Definisci il modello User con i campi necessari
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    house_size = db.Column(db.Float, nullable=False)
    num_lights = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    light_type = db.Column(db.String(100), nullable=False)
    light_energy_consumption = db.Column(db.Float, nullable=False)


# Calcola il consumo energetico totale dell'utente
def calculate_total_energy_consumption(user):
    return user.num_lights * user.light_energy_consumption

# Ottieni la media del consumo energetico per tipo di lampadina
def get_average_energy_consumption(light_type):
    # Simulazione di implementazione
    if light_type == "LED":
        return 10  # Media del consumo energetico per lampadine LED
    elif light_type == "Incandescent":
        return 50  # Media del consumo energetico per lampadine incandescenti
    elif light_type == "CFL":
        return 20  # Media del consumo energetico per lampadine CFL
    else:
        return 30  # Media di default

# Implementa la logica per confrontare il consumo energetico dell'utente con la media del tipo di lampadina e fornire consigli appropriati
def generate_energy_advice(user):
    average_energy_consumption = get_average_energy_consumption(user.light_type)
    total_energy_consumption = calculate_total_energy_consumption(user)
    if total_energy_consumption > average_energy_consumption:
        return "Hai un consumo energetico superiore alla media per le lampadine che possiedi. Considera di passare a lampadine a LED per ridurre il consumo."
    else:
        return "Il tuo consumo energetico è nella media per le lampadine che possiedi. Continua così!"

# Definisci le route dell'applicazione
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Logica per gestire il form POST
        # Recupera i dati dell'utente dal database
        user = User.query.filter_by(id=1).first()  # Esempio: recupera l'utente con ID 1
        advice = generate_energy_advice(user)
        return render_template("dashboard.html", advice=advice)
    else:
        # Logica per gestire la richiesta GET
        risultato = 0
        return render_template("dashboard.html", risultato=risultato)

@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        # Logica per la registrazione di un nuovo utente
        name = request.form.get("nome")
        surname = request.form.get("cognome")
        email = request.form.get("email")
        password = request.form.get("password")
        house_size = request.form.get("dimensioni_abitazione")
        num_lights = request.form.get("num_lampadine")
        location = request.form.get("luogo_abitazione")
        light_type = request.form.get("tipo_lampadina")
        light_energy_consumption = request.form.get("consumo_energetico_lampadina")

        # Verifica se i valori numerici sono presenti prima di convertirli in float
        if house_size is not None and house_size != "":
            house_size = float(house_size)
        else:
            house_size = 0.0  # Imposta un valore predefinito se il valore è None o vuoto
        
        if num_lights is not None and num_lights != "":
            num_lights = int(num_lights)
        else:
            num_lights = 0  # Imposta un valore predefinito se il valore è None o vuoto

        if light_energy_consumption is not None and light_energy_consumption != "":
            light_energy_consumption = float(light_energy_consumption)
        else:
            light_energy_consumption = 0.0  # Imposta un valore predefinito se il valore è None o vuoto

        # Crea l'oggetto utente dopo aver ottenuto tutti i dati
        user = User(name=name, surname=surname, email=email, password=password, house_size=house_size, num_lights=num_lights, location=location, light_type=light_type, light_energy_consumption=light_energy_consumption)
        
        # Calcola il consumo energetico totale dell'utente
        total_energy_consumption = calculate_total_energy_consumption(user)

        # Ottieni la media del consumo energetico per tipo di lampadina
        average_energy_consumption = get_average_energy_consumption(light_type)

        # Confronta il consumo energetico dell'utente con la media e fornisce consigli
        # Implementa la logica qui

        # Registra l'utente nel database
        db.session.add(user)
        db.session.commit()

        return redirect('/dashboard')
    else:
        # Logica per gestire la richiesta GET
        return render_template('registration.html', tipo_account="Propria abitazione")

# Route per la pagina di login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logica per la gestione del login
        # Verifica le credenziali dell'utente
        email = request.form.get('email')
        password = request.form.get('password')
        # Cerca l'utente nel database per email
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            # Credenziali corrette, reindirizza alla dashboard o ad altra pagina
            return redirect(url_for('dashboard'))
        else:
            # Credenziali errate, mostra un messaggio di errore
            error = "Credenziali non valide. Riprova."
            return render_template('login.html', error=error)
    else:
        # Logica per gestire la richiesta GET
        return render_template('login.html')

# Avvia l'applicazione Flask
if __name__ == "__main__":
    app.run(debug=True)
