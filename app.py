from flask import Flask, render_template, jsonify
import pandas as pd
from collections import defaultdict

app = Flask(__name__)

def parse_git_log(filepath="log.txt"):
    with open(filepath, "r") as f:
        lines = f.readlines()

    daily_data = defaultdict(lambda: {"added": 0, "deleted": 0})
    current_date = None

    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line.count('-') == 2 and len(line) == 10:
            current_date = line
        elif current_date and "\t" in line:
            parts = line.split("\t")
            if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                daily_data[current_date]["added"] += int(parts[0])
                daily_data[current_date]["deleted"] += int(parts[1])

    df = pd.DataFrame.from_dict(daily_data, orient="index").sort_index()
    df.index.name = "date"
    return df.reset_index().to_dict(orient="records")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    return jsonify(parse_git_log())

if __name__ == "__main__":
    app.run(debug=True)
