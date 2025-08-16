from flask import Flask, request, send_file, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# HTML template (upload form)
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Salary Calculator</title>
</head>
<body style="font-family: Arial; margin: 50px;">
    <h2>Upload Excel File (with columns: name, salary, leaves)</h2>
    <form action="/process" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".xlsx,.xls" required>
        <br><br>
        <button type="submit">Upload & Process</button>
    </form>
</body>
</html>
"""

def calculate_monthly_salary(salary, leaves):
    if leaves == "-":
        return 0
    try:
        leaves = int(leaves)
    except:
        return 0

    if leaves <= 10:
        return (salary / 30) * (30 - leaves + 4)
    else:
        return (salary / 30) * (30 - leaves)

@app.route("/")
def index():
    return render_template_string(html)

@app.route("/process", methods=["POST"])
def process():
    file = request.files["file"]
    if not file:
        return "No file uploaded!"

    # Read Excel
    df = pd.read_excel(file)

    # Apply logic
    df["Monthly_Salary"] = df.apply(lambda row: calculate_monthly_salary(row["salary"], row["leaves"]), axis=1)

    # Save output
    output_path = "output.xlsx"
    df.to_excel(output_path, index=False)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
