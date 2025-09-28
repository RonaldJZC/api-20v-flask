from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# crear una conexión a la base de datos
def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row #nos permite acceder a las columnas por nombre
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

# crear una ruta para la página de listado de posts
@app.route("/posts", methods=["GET"]) # requiere GET, que es la método de solicitud
def posts():
    c = get_db_connection()
    posts=(c.execute("SELECT * FROM posts").fetchall())
    c.close()
    return render_template("post/post_list.html", posts_list=posts)

# crear una ruta para la página de creación de posts
@app.route("/posts/create", methods=["GET", "POST"]) # requiere GET, que es la método de solicitud
def create_post():
    if request.method == "GET":
        return render_template("post/create.html")
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        return redirect(url_for("posts"))
    
# ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)