from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-123"  # solo dev

# crear una conexión a la base de datos
def get_db_connection():
    connection = sqlite3.connect("database.db")
    connection.row_factory = sqlite3.Row #nos permite acceder a las columnas por nombre
    return connection

# crear una ruta para la página de inicio
@app.route("/", methods=["GET"])
def index():
    name_page = "blog"

    # últimos posts (si no hay, simplemente no se muestran)
    conn = get_db_connection()
    posts_recent = conn.execute(
        "SELECT id, title, substr(content, 1, 120) AS excerpt FROM posts ORDER BY id DESC LIMIT 3"
    ).fetchall()
    conn.close()

    return render_template("index.html", name_page=name_page, posts_recent=posts_recent)

# crear una ruta para la página de contacto
@app.route("/about", methods=["GET"])
def about():
    name_page = "about"
    conn = get_db_connection()
    posts_count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    conn.close()
    return render_template("about.html",
                           name_page=name_page,
                           posts_count=posts_count,
                           author="Ronald Zarpan Casas")  

# crear una ruta para la página de listado de posts
@app.route("/posts", methods=["GET"]) # requiere GET, que es la método de solicitud
def posts():
    c = get_db_connection()
    posts=(c.execute("SELECT * FROM posts").fetchall())
    c.close()
    return render_template("post/post_list.html", posts_list=posts)

# crear una ruta para la página de detalle de un post
@app.route("/posts/<int:post_id>", methods=["GET"])
def post_detail(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if post is None:
        return "Post not found", 404
    return render_template("post/post_detail.html", post=post)

# crear una ruta para la página de creación de posts
@app.route("/posts/create", methods=["GET", "POST"])
def create_post():
    if request.method == "GET":
        return render_template("post/create.html")

    # POST
    title = (request.form.get("title") or "").strip()
    content = (request.form.get("content") or "").strip()

    # Validaciones simples
    errors = []
    if not title:
        errors.append("El título es obligatorio.")
    elif len(title) > 120:
        errors.append("El título no puede exceder 120 caracteres.")

    if not content:
        errors.append("El contenido es obligatorio.")
    elif len(content) < 5:
        errors.append("El contenido debe tener al menos 5 caracteres.")

    if errors:
        for e in errors:
            flash(e, "danger")
        # Volvemos a renderizar manteniendo lo escrito
        return render_template("post/create.html"), 400

    # Inserción segura
    try:
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO posts (title, content) VALUES (?, ?)",
            (title, content),
        )
        conn.commit()
        conn.close()
        flash("¡Post creado con éxito! 🎉", "success")
        return redirect(url_for("posts"))
    except Exception as exc:
        # Log opcional en consola
        print("DB error:", exc)
        flash("Ocurrió un error creando el post. Intenta nuevamente.", "danger")
        return render_template("post/create.html"), 500

# crear una ruta para la página de edición de un post
@app.route("/posts/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if post is None:
        flash("Post no encontrado.", "warning")
        return redirect(url_for("posts"))

    if request.method == "GET":
        return render_template("post/update.html", post=post)

    # POST
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if len(title) < 3 or len(content) < 3:
        flash("Por favor completa título y contenido (mín. 3 caracteres).", "danger")
        return render_template("post/update.html", post={"id": post_id, "title": title, "content": content})

    try:
        conn = get_db_connection()
        conn.execute(
            "UPDATE posts SET title = ?, content = ? WHERE id = ?",
            (title, content, post_id),
        )
        conn.commit()
        conn.close()
        flash("¡Post actualizado con éxito!", "success")
        return redirect(url_for("post_detail", post_id=post_id))
    except Exception as exc:
        print("DB error:", exc)
        flash("Ocurrió un error actualizando el post. Intenta nuevamente.", "danger")
        return render_template("post/update.html", post={"id": post_id, "title": title, "content": content}), 500


@app.route("/posts/delete/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    conn.close()
    if post is None:
        return "Post not found", 404
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return ""

# ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
    

