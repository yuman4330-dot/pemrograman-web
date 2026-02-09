from flask import Flask, render_template, request, redirect, url_for
from service import cari_anggota
from constants import ADMIN_USER, ADMIN_PASS, FLASK_PORT, DEBUG_MODE

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['user'] == ADMIN_USER and request.form['pass'] == ADMIN_PASS:
            return redirect(url_for('search'))
    return render_template('login.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    keyword = request.form.get('nama', '') if request.method == 'POST' else ''
    hasil_pencarian = cari_anggota(keyword)
    return render_template('search.html', hasil=hasil_pencarian, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE, port=FLASK_PORT)