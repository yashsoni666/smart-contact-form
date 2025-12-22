from flask import Flask, render_template, request
import pickle
import sqlite3

app = Flask(__name__, static_folder="static")

# Load ML model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def save_to_db(message, result):
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (message, result) VALUES (?, ?)",
        (message, result)
    )
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/history")
def history():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()
    cursor.execute("SELECT message, result, created_at FROM messages ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    return render_template("history.html", rows=rows)


@app.route("/submit", methods=["POST"])
def submit():
    message = request.form["message"]

    data = vectorizer.transform([message])
    prediction = model.predict(data)[0]

    # Save to database
    save_to_db(message, prediction)

    return render_template(
        "result.html",
        message=message,
        result=prediction
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

