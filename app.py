from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load CSV once at startup
CSV_FILE = "data.csv"
df = pd.read_csv(CSV_FILE)

# Precompute a combined lowercase column for searching
df["_search"] = df.astype(str).apply(lambda row: " ".join(row.values).lower(), axis=1)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        term = request.form.get("search", "").lower()
        if term:
            # Search only in the precomputed "_search" column
            mask = df["_search"].str.contains(term, na=False)
            results = df[mask].drop(columns="_search").to_dict(orient="records")
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
