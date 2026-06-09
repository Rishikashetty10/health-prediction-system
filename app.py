from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        full_name = request.form["full_name"]
        dob = request.form["dob"]
        email = request.form["email"]
        glucose = request.form["glucose"]
        haemoglobin = request.form["haemoglobin"]
        cholesterol = request.form["cholesterol"]

        remarks = "Healthy"

        if glucose and float(glucose) > 140:
            remarks = "High Diabetes Risk"

        if cholesterol and float(cholesterol) > 200:
            remarks = "High Heart Disease Risk"

        conn = sqlite3.connect("database/patients.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO patients
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        ))

        conn.commit()
        conn.close()

    conn = sqlite3.connect("database/patients.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    return render_template("index.html", patients=patients)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_patient(id):

    conn = sqlite3.connect("database/patients.db")
    cursor = conn.cursor()

    if request.method == "POST":

        full_name = request.form["full_name"]
        dob = request.form["dob"]
        email = request.form["email"]
        glucose = request.form["glucose"]
        haemoglobin = request.form["haemoglobin"]
        cholesterol = request.form["cholesterol"]

        remarks = "Healthy"

        if glucose and float(glucose) > 140:
            remarks = "High Diabetes Risk"

        if cholesterol and float(cholesterol) > 200:
            remarks = "High Heart Disease Risk"

        cursor.execute("""
        UPDATE patients
        SET full_name=?,
            dob=?,
            email=?,
            glucose=?,
            haemoglobin=?,
            cholesterol=?,
            remarks=?
        WHERE id=?
        """, (
            full_name,
            dob,
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks,
            id
        ))

        conn.commit()
        conn.close()

        return redirect("/")

    cursor.execute("SELECT * FROM patients WHERE id=?", (id,))
    patient = cursor.fetchone()

    conn.close()

    return render_template("edit_patient.html", patient=patient)


@app.route("/delete/<int:id>")
def delete_patient(id):

    conn = sqlite3.connect("database/patients.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)