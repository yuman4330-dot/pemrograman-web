from flask import Flask, render_template, request, redirect, session
from service import buat_data_nilai, hitung_ips

app = Flask(__name__)
app.secret_key = "rahasia"

@app.route("/")
def index():
    return render_template("beranda.html")


@app.route("/biodata", methods=["GET", "POST"])
def biodata():
    if request.method == "POST":
        session["biodata"] = {
            "nama_mahasiswa": request.form["nama"],
            "nim_mahasiswa": request.form["nim"]
        }
        return redirect("/biodata")

    return render_template("biodata.html", biodata=session.get("biodata"))


@app.route("/sks", methods=["GET", "POST"])
def sks():
    if "total_matkul" not in session:
        if request.method == "POST":
            session["total_matkul"] = int(request.form["jumlah"])
            session["list_sks"] = []
            session["index_sks"] = 0
            return redirect("/sks")
        return render_template("sks.html", tahap="jumlah")

    if request.method == "POST":
        session["list_sks"].append(int(request.form["sks"]))
        session["index_sks"] += 1

        if session["index_sks"] >= session["total_matkul"]:
            session.pop("total_matkul")
            session.pop("index_sks")
            return redirect("/")

        return redirect("/sks")

    return render_template(
        "sks.html",
        tahap="input",
        index=session["index_sks"] + 1
    )


@app.route("/nilai", methods=["GET", "POST"])
def nilai():
    if "total_nilai" not in session:
        if request.method == "POST":
            session["total_nilai"] = int(request.form["jumlah"])
            session["list_nilai"] = []
            session["index_nilai"] = 0
            return redirect("/nilai")
        return render_template("nilai.html", tahap="jumlah")

    if request.method == "POST":
        session["list_nilai"].append(float(request.form["nilai"]))
        session["index_nilai"] += 1

        if session["index_nilai"] >= session["total_nilai"]:
            session.pop("total_nilai")
            session.pop("index_nilai")
            return redirect("/")

        return redirect("/nilai")

    return render_template(
        "nilai.html",
        tahap="input",
        index=session["index_nilai"] + 1
    )


@app.route("/lihat-nilai")
def lihat_nilai():
    list_sks = session.get("list_sks")
    list_nilai = session.get("list_nilai")

    if not list_sks or not list_nilai or len(list_sks) != len(list_nilai):
        return render_template("lihat_nilai.html", data=[])

    data = buat_data_nilai(list_sks, list_nilai)
    return render_template("lihat_nilai.html", data=data)


@app.route("/lihat-ip")
def lihat_ip():
    list_sks = session.get("list_sks")
    list_nilai = session.get("list_nilai")

    if not list_sks or not list_nilai or len(list_sks) != len(list_nilai):
        return render_template("lihat_ip.html", ips=None)

    ips = hitung_ips(list_sks, list_nilai)
    return render_template("lihat_ip.html", ips=ips)


if __name__ == "__main__":
    app.run(debug=True)
