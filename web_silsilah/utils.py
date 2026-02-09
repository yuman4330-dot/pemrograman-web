def bersihkan_nama(nama_raw):
    if not nama_raw:
        return ""
    
    # Menghapus tag awal GEDCOM dan tanda garis miring /
    nama = nama_raw.replace("1 NAME", "").replace("/", "")
    
    # Mengganti koma menjadi spasi (Menghilangkan ", budi" atau "siti, aminah")
    nama = nama.replace(",", " ")
    
    # Menghapus spasi berlebih di tengah dan di ujung
    return " ".join(nama.split()).strip()