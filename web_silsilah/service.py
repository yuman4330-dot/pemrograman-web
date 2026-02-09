import os
from constants import DATA_FILE
from utils import bersihkan_nama

def cari_anggota(nama_input):
    if not os.path.exists(DATA_FILE): return []

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    individu, keluarga = {}, {}
    current_id, current_fam_id = "", ""

    # 1. Parsing Data Individu
    for line in lines:
        line = line.strip()
        if "@ INDI" in line:
            current_id = line.split("@")[1]
            individu[current_id] = {"nama": "", "gender": "-", "lahir": "Tidak diketahui", "famc": "", "fams": []}
        elif current_id:
            if line.startswith("1 NAME"):
                individu[current_id]["nama"] = bersihkan_nama(line)
            elif line.startswith("1 SEX"):
                individu[current_id]["gender"] = "Laki-laki" if "M" in line else "Perempuan"
            elif line.startswith("2 DATE"):
                individu[current_id]["lahir"] = line.replace("2 DATE", "").strip()
            elif line.startswith("1 FAMC"):
                individu[current_id]["famc"] = line.replace("1 FAMC", "").replace("@", "").strip()
            elif line.startswith("1 FAMS"):
                individu[current_id]["fams"].append(line.replace("1 FAMS", "").replace("@", "").strip())

    # 2. Parsing Data Keluarga
    for line in lines:
        line = line.strip()
        if "@ FAM" in line and "FAMC" not in line:
            current_fam_id = line.split("@")[1]
            keluarga[current_fam_id] = {"ayah": "", "ibu": "", "anak": []}
        elif current_fam_id:
            if line.startswith("1 HUSB"): keluarga[current_fam_id]["ayah"] = line.replace("1 HUSB", "").replace("@", "").strip()
            elif line.startswith("1 WIFE"): keluarga[current_fam_id]["ibu"] = line.replace("1 WIFE", "").replace("@", "").strip()
            elif line.startswith("1 CHIL"): keluarga[current_fam_id]["anak"].append(line.replace("1 CHIL", "").replace("@", "").strip())

    # 3. Filter Hasil Pencarian & Relasi
    hasil = []
    for id_ind, data in individu.items():
        if nama_input.lower() in data["nama"].lower() and nama_input != "":
            info = {
                "nama": data["nama"], "gender": data["gender"], "lahir": data["lahir"],
                "ayah": None, "ibu": None, "saudara": [], "anak": [], "urutan": ""
            }
            # Cari Orang Tua & Saudara
            f_id = data["famc"]
            if f_id in keluarga:
                fam = keluarga[f_id]
                info["ayah"] = individu.get(fam["ayah"], {}).get("nama")
                info["ibu"] = individu.get(fam["ibu"], {}).get("nama")
                info["saudara"] = [individu.get(s_id, {}).get("nama") for s_id in fam["anak"] if s_id != id_ind]
                if id_ind in fam["anak"]:
                    info["urutan"] = f"Anak ke-{fam['anak'].index(id_ind) + 1} dari {len(fam['anak'])} bersaudara"
            
            # Cari Anak
            for fs_id in data["fams"]:
                if fs_id in keluarga:
                    info["anak"].extend([individu.get(a_id, {}).get("nama") for a_id in keluarga[fs_id]["anak"]])
            
            hasil.append(info)
    return hasil