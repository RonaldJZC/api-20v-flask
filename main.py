from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET"]) # requiere GET, que es la método de solicitud
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/home", methods=["GET"])
def home():
    numero_1 = "uno"
    return render_template("index.html", numero_1=numero_1)

if __name__ == "__main__":
    app.run(debug=True)