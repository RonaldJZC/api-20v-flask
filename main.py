from flask import Flask, render_template
import sqlite3

# crear una conexión a la base de datos
def get_db_connection():
    connection = sqlite3.connect("database.db")
    return connection

# crear una función para insertar datos en la base de datos
app = Flask(__name__)

# crear una ruta para la página de inicio
@app.route("/", methods=["GET"]) # requiere GET, que es la método de solicitud
def index():
    name_page = "blog"
    return render_template("index.html", name_page=name_page)

# crear una ruta para la página de home
@app.route("/home", methods=["GET"])
def home():
    name_page = "home"
    return render_template("home.html", name_page=name_page)

# crear una ruta para la página de contacto
@app.route("/about", methods=["GET"]) # requiere GET, que es la método de solicitud
def about():
    name_page = "about"
    return render_template("about.html", name_page=name_page)

# ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)