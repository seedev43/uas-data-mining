from flask import Flask, render_template, request
from datetime import datetime
import pickle
import pytz
import numpy as np

current_time = datetime.now()
# Mendefinisikan zona waktu awal (misalnya UTC)
original_timezone = pytz.UTC

# Mendefinisikan zona waktu baru 
new_timezone = pytz.timezone('Asia/Jakarta')


# load file pickle nya
pickleFileOne = './models/kelulusan.pkl'
pickleFileTwo = './models/potability.pkl'

with open(pickleFileOne, 'rb') as file:
    modelLogistic = pickle.load(file)
    print(f"File {pickleFileOne} loaded!")

with open(pickleFileTwo, 'rb') as file:
    modelRandomForest = pickle.load(file)
    print(f"File {pickleFileTwo} loaded!")

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    # Mengonversi waktu ke zona waktu baru
    originalTimezone = original_timezone.localize(current_time)
    timeNow = originalTimezone.astimezone(new_timezone)
    datas = {
        # Mendapatkan alamat IP pengguna
        'user_ip' : request.headers.get('X-Forwarded-For', request.remote_addr),
        'date': current_time.strftime('%d-%m-%Y'),
        'time': current_time.strftime('%H:%M:%s')
    }
    return render_template('index.html', data=datas)

@app.route("/kelulusan-mahasiswa", methods=['GET', 'POST'])
def kelulusanMhs():
    if request.method == "GET":
        return render_template('kelulusan_mhs.html')
    int_fields = ['gender', 'age', 'student_status', 'married_status']  # Contoh nama field yang tetap int

    # Fungsi untuk mengonversi nilai form input
    def convert_value(name, value):
        try:
            if name in int_fields:
                return int(value)
            else:
                return float(value)
        except ValueError:
            return None  # atau nilai default yang diinginkan jika konversi gagal

    # Mengambil nilai-nilai dari form
    values = {name: convert_value(name, value) for name, value in request.form.items()}
    
    # Filter out None values if conversion fails
    values = {name: value for name, value in values.items() if value is not None}

    # Masukkan nilai-nilai ke dalam array
    array_values = [list(values.values())]
    print(array_values)
    prediction = modelLogistic.predict(array_values)
    datas = {
        'inputs': array_values,
        'predict' : prediction[0]
    }
    return render_template('kelulusan_mhs.html', data=datas)

@app.route("/water-potability", methods=['GET', 'POST'])
def waterPotability():
    if request.method == "GET":
        return render_template('water_potability.html')
    # mengambil semua value dari form input html
    values = [float(x) for x in request.form.values()]
    # masukkan value tadi ke array
    array_values = [values]
    # print(array_values[0])
    prediction = modelRandomForest.predict(array_values)
    datas = {
        'inputs': array_values,
        'predict' : prediction[0]
    }
    return render_template('water_potability.html', data=datas)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run(debug=True) 
    

