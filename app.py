from flask import Flask, render_template, request

app = Flask(__name__)

# Home route
@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        name = request.form.get("name")
        message = f"Hello {name}, welcome to your sample app 🚀"

    return render_template("index.html", message=message)


# API route
@app.route("/api")
def api():
    return {"status": "success", "message": "API is working!"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
