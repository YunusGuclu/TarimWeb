from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Function to fetch data from SQLite database
def fetch_soil_data():
    conn = sqlite3.connect('tarim_bilgileri.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Toprak_Bilgisi")
    rows = cursor.fetchall()
    conn.close()
    # Convert rows to a list of dictionaries
    data = [
        {"id": row[0], "Toprak_Turu": row[1], "Urunler": row[2], "Ozellikler": row[3]}
        for row in rows
    ]
    return data

# Endpoint to get soil data
@app.route('/get_soil_data', methods=['GET'])
def get_soil_data():
    data = fetch_soil_data()
    return jsonify(data)

# Endpoint to update soil data
@app.route('/update_soil_data', methods=['POST'])
def update_soil_data():
    data = request.get_json()
    soil_id = data.get('id')
    soil_type = data.get('Toprak_Turu')
    products = data.get('Urunler')
    properties = data.get('Ozellikler')

    try:
        conn = sqlite3.connect('tarim_bilgileri.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Toprak_Bilgisi
            SET Toprak_Turu = ?, Urunler = ?, Ozellikler = ?
            WHERE id = ?
        ''', (soil_type, products, properties, soil_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
