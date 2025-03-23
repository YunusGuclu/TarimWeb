import sqlite3
from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/get_soil_data')
def get_soil_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('dp.sqllite4.db')
    cursor = conn.cursor()
    
    # Fetch data from the Toprak_Bilgisi table
    cursor.execute('SELECT * FROM Toprak_Bilgisi')
    rows = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Convert the data into a list of dictionaries
    data = [
        {'id': row[0], 'Toprak_Turu': row[1], 'Urunler': row[2], 'Ozellikler': row[3]}
        for row in rows
    ]
    
    return jsonify(data)

@app.route('/tarimverileri')
def tarimverileri():
    return render_template('tarimverileri.html')

if __name__ == '__main__':
    app.run(debug=True)
