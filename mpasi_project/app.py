from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfigurasi database (menggunakan SQLite di sini)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mpasi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model untuk menyimpan data anak
class Anak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    umur = db.Column(db.Integer, nullable=False)
    berat_badan = db.Column(db.Float, nullable=False)
    tanggal_input = db.Column(db.DateTime, default=db.func.now())

    def rekomendasi_mpasi(self):
        if self.umur < 6:
            return "ASI eksklusif"
        elif 6 <= self.umur < 12:
            if self.berat_badan < 7:
                return "MPASI lembut, seperti bubur"
            else:
                return "MPASI semi padat, seperti nasi tim"
        elif 12 <= self.umur < 24:
            return "MPASI padat, makanan keluarga yang dicincang"
        else:
            return "MPASI lanjutan, sesuai dengan makanan keluarga"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nama = request.form['nama']
        umur = int(request.form['umur'])
        berat_badan = float(request.form['berat_badan'])

        anak = Anak(nama=nama, umur=umur, berat_badan=berat_badan)
        db.session.add(anak)
        db.session.commit()

        rekomendasi = anak.rekomendasi_mpasi()
        return render_template('result.html', rekomendasi=rekomendasi, anak=anak)
    return render_template('index.html')

@app.route('/daftar')
def daftar_anak():
    anak_list = Anak.query.all()
    return render_template('daftar_anak.html', anak_list=anak_list)

if __name__ == "__main__":
    db.create_all()  # Membuat tabel di database
    app.run(debug=True)
