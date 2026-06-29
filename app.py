from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Deepa#2006",   # Replace with your MySQL password
    database="medicine_db"
)

cursor = db.cursor()


# Dashboard Home Page
@app.route('/')
def home():

    # Low Stock Medicines
    cursor.execute(
        "SELECT medicine_name FROM medicines WHERE quantity < 10"
    )
    low_stock = cursor.fetchall()

    # Expired Medicines
    cursor.execute("""
        SELECT medicine_name
        FROM medicines
        WHERE expiry_date <= CURDATE()
    """)
    expired = cursor.fetchall()

    return render_template(
        'dashboard.html',
        low_stock=low_stock,
        expired=expired
    )


# Add Medicine
@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':

        name = request.form['name']
        quantity = request.form['quantity']
        expiry = request.form['expiry']
        company = request.form['company']

        sql = """
        INSERT INTO medicines
        (medicine_name, quantity, expiry_date, manufacturer)
        VALUES (%s, %s, %s, %s)
        """

        values = (name, quantity, expiry, company)

        cursor.execute(sql, values)
        db.commit()

        return "Medicine Added Successfully"

    return render_template('add_medicine.html')


# View Medicines
@app.route('/view')
def view():

    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()

    return render_template(
        'view_medicines.html',
        medicines=medicines
    )


# Update Medicine
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    if request.method == 'POST':

        name = request.form['name']
        quantity = request.form['quantity']
        expiry = request.form['expiry']
        company = request.form['company']

        cursor.execute("""
            UPDATE medicines
            SET medicine_name=%s,
                quantity=%s,
                expiry_date=%s,
                manufacturer=%s
            WHERE id=%s
        """, (name, quantity, expiry, company, id))

        db.commit()

        return "Medicine Updated Successfully"

    cursor.execute(
        "SELECT * FROM medicines WHERE id=%s",
        (id,)
    )

    medicine = cursor.fetchone()

    return render_template(
        'update_medicine.html',
        medicine=medicine
    )


# Delete Medicine
@app.route('/delete/<int:id>')
def delete(id):

    cursor.execute(
        "DELETE FROM medicines WHERE id=%s",
        (id,)
    )

    db.commit()

    return "Medicine Deleted Successfully"


# Low Stock Page
@app.route('/lowstock')
def lowstock():

    cursor.execute(
        "SELECT * FROM medicines WHERE quantity < 10"
    )

    medicines = cursor.fetchall()

    return render_template(
        'view_medicines.html',
        medicines=medicines
    )


# Expiry Page
@app.route('/expiry')
def expiry():

    cursor.execute("""
        SELECT * FROM medicines
        WHERE expiry_date <= CURDATE()
    """)

    medicines = cursor.fetchall()

    return render_template(
        'view_medicines.html',
        medicines=medicines
    )


if __name__ == '__main__':
    app.run(debug=True)