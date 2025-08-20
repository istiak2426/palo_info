from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load CSV once at startup
CSV_FILE = "data.csv"   # change to your file name
df = pd.read_csv(CSV_FILE)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        term = request.form.get("search")
        if term:
            term = term.lower()
            # Efficient vectorized search across all columns
            mask = pd.concat(
                [df[col].astype(str).str.lower().str.contains(term, na=False) for col in df.columns],
                axis=1
            ).any(axis=1)
            results = df[mask].to_dict(orient="records")
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)

