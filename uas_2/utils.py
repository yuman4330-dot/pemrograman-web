def konversi_nilai_ke_label(nilai_angka):
    if 85 <= nilai_angka <= 100:
        return "A"
    elif 80 <= nilai_angka <= 84:
        return "A-"
    elif 75 <= nilai_angka <= 79:
        return "B+"
    elif 70 <= nilai_angka <= 74:
        return "B"
    elif 65 <= nilai_angka <= 69:
        return "B-"
    elif 60 <= nilai_angka <= 64:
        return "C+"
    elif 55 <= nilai_angka <= 59:
        return "C"
    elif 45 <= nilai_angka <= 54:
        return "D"
    else:
        return "E"


def konversi_label_ke_bobot(label_nilai):
    bobot = {
        "A": 4.00,
        "A-": 3.75,
        "B+": 3.50,
        "B": 3.00,
        "B-": 2.75,
        "C+": 2.50,
        "C": 2.00,
        "D": 1.00,
        "E": 0.00
    }
    return bobot.get(label_nilai.upper(), 0.0)
