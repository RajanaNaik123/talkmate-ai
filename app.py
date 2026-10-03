
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/practice")
def practice():
    return render_template("practice.html")


@app.route("/chat")
def chat():
    scenario = request.args.get(
        "scenario", "Everyday Conversation"
    )
    return render_template("chat.html", scenario=scenario)


if __name__ == "__main__":
    app.run(debug=True)