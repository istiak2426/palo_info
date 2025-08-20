from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load CSV once at startup
CSV_FILE = "data.csv"   # change to your file name
df = pd.read_csv(CSV_FILE)

# Precompute a search-friendly text column (one-time cost at startup)
df["_search_blob"] = df.astype(str).agg(" ".join, axis=1).str.lower()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        term = request.form.get("search")
        if term:
            term = term.lower()
            # Fast search: check only the precomputed blob column
            mask = df["_search_blob"].str.contains(term, na=False, regex=False)
            results = df[mask].drop(columns="_search_blob").to_dict(orient="records")
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
