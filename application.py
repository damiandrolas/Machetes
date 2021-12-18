import os
# import sqlalchemy


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# from flask_mail import Mail, Message

from forms import ContactForm
from helpers import apology, login_required, datetime_format, check

# import pandas as pd

# Configure application
app = Flask(__name__)

# configurar objeto mail
# mail = Mail(app)

#configurar una clave secreta para protejer los datos de la webform
app.config['SECRET_KEY'] = 'globetes1'


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///machetes.db")


@app.route("/", methods=["GET"])
def index():
    try:
        user_id = session["user_id"]
    except:
        flash(f'Necesitás loguearte para ser feliz')
    return render_template("index.html")


@app.route("/inicio/<inicio_id>", methods=["GET", "POST"])
def inicio(inicio_id):
    
    tabla_posteo = {'1':'posts','2': 'posts_2','3': 'posts_3','4': 'posts_4'}[inicio_id]
    
    datos = {"1":["images/analisis sintactico.jpg","Análisis sintáctico"], "2":["images/verbos.jpg","Verbos"],"3":["images/aparato femenino.jpg","Aparato Reproductor Femenino"],"4":["images/masculino.jpg","Aparato reproductor Masculino"]}
    ruta = url_for('static', filename= datos[inicio_id][0])
    titulo = datos[inicio_id][1]
    restos = [[url_for('static', filename=datos[key][0]), datos[key][1], key] for key in datos if key != inicio_id]
 

    try:
        user_id = session["user_id"]
        name = db.execute("SELECT username FROM users WHERE id = ?",user_id)[0]['username']
    except:
        flash(f'Necesitás loguearte para ser feliz')
        name = ""
    
    if request.method == "POST":
        body = request.form.get("comentarios")
        if not body:
            flash(f'El espacio para los comentarios está vacío')
            return redirect(f"/inicio/{inicio_id}")
        
        user_name = db.execute("SELECT username FROM users WHERE ID = ?", user_id)[0]['username']
        db.execute(f"INSERT INTO {tabla_posteo} (user_id, body, user_name) VALUES(?,?,?)", user_id, body, user_name)
        return redirect(f"/inicio/{inicio_id}")


    comentarios = db.execute(f"SELECT * FROM {tabla_posteo}")
    return render_template("inicio.html",restos=restos, titulo=titulo, ruta=ruta, comentarios=comentarios, datetime_format=datetime_format, name=name,inicio_id=inicio_id)
@app.route("/admin", methods=["GET","POST"])
def admin():
    flash(" ")
    if "admin" not in session:
        session["admin"] = False
    if request.method == "POST":
        
        if not request.form.get("password"):
            flash(f'No pusiste la contraseña de admin')
            return apology("must provide password", 403)
            
        if request.form.get("password") != "globetes1":
            flash(f'No pusiste la contraseña de admin')
            return apology("Contraseña no válida", 403)
            
        session["admin"] = True
        return redirect("/admin")
    mensajes = []
    if session["admin"]:
        mensajes = db.execute("SELECT * FROM mensajes ")

    return render_template("admin.html", admin=session["admin"], mensajes=mensajes, datetime_format=datetime_format)

@app.route('/logout_admin')
def logout_admin():
    session["admin"] = False
    return redirect("/admin")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash(f'Falta el nombre de usuario')
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash(f'Falta la contraseña')
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))


        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash(f'Nombre o contraseña no válidos')
            return apology("Nombre o contraseña no válidos", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    # else:
    #     return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    """Register user"""
    if request.method == "POST":
        nombre = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not nombre:
            flash(f'Falta ingresar el nombre de usuario')
            return apology("Falta ingresar el nombre de usuario")
        if not password:
            flash(f'Falta ingresar la contraseña')
            return apology("Falta ingresar la contraseña")
        if not confirm_password:
            flash(f'Falta confirmar la contraseña')
            return apology("Falta confirmar la contraseña")
        if password != confirm_password:
            flash(f'Las contraseñas no coinciden')
            return apology("Las contraseñas no coinciden")
        token = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username,hash) VALUES(?,?)", nombre, token)

            user_id = db.execute("SELECT id FROM users WHERE username = ?", nombre)
            flash(f'{nombre} ya estás registrado')

            session["user_id"] = user_id[0]['id']
            return redirect("/")
        except:
            flash(f'Nombre de usuario ya usado')
            return apology("")

    else:
        return render_template("register.html")


@login_required
@app.route('/contactus', methods=["GET","POST"])
def get_contact():
    form = ContactForm()
    # here, if the request type is a POST we get the data on contat
    #forms and save them else we return the contact forms html page
    try:
        user_id = session["user_id"]
    except:
        flash(f'Necesitás loguearte para contactarte con nosotros')
        return render_template("index.html")    
    if request.method == 'POST':

        name =  request.form["name"]
        if not name:
            flash(f'Falta ingresar tu nombre')
            return render_template('contactus.html', form=form)
            
        email = request.form["email"]
        if not email:
            flash(f'Falta ingresar tu e-mail')
            return render_template('contactus.html', form=form)
        valido = check(email) #chequeador de validez de email en helper.py
        if not valido:
            flash(f'No es una dirección de email válida')
            return render_template('contactus.html', form=form)
        
        subject = request.form["subject"]
        if not subject:
            flash(f'Falta ingresar el asunto')
            return render_template('contactus.html', form=form)
        message = request.form["message"]
        if not message:
            flash(f'Falta ingresar el mensaje')
            return render_template('contactus.html', form=form)


        # msg = Message("Hello", sender=["damiandrolas@gmail.com"],recipients=[email])
        # msg.body = "Gracias por enviar el email"
        # mail.send(msg)

        db.execute("INSERT INTO mensajes (nombre,email, asunto,mensaje) VALUES(?,?,?,?)", name, email, subject, message)

        # res = pd.DataFrame({'name':name, 'email':email, 'subject':subject ,'message':message}, index=[0])
        # res.to_csv('./contactusMessage.csv')
        flash(f'Tu mensaje ha sido enviado,te responderemos a la brevedad')
        return render_template("index.html")
 
    else:
        return render_template('contactus.html', form=form)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run(debug = True) 
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=port)

