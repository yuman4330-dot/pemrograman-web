from utils import konversi_nilai_ke_label, konversi_label_ke_bobot


def buat_data_nilai(list_sks, list_nilai_angka):
    hasil = []

    for i in range(len(list_nilai_angka)):
        nilai_angka = list_nilai_angka[i]
        sks_matkul = list_sks[i]

        label_nilai = konversi_nilai_ke_label(nilai_angka)
        bobot_nilai = konversi_label_ke_bobot(label_nilai)

        hasil.append({
            "sks": sks_matkul,
            "nilai": nilai_angka,
            "label": label_nilai,
            "bobot": bobot_nilai
        })

    return hasil


def hitung_ips(list_sks, list_nilai_angka):
    total_bobot_sks = 0
    total_sks = sum(list_sks)

    for i in range(len(list_nilai_angka)):
        label = konversi_nilai_ke_label(list_nilai_angka[i])
        bobot = konversi_label_ke_bobot(label)
        total_bobot_sks += bobot * list_sks[i]

    if total_sks == 0:
        return 0

    return round(total_bobot_sks / total_sks, 2)
