from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load CSV once at startup
CSV_FILE = os.path.join(os.path.dirname(__file__), "data.csv")
df = pd.read_csv(CSV_FILE)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        term = request.form.get("search", "").lower()
        if term:
            mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(term).any(), axis=1)
            results = df[mask].to_dict(orient="records")
    return render_template("index.html", results=results)

