import os
import datetime
import pandas as pd

# ==========================================

file_admin = "admin_rs.csv"
file_akun = "akun_pasien.csv"
file_kamar = "kamar_rs.csv"
file_rujukan = "surat_rujukan.csv"
file_riwayat_rujukan = "riwayat_rujukan.csv"
file_riwayat_rawat = "riwayat_rawat_inap.csv"

usn_admin = "admin"
pw_admin = "sehat123"

rekening_rs = "1234567890"
nama_rs = "Rumah Sehat"

input_admin = ["username", "password"]
input_pasien = ["username", "password", "nama lengkap", "nik", "no rekening"]
data_kamar = ["nomor kamar", "tipe kamar", "tarif per hari", "fasilitas", "status", "pasien",
              "tgl masuk", "tgl keluar"]

surat_rujuk = ["nomor rujukan", "nama pasien", "nik", "asal rujukan", "status rujukan"]
riwayat_rujuk = ["tanggal", "nomor rujukan", "nama pasien", "nik", "asal rujukan", "status rujukan"]
riwayat_rawat = ["tanggal proses", "jenis transaksi", "nomor kamar", "tipe kamar", "pasien",
                 "tgl masuk", "tgl keluar", "hari terpakai", "total tagihan", "dana kembali",
                 "no rekening pasien"]

list_tipe_kamar = ["VIP", "Kelas 1", "Kelas 2", "Kelas 3"]
status_rujukan = ["Aktif", "Terpakai", "Tidak Aktif"]


# ==========================================
# HEADER RUMAH SAKIT
# ==========================================

def tampilkan_header():
    print("=" * 60)
    print("|" + " " * 58 + "|")
    print("|" + "[+] INI RUMAH SEHAT BUKAN RUMAH SAKIT [+]".center(58) + "|")
    print("|" + "Melayani dengan Seniat Mungkin".center(58) + "|")
    print("|" + " " * 58 + "|")
    print("-" * 60)
    print("|" + "Jl. Rawon Seto Jos Jis No. Horeg".center(58) + "|")
    print("|" + "IGD 24 Detik: (0) 123-4567".center(58) + "|")
    print("=" * 60)


# ==========================================
# FUNGSI BANTU DATA & TABEL DINAMIS
# ==========================================

def ambil_nilai_sel(df, baris, kolom, default=""):
    if kolom not in df.columns:
        return default
    nilai = df.loc[baris, kolom]
    if bool(pd.isna(nilai)) or str(nilai).strip() == "" or str(nilai).strip().lower() == "nan":
        return default
    return str(nilai).strip()


def buat_baris_tabel(isi_baris, lebar_kolom):
    baris_teks = "|"
    for i in range(len(isi_baris)):
        teks = str(isi_baris[i])
        spasi = lebar_kolom[i] - len(teks)
        if spasi < 0:
            spasi = 0
        baris_teks += " " + teks + (" " * spasi) + " |"
    return baris_teks


def tabel(judul_kolom, daftar_baris):
    lebar_kolom = []
    for i in range(len(judul_kolom)):
        terpanjang = len(str(judul_kolom[i]))
        for baris in daftar_baris:
            panjang_sel = len(str(baris[i]))
            if panjang_sel > terpanjang:
                terpanjang = panjang_sel
        lebar_kolom.append(terpanjang)

    garis = "+"
    for lebar in lebar_kolom:
        garis += "-" * (lebar + 2) + "+"

    print(garis)
    print(buat_baris_tabel(judul_kolom, lebar_kolom))
    print(garis)
    for baris in daftar_baris:
        print(buat_baris_tabel(baris, lebar_kolom))
    print(garis)


# ==========================================
# SIAPKAN FILE CSV AWAL
# ==========================================

def siapkan_file_data():
    if not os.path.exists(file_admin):
        df_admin = pd.DataFrame(columns=pd.Index(input_admin))
        df_admin.loc[0, "username"] = usn_admin
        df_admin.loc[0, "password"] = pw_admin
        df_admin.to_csv(file_admin, index=False)
    if not os.path.exists(file_akun):
        pd.DataFrame(columns=pd.Index(input_pasien)).to_csv(file_akun, index=False)
    if not os.path.exists(file_kamar):
        pd.DataFrame(columns=pd.Index(data_kamar)).to_csv(file_kamar, index=False)
    if not os.path.exists(file_rujukan):
        pd.DataFrame(columns=pd.Index(surat_rujuk)).to_csv(file_rujukan, index=False)
    if not os.path.exists(file_riwayat_rujukan):
        pd.DataFrame(columns=pd.Index(riwayat_rujuk)).to_csv(file_riwayat_rujukan, index=False)
    if not os.path.exists(file_riwayat_rawat):
        pd.DataFrame(columns=pd.Index(riwayat_rawat)).to_csv(file_riwayat_rawat, index=False)


# ==========================================
# LOGIN DAN REGISTRASI
# ==========================================

def registrasi_pasien():
    os.system("cls")
    tampilkan_header()
    print("\n    --- REGISTRASI PASIEN BARU ---")

    nama = input("    Masukkan Nama Lengkap : ").strip()
    nik = input("    Masukkan NIK (16 digit): ").strip()
    no_rekening = input("    Masukkan No Rekening  : ").strip()
    username = input("    Buat Username         : ").strip().lower()
    password = input("    Buat Password         : ").strip()
    konfirmasi = input("    Konfirmasi Password   : ").strip()

    if nama == "" or nik == "" or no_rekening == "" or username == "" or password == "":
        print("\n    [!] Semua kolom wajib diisi!")
        input("\n    Tekan Enter untuk kembali...")
        return

    if not nama.replace(" ", "").isalpha():
        print("\n    [!] Nama lengkap harus berupa huruf (boleh spasi)!")
        input("\n    Tekan Enter untuk kembali...")
        return

    if not nik.isdigit() or len(nik) != 16:
        print("\n    [!] NIK harus berupa angka tepat 16 digit!")
        input("\n    Tekan Enter untuk kembali...")
        return

    if not username.isalpha():
        print("\n    [!] Username harus berupa huruf tanpa spasi!")
        input("\n    Tekan Enter untuk kembali...")
        return

    if not no_rekening.isdigit() or len(no_rekening) < 10 or len(no_rekening) > 15:
        print("\n    [!] Nomor rekening harus berupa angka (10-15 karakter)!")
        input("\n    Tekan Enter untuk kembali...")
        return

    if password != konfirmasi:
        print("\n    [!] Konfirmasi password tidak cocok!")
        input("\n    Tekan Enter untuk kembali...")
        return

    try:
        df_admin = pd.read_csv(file_admin, dtype=str, keep_default_na=False)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df_admin = pd.DataFrame([{"username": usn_admin, "password": pw_admin}])
        df_admin.to_csv(file_admin, index=False)

    try:
        df_akun = pd.read_csv(file_akun, dtype=str, keep_default_na=False)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df_akun = pd.DataFrame(columns=input_pasien)

    df_admin.columns = df_admin.columns.str.strip().str.replace("\ufeff", "", regex=False)
    df_akun.columns = df_akun.columns.str.strip().str.replace("\ufeff", "", regex=False)

    for kolom in input_pasien:
        if kolom not in df_akun.columns:
            df_akun[kolom] = ""

    sudah_ada = False
    nik_ada = False
    for i in range(len(df_admin)):
        usn_adm = ambil_nilai_sel(df_admin, i, "username", "")
        if usn_adm.lower() == username:
            sudah_ada = True

    for i in range(len(df_akun)):
        usn_ak = ambil_nilai_sel(df_akun, i, "username", "")
        nik_ak = ambil_nilai_sel(df_akun, i, "nik", "")
        if usn_ak.lower() == username:
            sudah_ada = True
        if nik_ak == nik:
            nik_ada = True

    if sudah_ada:
        print(f"\n    [!] Username '{username}' sudah dipakai. Pilih yang lain.")
    elif nik_ada:
        print(f"\n    [!] NIK '{nik}' sudah terdaftar pada akun lain.")
    else:
        data_baru = pd.DataFrame([{
            "username": username,
            "password": password,
            "nama lengkap": nama,
            "nik": nik,
            "no rekening": no_rekening
        }])
        if len(df_akun) == 0:
            df_akun = data_baru[input_pasien]
        else:
            df_akun = pd.concat([df_akun, data_baru], ignore_index=True)
        df_akun.to_csv(file_akun, index=False)
        print("\n    [OK] Registrasi berhasil! Silakan login.")

    input("\n    Tekan Enter untuk kembali...")


def login():
    os.system("cls")
    tampilkan_header()
    print("\n    --- LOGIN SISTEM RUMAH SAKIT ---")

    username = input("    Username : ").strip().lower()
    password = input("    Password : ").strip()

    df_admin = pd.read_csv(file_admin, dtype=str)
    for i in range(len(df_admin)):
        usn_adm = ambil_nilai_sel(df_admin, i, "username", "").lower()
        pw_adm = ambil_nilai_sel(df_admin, i, "password", "")
        if usn_adm == username and pw_adm == password:
            print(f"\n    [OK] Login Admin berhasil! Selamat datang, {username}.")
            input("\n    Tekan Enter untuk lanjut...")
            menu_admin(username)
            return

    df_akun = pd.read_csv(file_akun, dtype=str)
    for i in range(len(df_akun)):
        usn_ak = ambil_nilai_sel(df_akun, i, "username", "").lower()
        pw_ak = ambil_nilai_sel(df_akun, i, "password", "")
        nama_ak = ambil_nilai_sel(df_akun, i, "nama lengkap", "")
        if usn_ak == username and pw_ak == password:
            print(f"\n    [OK] Login berhasil! Selamat datang, {nama_ak}.")
            input("\n    Tekan Enter untuk lanjut...")
            menu_pasien(nama_ak)
            return

    print("\n    [!] Username atau password salah!")
    input("\n    Tekan Enter untuk kembali...")


# ==========================================
# FITUR ADMIN - KELOLA DATA KAMAR
# ==========================================

def cetak_tabel_kamar(df_kamar, daftar_indeks=None):
    judul = ["No Kamar", "Tipe Kamar", "Tarif/Hari", "Fasilitas", "Status", "Pasien"]
    daftar_baris = []

    if daftar_indeks is None:
        daftar_indeks = list(range(len(df_kamar)))

    for i in daftar_indeks:
        no_k = ambil_nilai_sel(df_kamar, i, "nomor kamar", "-")
        tipe_k = ambil_nilai_sel(df_kamar, i, "tipe kamar", "-")
        tarif_str = ambil_nilai_sel(df_kamar, i, "tarif per hari", "0")
        tarif_angka = int(tarif_str) if tarif_str.isdigit() else 0
        tarif_teks = f"Rp {tarif_angka:,}".replace(",", ".")
        fas = ambil_nilai_sel(df_kamar, i, "fasilitas", "-")
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        psn = ambil_nilai_sel(df_kamar, i, "pasien", "-")
        daftar_baris.append([no_k, tipe_k, tarif_teks, fas, st, psn])

    tabel(judul, daftar_baris)


def lihat_data_kamar():
    os.system("cls")
    tampilkan_header()
    print("\n    --- DATA KAMAR RAWAT INAP ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    if len(df_kamar) == 0:
        print("    [!] Belum ada data kamar yang tersimpan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    cetak_tabel_kamar(df_kamar)

    tersedia = 0
    dipesan = 0
    terisi = 0
    for i in range(len(df_kamar)):
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        if st == "Tersedia":
            tersedia += 1
        elif st == "Dipesan":
            dipesan += 1
        elif st == "Terisi":
            terisi += 1

    print(f"Total kamar: {len(df_kamar)} | Tersedia: {tersedia} | Dipesan: {dipesan} | Terisi: {terisi}")
    input("\n    Tekan Enter untuk kembali...")


def tambah_data_kamar():
    os.system("cls")
    tampilkan_header()
    print("\n    --- TAMBAH DATA KAMAR RAWAT INAP ---")
    print("    (Ketik 0 pada Nomor Kamar untuk batal)\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)

    while True:
        nomor = input("    Nomor Kamar            : ").strip().upper()
        if nomor == "0":
            return
        if nomor == "":
            print("    [!] Nomor kamar tidak boleh kosong.")
            continue

        duplikat = False
        for i in range(len(df_kamar)):
            if ambil_nilai_sel(df_kamar, i, "nomor kamar", "").upper() == nomor:
                duplikat = True
        if duplikat:
            print(f"    [!] Kamar '{nomor}' sudah terdaftar.")
        else:
            break

    print("    Pilih Tipe Kamar:")
    for i in range(len(list_tipe_kamar)):
        print(f"      [{i + 1}] {list_tipe_kamar[i]}")
    while True:
        pilih_tipe = input("    Pilih (1-4)            : ").strip()
        if pilih_tipe.isdigit() and 1 <= int(pilih_tipe) <= len(list_tipe_kamar):
            tipe_kamar = list_tipe_kamar[int(pilih_tipe) - 1]
            break
        print("    [!] Masukkan angka 1-4.")

    while True:
        tarif_teks = input("    Tarif per Hari (Rp)    : ").strip().lower().replace("rp", "").replace(".", "").replace(",", "")
        if tarif_teks.isdigit() and int(tarif_teks) > 0:
            tarif = int(tarif_teks)
            break
        print("    [!] Tarif harus berupa angka lebih dari 0.")

    while True:
        fasilitas = input("    Fasilitas (pisah koma) : ").strip()
        if fasilitas != "":
            break
        print("    [!] Fasilitas wajib diisi.")

    print("\n    --- Ringkasan Data Kamar ---")
    print(f"    Nomor Kamar : {nomor}")
    print(f"    Tipe Kamar  : {tipe_kamar}")
    print(f"    Tarif/Hari  : Rp {tarif:,}".replace(",", "."))
    print(f"    Fasilitas   : {fasilitas}")
    print("    Status      : Tersedia")

    yakin = input("\n    Simpan data kamar ini? (y/n): ").strip().lower()
    if yakin != "y":
        print("\n    [!] Penyimpanan dibatalkan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    baris_baru = len(df_kamar)
    df_kamar.loc[baris_baru, "nomor kamar"] = nomor
    df_kamar.loc[baris_baru, "tipe kamar"] = tipe_kamar
    df_kamar.loc[baris_baru, "tarif per hari"] = str(tarif)
    df_kamar.loc[baris_baru, "fasilitas"] = fasilitas
    df_kamar.loc[baris_baru, "status"] = "Tersedia"
    df_kamar.loc[baris_baru, "pasien"] = "-"
    df_kamar.loc[baris_baru, "tgl masuk"] = "-"
    df_kamar.loc[baris_baru, "tgl keluar"] = "-"
    df_kamar.to_csv(file_kamar, index=False)

    print(f"\n    [OK] Data kamar {nomor} berhasil disimpan!")
    input("\n    Tekan Enter untuk kembali...")


def ubah_data_kamar():
    os.system("cls")
    tampilkan_header()
    print("\n    --- UBAH DATA KAMAR RAWAT INAP ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    if len(df_kamar) == 0:
        print("    [!] Belum ada data kamar.")
        input("\n    Tekan Enter untuk kembali...")
        return

    cetak_tabel_kamar(df_kamar)
    nomor = input("\n    Masukkan nomor kamar yang akan diubah (0 = batal): ").strip().upper()
    if nomor == "0":
        return

    index_ketemu = -1
    for i in range(len(df_kamar)):
        if ambil_nilai_sel(df_kamar, i, "nomor kamar", "").upper() == nomor:
            index_ketemu = i
            break

    if index_ketemu == -1:
        print(f"\n    [!] Kamar '{nomor}' tidak ditemukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    tipe_lama = ambil_nilai_sel(df_kamar, index_ketemu, "tipe kamar", "-")
    tarif_lama = ambil_nilai_sel(df_kamar, index_ketemu, "tarif per hari", "0")
    fas_lama = ambil_nilai_sel(df_kamar, index_ketemu, "fasilitas", "-")
    st_lama = ambil_nilai_sel(df_kamar, index_ketemu, "status", "-")

    tarif_angka = int(tarif_lama) if tarif_lama.isdigit() else 0
    print(f"\n    Data saat ini untuk Kamar {nomor}:")
    print(f"    - Tipe Kamar : {tipe_lama}")
    print(f"    - Tarif/Hari : Rp {tarif_angka:,}".replace(",", "."))
    print(f"    - Fasilitas  : {fas_lama}")
    print(f"    - Status     : {st_lama}")
    print("    (Kosongkan jika tidak ingin diubah)\n")

    tipe_baru = tipe_lama
    ubah_tipe = input("    Ubah tipe kamar? (y/n): ").strip().lower()
    if ubah_tipe == "y":
        for i in range(len(list_tipe_kamar)):
            print(f"      [{i + 1}] {list_tipe_kamar[i]}")
        while True:
            pilih_tipe = input("    Pilih (1-4): ").strip()
            if pilih_tipe.isdigit() and 1 <= int(pilih_tipe) <= len(list_tipe_kamar):
                tipe_baru = list_tipe_kamar[int(pilih_tipe) - 1]
                break
            print("    [!] Masukkan angka 1-4.")

    tarif_baru = tarif_lama
    while True:
        teks_tarif = input("    Tarif per Hari baru (Rp): ").strip().lower().replace("rp", "").replace(".", "").replace(",", "")
        if teks_tarif == "":
            break
        if teks_tarif.isdigit() and int(teks_tarif) > 0:
            tarif_baru = teks_tarif
            break
        print("    [!] Tarif harus berupa angka lebih dari 0.")

    fasilitas_baru = input("    Fasilitas baru          : ").strip()
    if fasilitas_baru == "":
        fasilitas_baru = fas_lama

    yakin = input(f"\n    Yakin ingin menyimpan perubahan kamar {nomor}? (y/n): ").strip().lower()
    if yakin != "y":
        print("\n    [!] Perubahan dibatalkan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    df_kamar.loc[index_ketemu, "tipe kamar"] = tipe_baru
    df_kamar.loc[index_ketemu, "tarif per hari"] = tarif_baru
    df_kamar.loc[index_ketemu, "fasilitas"] = fasilitas_baru
    df_kamar.to_csv(file_kamar, index=False)
    print(f"\n    [OK] Data kamar {nomor} berhasil diperbarui!")
    input("\n    Tekan Enter untuk kembali...")


def hapus_data_kamar():
    os.system("cls")
    tampilkan_header()
    print("\n    --- HAPUS DATA KAMAR RAWAT INAP ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    if len(df_kamar) == 0:
        print("    [!] Belum ada data kamar.")
        input("\n    Tekan Enter untuk kembali...")
        return

    cetak_tabel_kamar(df_kamar)
    nomor = input("\n    Masukkan nomor kamar yang akan dihapus (0 = batal): ").strip().upper()
    if nomor == "0":
        return

    index_ketemu = -1
    for i in range(len(df_kamar)):
        if ambil_nilai_sel(df_kamar, i, "nomor kamar", "").upper() == nomor:
            index_ketemu = i
            break

    if index_ketemu == -1:
        print(f"\n    [!] Kamar '{nomor}' tidak ditemukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    status_kamar = ambil_nilai_sel(df_kamar, index_ketemu, "status", "-")
    if status_kamar == "Terisi" or status_kamar == "Dipesan":
        print(f"\n    [!] Sistem tidak bisa menghapus kamar {nomor} karena masih berstatus {status_kamar}.")
        input("\n    Tekan Enter untuk kembali...")
        return

    yakin = input(f"    Yakin ingin menghapus kamar {nomor}? (y/n): ").strip().lower()
    if yakin == "y":
        df_kamar = df_kamar.drop(index=pd.Index([index_ketemu])).reset_index(drop=True)
        df_kamar.to_csv(file_kamar, index=False)
        print(f"\n    [OK] Data kamar {nomor} berhasil dihapus.")
    else:
        print("\n    [!] Penghapusan dibatalkan.")
    input("\n    Tekan Enter untuk kembali...")


# ==========================================
# FITUR ADMIN - KELOLA DATA PASIEN
# ==========================================

def lihat_data_pasien():
    os.system("cls")
    tampilkan_header()
    print("\n    --- DAFTAR PASIEN RAWAT INAP AKTIF ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    judul = ["No Kamar", "Nama Pasien", "Status", "Tgl Masuk", "Tgl Keluar"]
    daftar_baris = []

    for i in range(len(df_kamar)):
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        if st == "Dipesan" or st == "Terisi":
            daftar_baris.append([
                ambil_nilai_sel(df_kamar, i, "nomor kamar", "-"),
                ambil_nilai_sel(df_kamar, i, "pasien", "-"),
                st,
                ambil_nilai_sel(df_kamar, i, "tgl masuk", "-"),
                ambil_nilai_sel(df_kamar, i, "tgl keluar", "-")
            ])

    if len(daftar_baris) == 0:
        print("    [!] Belum ada pasien yang menempati atau memesan kamar.")
    else:
        tabel(judul, daftar_baris)

    input("\n    Tekan Enter untuk kembali...")


def ubah_data_pasien():
    os.system("cls")
    tampilkan_header()
    print("\n    --- UBAH DATA PASIEN RAWAT INAP ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    if len(df_kamar) == 0:
        print("    [!] Belum ada data kamar.")
        input("\n    Tekan Enter untuk kembali...")
        return

    cetak_tabel_kamar(df_kamar)
    nomor = input("\n    Nomor Kamar yang ingin diubah (0 = batal): ").strip().upper()
    if nomor == "0":
        return

    index_ketemu = -1
    for i in range(len(df_kamar)):
        if ambil_nilai_sel(df_kamar, i, "nomor kamar", "").upper() == nomor:
            index_ketemu = i
            break

    if index_ketemu == -1:
        print(f"\n    [!] Kamar '{nomor}' tidak ditemukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    st = ambil_nilai_sel(df_kamar, index_ketemu, "status", "-")
    if st == "Tersedia":
        print(f"\n    [!] Kamar {nomor} masih kosong, belum ada data pasien.")
        input("\n    Tekan Enter untuk kembali...")
        return

    psn_lama = ambil_nilai_sel(df_kamar, index_ketemu, "pasien", "-")
    masuk_lama = ambil_nilai_sel(df_kamar, index_ketemu, "tgl masuk", "-")
    keluar_lama = ambil_nilai_sel(df_kamar, index_ketemu, "tgl keluar", "-")

    print(f"\n    Data saat ini untuk Kamar {nomor}:")
    print(f"    - Pasien     : {psn_lama}")
    print(f"    - Status     : {st}")
    print(f"    - Tgl Masuk  : {masuk_lama}")
    print(f"    - Tgl Keluar : {keluar_lama}")
    print("    (Kosongkan jika tidak ingin diubah)\n")

    nama_simpan = psn_lama
    while True:
        nama_baru = input("    Nama pasien baru                 : ").strip()
        if nama_baru == "":
            break
        if nama_baru.replace(" ", "").isalpha():
            nama_simpan = nama_baru
            break
        print("    [!] Nama pasien hanya boleh berisi huruf dan spasi.")

    tgl_masuk_simpan = masuk_lama
    try:
        batas_masuk_awal = datetime.datetime.strptime(masuk_lama, "%Y-%m-%d").date()
        if batas_masuk_awal > datetime.date.today():
            batas_masuk_awal = datetime.date.today()
    except ValueError:
        batas_masuk_awal = datetime.date.today()

    while True:
        tgl_masuk_baru = input("    Tanggal masuk baru (YYYY-MM-DD)  : ").strip()
        if tgl_masuk_baru == "":
            break
        tgl_masuk_bersih = tgl_masuk_baru.replace(" ", "-")
        bagian_masuk = tgl_masuk_bersih.split("-")
        if len(bagian_masuk) == 3 and len(bagian_masuk[0]) == 4 and len(bagian_masuk[1]) == 2 and len(bagian_masuk[2]) == 2 and bagian_masuk[0].isdigit() and bagian_masuk[1].isdigit() and bagian_masuk[2].isdigit():
            try:
                tgl_masuk_valid = datetime.datetime.strptime(tgl_masuk_bersih, "%Y-%m-%d").date()
                if tgl_masuk_valid < batas_masuk_awal:
                    print("    [!] Peringatan: Tanggal masuk tidak masuk akal / terlalu lampau.")
                    continue
                tgl_masuk_simpan = str(tgl_masuk_valid)
                break
            except ValueError:
                print("    [!] Peringatan: Tanggal tidak valid pada kalender.")
        else:
            print("    [!] Peringatan: Penulisan tanggal harus angka urut YYYY-MM-DD atau YYYY MM DD (misal: 2026-12-23 atau 2026 12 23).")

    tgl_keluar_simpan = keluar_lama
    patokan_masuk = datetime.datetime.strptime(tgl_masuk_simpan, "%Y-%m-%d").date()

    while True:
        tgl_keluar_baru = input("    Tanggal keluar baru (YYYY-MM-DD) : ").strip()
        if tgl_keluar_baru == "":
            if tgl_keluar_simpan != "-":
                cek_keluar_lama = datetime.datetime.strptime(tgl_keluar_simpan, "%Y-%m-%d").date()
                selisih_lama = (cek_keluar_lama - patokan_masuk).days
                if selisih_lama < 1:
                    print("    [!] Peringatan: Tanggal keluar lama sebelum/sama dengan tanggal masuk baru. Wajib isi tanggal keluar baru!")
                    continue
                if selisih_lama > 30:
                    print("    [!] Peringatan: Selisih dengan tanggal keluar lama melebihi 30 hari. Wajib isi tanggal keluar baru!")
                    continue
            break
        tgl_keluar_bersih = tgl_keluar_baru.replace(" ", "-")
        bagian_keluar = tgl_keluar_bersih.split("-")
        if len(bagian_keluar) == 3 and len(bagian_keluar[0]) == 4 and len(bagian_keluar[1]) == 2 and len(bagian_keluar[2]) == 2 and bagian_keluar[0].isdigit() and bagian_keluar[1].isdigit() and bagian_keluar[2].isdigit():
            try:
                tgl_keluar_valid = datetime.datetime.strptime(tgl_keluar_bersih, "%Y-%m-%d").date()
                selisih_hari = (tgl_keluar_valid - patokan_masuk).days
                if selisih_hari < 1:
                    print("    [!] Peringatan: Tanggal keluar harus setelah tanggal masuk.")
                    continue
                if selisih_hari > 30:
                    print("    [!] Peringatan: Lama penyewaan kamar maksimal 30 hari.")
                    continue
                tgl_keluar_simpan = str(tgl_keluar_valid)
                break
            except ValueError:
                print("    [!] Peringatan: Tanggal tidak valid pada kalender.")
        else:
            print("    [!] Peringatan: Penulisan tanggal harus angka urut YYYY-MM-DD atau YYYY MM DD (misal: 2026-12-23 atau 2026 12 23).")

    yakin = input(f"\n    Simpan perubahan data pasien kamar {nomor}? (y/n): ").strip().lower()
    if yakin != "y":
        print("\n    [!] Perubahan dibatalkan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    df_kamar.loc[index_ketemu, "pasien"] = nama_simpan
    df_kamar.loc[index_ketemu, "tgl masuk"] = tgl_masuk_simpan
    df_kamar.loc[index_ketemu, "tgl keluar"] = tgl_keluar_simpan

    df_kamar.to_csv(file_kamar, index=False)
    print(f"\n    [OK] Data pasien kamar {nomor} berhasil diperbarui!")
    input("\n    Tekan Enter untuk kembali...")


def checkout_pasien():
    os.system("cls")
    tampilkan_header()
    print("\n    --- CHECKOUT PASIEN & PERHITUNGAN REFUND ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    indeks_terisi = []
    for i in range(len(df_kamar)):
        if ambil_nilai_sel(df_kamar, i, "status", "-") == "Terisi":
            indeks_terisi.append(i)

    if len(indeks_terisi) == 0:
        print("    [!] Belum ada pasien berstatus Terisi untuk di-checkout.")
        input("\n    Tekan Enter untuk kembali...")
        return

    cetak_tabel_kamar(df_kamar, indeks_terisi)
    nomor = input("\n    Nomor Kamar pasien yang akan checkout (0 = batal): ").strip().upper()
    if nomor == "0":
        return

    index_ketemu = -1
    for i in range(len(df_kamar)):
        no_k = ambil_nilai_sel(df_kamar, i, "nomor kamar", "").upper()
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        if no_k == nomor and st == "Terisi":
            index_ketemu = i
            break

    if index_ketemu == -1:
        print(f"\n    [!] Kamar '{nomor}' tidak ditemukan atau tidak sedang berstatus Terisi.")
        input("\n    Tekan Enter untuk kembali...")
        return

    tarif_str = ambil_nilai_sel(df_kamar, index_ketemu, "tarif per hari", "0")
    tarif = int(tarif_str) if tarif_str.isdigit() else 0
    pasien_nama = ambil_nilai_sel(df_kamar, index_ketemu, "pasien", "-")
    tipe_kamar = ambil_nilai_sel(df_kamar, index_ketemu, "tipe kamar", "-")
    no_kamar_asli = ambil_nilai_sel(df_kamar, index_ketemu, "nomor kamar", "-")
    tgl_masuk_str = ambil_nilai_sel(df_kamar, index_ketemu, "tgl masuk", str(datetime.date.today()))
    tgl_keluar_str = ambil_nilai_sel(df_kamar, index_ketemu, "tgl keluar", str(datetime.date.today()))

    masuk = datetime.datetime.strptime(tgl_masuk_str, "%Y-%m-%d").date()
    keluar_rencana = datetime.datetime.strptime(tgl_keluar_str, "%Y-%m-%d").date()
    hari_rencana = (keluar_rencana - masuk).days
    if hari_rencana < 1:
        hari_rencana = 1

    hari_terpakai = (datetime.date.today() - masuk).days
    if hari_terpakai < 1:
        hari_terpakai = 1
    if hari_terpakai > hari_rencana:
        hari_terpakai = hari_rencana

    total_dibayar = tarif * hari_rencana
    biaya_terpakai = tarif * hari_terpakai
    dana_kembali = total_dibayar - biaya_terpakai

    print(f"\n    Rincian Checkout Kamar {nomor}:")
    print(f"    - Pasien         : {pasien_nama}")
    print(f"    - Tarif / Hari   : Rp {tarif:,}".replace(",", "."))
    print(f"    - Lama Rencana   : {hari_rencana} hari (Total Dibayar: Rp {total_dibayar:,})".replace(",", "."))
    print(f"    - Hari Terpakai  : {hari_terpakai} hari")
    print(f"    - Biaya Terpakai : Rp {biaya_terpakai:,}".replace(",", "."))
    print(f"    - Dana Kembali   : Rp {dana_kembali:,}".replace(",", "."))

    no_rek = "-"
    if dana_kembali > 0:
        df_akun = pd.read_csv(file_akun, dtype=str)
        if "no rekening" in df_akun.columns:
            for i in range(len(df_akun)):
                nama_ak = ambil_nilai_sel(df_akun, i, "nama lengkap", "").lower()
                if nama_ak == pasien_nama.lower():
                    rek_terdaftar = ambil_nilai_sel(df_akun, i, "no rekening", "")
                    if rek_terdaftar != "" and rek_terdaftar != "-":
                        no_rek = rek_terdaftar
                    break

        if no_rek != "-":
            print(f"    - Rekening Refund: {no_rek}")
        else:
            while True:
                no_rek = input("    Nomor Rekening Pasien untuk Refund: ").strip()
                if no_rek.isdigit() and 10 <= len(no_rek) <= 15:
                    break
                print("    [!] Nomor rekening harus berupa angka (minimal 10, maksimal 15 karakter).")

    yakin = input(f"\n    Konfirmasi checkout pasien dari kamar {nomor}? (y/n): ").strip().lower()
    if yakin != "y":
        print("\n    [!] Checkout dibatalkan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    df_riwayat_rawat = pd.read_csv(file_riwayat_rawat, dtype=str)
    baris_riw = len(df_riwayat_rawat)
    df_riwayat_rawat.loc[baris_riw, "tanggal proses"] = str(datetime.date.today())
    df_riwayat_rawat.loc[baris_riw, "jenis transaksi"] = "Checkout"
    df_riwayat_rawat.loc[baris_riw, "nomor kamar"] = no_kamar_asli
    df_riwayat_rawat.loc[baris_riw, "tipe kamar"] = tipe_kamar
    df_riwayat_rawat.loc[baris_riw, "pasien"] = pasien_nama
    df_riwayat_rawat.loc[baris_riw, "tgl masuk"] = tgl_masuk_str
    df_riwayat_rawat.loc[baris_riw, "tgl keluar"] = tgl_keluar_str
    df_riwayat_rawat.loc[baris_riw, "hari terpakai"] = str(hari_terpakai)
    df_riwayat_rawat.loc[baris_riw, "total tagihan"] = f"Rp {biaya_terpakai:,}".replace(",", ".")
    df_riwayat_rawat.loc[baris_riw, "dana kembali"] = f"Rp {dana_kembali:,}".replace(",", ".")
    df_riwayat_rawat.loc[baris_riw, "no rekening pasien"] = no_rek
    df_riwayat_rawat.to_csv(file_riwayat_rawat, index=False)

    df_kamar.loc[index_ketemu, "status"] = "Tersedia"
    df_kamar.loc[index_ketemu, "pasien"] = "-"
    df_kamar.loc[index_ketemu, "tgl masuk"] = "-"
    df_kamar.loc[index_ketemu, "tgl keluar"] = "-"
    df_kamar.to_csv(file_kamar, index=False)

    print(f"\n    [OK] Checkout kamar {nomor} selesai! Kamar kembali Tersedia.")
    if dana_kembali > 0:
        dana_teks = f"Rp {dana_kembali:,}".replace(",", ".")
        print(f"    [INFO REFUND] Dana sebesar {dana_teks} sudah dikembalikan ke rekening {no_rek}.")
    input("\n    Tekan Enter untuk kembali...")


def batalkan_pemesanan_kamar():
    os.system("cls")
    tampilkan_header()
    print("\n    --- BATALKAN PEMESANAN KAMAR PASIEN ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    indeks_dipesan = []
    for i in range(len(df_kamar)):
        if ambil_nilai_sel(df_kamar, i, "status", "-") == "Dipesan":
            indeks_dipesan.append(i)

    if len(indeks_dipesan) == 0:
        print("    [!] Belum ada pemesanan kamar yang menunggu pembayaran.")
        input("\n    Tekan Enter untuk kembali...")
        return

    cetak_tabel_kamar(df_kamar, indeks_dipesan)
    nomor = input("\n    Nomor Kamar yang pemesanannya dibatalkan (0 = batal): ").strip().upper()
    if nomor == "0":
        return

    index_ketemu = -1
    for i in range(len(df_kamar)):
        no_k = ambil_nilai_sel(df_kamar, i, "nomor kamar", "").upper()
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        if no_k == nomor and st == "Dipesan":
            index_ketemu = i
            break

    if index_ketemu == -1:
        print(f"\n    [!] Kamar '{nomor}' tidak ditemukan atau tidak sedang berstatus Dipesan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    pasien_nama = ambil_nilai_sel(df_kamar, index_ketemu, "pasien", "-")
    yakin = input(f"    Yakin membatalkan pemesanan kamar {nomor} atas nama {pasien_nama}? (y/n): ").strip().lower()
    if yakin != "y":
        print("\n    [!] Pembatalan dibatalkan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    df_riwayat_rawat = pd.read_csv(file_riwayat_rawat, dtype=str)
    baris_riw = len(df_riwayat_rawat)
    df_riwayat_rawat.loc[baris_riw, "tanggal proses"] = str(datetime.date.today())
    df_riwayat_rawat.loc[baris_riw, "jenis transaksi"] = "Pembatalan Reservasi"
    df_riwayat_rawat.loc[baris_riw, "nomor kamar"] = ambil_nilai_sel(df_kamar, index_ketemu, "nomor kamar", "-")
    df_riwayat_rawat.loc[baris_riw, "tipe kamar"] = ambil_nilai_sel(df_kamar, index_ketemu, "tipe kamar", "-")
    df_riwayat_rawat.loc[baris_riw, "pasien"] = pasien_nama
    df_riwayat_rawat.loc[baris_riw, "tgl masuk"] = ambil_nilai_sel(df_kamar, index_ketemu, "tgl masuk", "-")
    df_riwayat_rawat.loc[baris_riw, "tgl keluar"] = ambil_nilai_sel(df_kamar, index_ketemu, "tgl keluar", "-")
    df_riwayat_rawat.loc[baris_riw, "hari terpakai"] = "0"
    df_riwayat_rawat.loc[baris_riw, "total tagihan"] = "Rp 0"
    df_riwayat_rawat.loc[baris_riw, "dana kembali"] = "Rp 0"
    df_riwayat_rawat.loc[baris_riw, "no rekening pasien"] = "-"
    df_riwayat_rawat.to_csv(file_riwayat_rawat, index=False)

    df_kamar.loc[index_ketemu, "status"] = "Tersedia"
    df_kamar.loc[index_ketemu, "pasien"] = "-"
    df_kamar.loc[index_ketemu, "tgl masuk"] = "-"
    df_kamar.loc[index_ketemu, "tgl keluar"] = "-"
    df_kamar.to_csv(file_kamar, index=False)

    print(f"\n    [OK] Pemesanan kamar {nomor} berhasil dibatalkan.")
    input("\n    Tekan Enter untuk kembali...")


# ==========================================
# FITUR ADMIN - KELOLA DATA SURAT RUJUKAN
# ==========================================

def lihat_data_rujukan():
    os.system("cls")
    tampilkan_header()
    print("\n    --- DAFTAR SURAT RUJUKAN TERDAFTAR ---\n")

    df_rujukan = pd.read_csv(file_rujukan, dtype=str)
    if len(df_rujukan) == 0:
        print("    [!] Belum ada data surat rujukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    judul = ["No Rujukan", "Nama Pasien", "NIK", "Asal Rujukan", "Status"]
    daftar_baris = []
    for i in range(len(df_rujukan)):
        daftar_baris.append([
            ambil_nilai_sel(df_rujukan, i, "nomor rujukan", "-"),
            ambil_nilai_sel(df_rujukan, i, "nama pasien", "-"),
            ambil_nilai_sel(df_rujukan, i, "nik", "-"),
            ambil_nilai_sel(df_rujukan, i, "asal rujukan", "-"),
            ambil_nilai_sel(df_rujukan, i, "status rujukan", "-")
        ])

    tabel(judul, daftar_baris)
    input("\n    Tekan Enter untuk kembali...")


def tambah_data_rujukan():
    os.system("cls")
    tampilkan_header()
    print("\n    --- TAMBAH DATA SURAT RUJUKAN ---")
    print("    (Ketik 0 pada Nomor Rujukan untuk batal)\n")

    df_rujukan = pd.read_csv(file_rujukan, dtype=str)

    while True:
        no_rujukan = input("    Nomor Surat Rujukan     : ").strip().upper()
        if no_rujukan == "0":
            return
        if no_rujukan == "":
            print("    [!] Nomor surat rujukan wajib diisi.")
            continue

        sudah_ada = False
        for i in range(len(df_rujukan)):
            if ambil_nilai_sel(df_rujukan, i, "nomor rujukan", "").upper() == no_rujukan:
                sudah_ada = True
        if sudah_ada:
            print(f"    [!] Nomor rujukan '{no_rujukan}' sudah terdaftar.")
        else:
            break

    while True:
        nama_pasien = input("    Nama Pasien             : ").strip()
        nik_pasien = input("    NIK Pasien (16 digit)   : ").strip()
        asal_rujukan = input("    Asal Rujukan            : ").strip()
        if nama_pasien == "" or nik_pasien == "" or asal_rujukan == "":
            print("    [!] Semua data rujukan wajib diisi.\n")
            continue
        if not nama_pasien.replace(" ", "").isalpha():
            print("    [!] Nama pasien harus berupa huruf (boleh spasi).\n")
            continue
        if not nik_pasien.isdigit() or len(nik_pasien) != 16:
            print("    [!] NIK pasien harus berupa angka tepat 16 digit.\n")
            continue
        break

    yakin = input("\n    Simpan surat rujukan ini? (y/n): ").strip().lower()
    if yakin != "y":
        print("\n    [!] Penyimpanan dibatalkan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    baris_baru = len(df_rujukan)
    df_rujukan.loc[baris_baru, "nomor rujukan"] = no_rujukan
    df_rujukan.loc[baris_baru, "nama pasien"] = nama_pasien
    df_rujukan.loc[baris_baru, "nik"] = nik_pasien
    df_rujukan.loc[baris_baru, "asal rujukan"] = asal_rujukan
    df_rujukan.loc[baris_baru, "status rujukan"] = "Aktif"
    df_rujukan.to_csv(file_rujukan, index=False)

    df_riwayat_rujukan = pd.read_csv(file_riwayat_rujukan, dtype=str)
    baris_riw = len(df_riwayat_rujukan)
    df_riwayat_rujukan.loc[baris_riw, "tanggal"] = str(datetime.date.today())
    df_riwayat_rujukan.loc[baris_riw, "nomor rujukan"] = no_rujukan
    df_riwayat_rujukan.loc[baris_riw, "nama pasien"] = nama_pasien
    df_riwayat_rujukan.loc[baris_riw, "nik"] = nik_pasien
    df_riwayat_rujukan.loc[baris_riw, "asal rujukan"] = asal_rujukan
    df_riwayat_rujukan.loc[baris_riw, "status rujukan"] = "Aktif"
    df_riwayat_rujukan.to_csv(file_riwayat_rujukan, index=False)

    print(f"\n    [OK] Surat rujukan '{no_rujukan}' berhasil disimpan!")
    input("\n    Tekan Enter untuk kembali...")


def ubah_data_rujukan():
    os.system("cls")
    tampilkan_header()
    print("\n    --- UBAH DATA SURAT RUJUKAN ---\n")

    df_rujukan = pd.read_csv(file_rujukan, dtype=str)
    if len(df_rujukan) == 0:
        print("    [!] Belum ada data surat rujukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    judul = ["No Rujukan", "Nama Pasien", "NIK", "Asal Rujukan", "Status"]
    daftar_baris = []
    for i in range(len(df_rujukan)):
        daftar_baris.append([
            ambil_nilai_sel(df_rujukan, i, "nomor rujukan", "-"),
            ambil_nilai_sel(df_rujukan, i, "nama pasien", "-"),
            ambil_nilai_sel(df_rujukan, i, "nik", "-"),
            ambil_nilai_sel(df_rujukan, i, "asal rujukan", "-"),
            ambil_nilai_sel(df_rujukan, i, "status rujukan", "-")
        ])
    tabel(judul, daftar_baris)

    no_rujukan = input("\n    Nomor Surat Rujukan yang diubah (0 = batal): ").strip().upper()
    if no_rujukan == "0":
        return

    index_ketemu = -1
    for i in range(len(df_rujukan)):
        if ambil_nilai_sel(df_rujukan, i, "nomor rujukan", "").upper() == no_rujukan:
            index_ketemu = i
            break

    if index_ketemu == -1:
        print(f"\n    [!] Nomor rujukan '{no_rujukan}' tidak ditemukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    print("\n    (Kosongkan jika tidak ingin diubah)")
    while True:
        nama_baru = input("    Nama Pasien baru      : ").strip()
        if nama_baru == "" or nama_baru.replace(" ", "").isalpha():
            break
        print("    [!] Nama pasien harus berupa huruf (boleh spasi).")

    while True:
        nik_baru = input("    NIK Pasien baru       : ").strip()
        if nik_baru == "" or (nik_baru.isdigit() and len(nik_baru) == 16):
            break
        print("    [!] NIK pasien harus berupa angka tepat 16 digit.")

    asal_baru = input("    Asal Rujukan baru     : ").strip()

    status_lama = ambil_nilai_sel(df_rujukan, index_ketemu, "status rujukan", "Aktif")
    status_baru = status_lama
    ubah_status = input("    Ubah status rujukan? (y/n): ").strip().lower()
    if ubah_status == "y":
        for i in range(len(status_rujukan)):
            print(f"      [{i + 1}] {status_rujukan[i]}")
        while True:
            pilih_st = input("    Pilih (1-3): ").strip()
            if pilih_st.isdigit() and 1 <= int(pilih_st) <= len(status_rujukan):
                calon_status = status_rujukan[int(pilih_st) - 1]
                if (status_lama == "Terpakai" or status_lama == "Tidak Aktif") and calon_status == "Aktif":
                    print(f"    [!] Status surat rujukan sudah '{status_lama}', tidak bisa diubah menjadi 'Aktif'!")
                    continue
                status_baru = calon_status
                break
            print("    [!] Masukkan angka 1-3.")

    yakin = input(f"\n    Simpan perubahan rujukan '{no_rujukan}'? (y/n): ").strip().lower()
    if yakin != "y":
        print("\n    [!] Perubahan dibatalkan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    if nama_baru != "":
        df_rujukan.loc[index_ketemu, "nama pasien"] = nama_baru
    if nik_baru != "":
        df_rujukan.loc[index_ketemu, "nik"] = nik_baru
    if asal_baru != "":
        df_rujukan.loc[index_ketemu, "asal rujukan"] = asal_baru
    df_rujukan.loc[index_ketemu, "status rujukan"] = status_baru
    df_rujukan.to_csv(file_rujukan, index=False)

    df_riwayat_rujukan = pd.read_csv(file_riwayat_rujukan, dtype=str)
    baris_riw = len(df_riwayat_rujukan)
    df_riwayat_rujukan.loc[baris_riw, "tanggal"] = str(datetime.date.today())
    df_riwayat_rujukan.loc[baris_riw, "nomor rujukan"] = ambil_nilai_sel(df_rujukan, index_ketemu, "nomor rujukan", "-")
    df_riwayat_rujukan.loc[baris_riw, "nama pasien"] = ambil_nilai_sel(df_rujukan, index_ketemu, "nama pasien", "-")
    df_riwayat_rujukan.loc[baris_riw, "nik"] = ambil_nilai_sel(df_rujukan, index_ketemu, "nik", "-")
    df_riwayat_rujukan.loc[baris_riw, "asal rujukan"] = ambil_nilai_sel(df_rujukan, index_ketemu, "asal rujukan", "-")
    df_riwayat_rujukan.loc[baris_riw, "status rujukan"] = ambil_nilai_sel(df_rujukan, index_ketemu, "status rujukan", "-")
    df_riwayat_rujukan.to_csv(file_riwayat_rujukan, index=False)

    print(f"\n    [OK] Data surat rujukan '{no_rujukan}' berhasil diperbarui!")
    input("\n    Tekan Enter untuk kembali...")


def hapus_data_rujukan():
    os.system("cls")
    tampilkan_header()
    print("\n    --- HAPUS DATA SURAT RUJUKAN ---\n")

    df_rujukan = pd.read_csv(file_rujukan, dtype=str)
    if len(df_rujukan) == 0:
        print("    [!] Belum ada data surat rujukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    no_rujukan = input("    Nomor Surat Rujukan yang dihapus (0 = batal): ").strip().upper()
    if no_rujukan == "0":
        return

    index_ketemu = -1
    for i in range(len(df_rujukan)):
        if ambil_nilai_sel(df_rujukan, i, "nomor rujukan", "").upper() == no_rujukan:
            index_ketemu = i
            break

    if index_ketemu == -1:
        print(f"\n    [!] Nomor rujukan '{no_rujukan}' tidak ditemukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    yakin = input(f"    Yakin ingin menghapus surat rujukan '{no_rujukan}'? (y/n): ").strip().lower()
    if yakin == "y":
        df_riwayat_rujukan = pd.read_csv(file_riwayat_rujukan, dtype=str)
        baris_riw = len(df_riwayat_rujukan)
        df_riwayat_rujukan.loc[baris_riw, "tanggal"] = str(datetime.date.today())
        df_riwayat_rujukan.loc[baris_riw, "nomor rujukan"] = ambil_nilai_sel(df_rujukan, index_ketemu, "nomor rujukan", "-")
        df_riwayat_rujukan.loc[baris_riw, "nama pasien"] = ambil_nilai_sel(df_rujukan, index_ketemu, "nama pasien", "-")
        df_riwayat_rujukan.loc[baris_riw, "nik"] = ambil_nilai_sel(df_rujukan, index_ketemu, "nik", "-")
        df_riwayat_rujukan.loc[baris_riw, "asal rujukan"] = ambil_nilai_sel(df_rujukan, index_ketemu, "asal rujukan", "-")
        df_riwayat_rujukan.loc[baris_riw, "status rujukan"] = ambil_nilai_sel(df_rujukan, index_ketemu, "status rujukan", "-")
        df_riwayat_rujukan.to_csv(file_riwayat_rujukan, index=False)

        df_rujukan = df_rujukan.drop(index=pd.Index([index_ketemu])).reset_index(drop=True)
        df_rujukan.to_csv(file_rujukan, index=False)
        print(f"\n    [OK] Surat rujukan '{no_rujukan}' berhasil dihapus.")
    else:
        print("\n    [!] Penghapusan dibatalkan.")
    input("\n    Tekan Enter untuk kembali...")


def lihat_riwayat_rujukan():
    os.system("cls")
    tampilkan_header()
    print("\n    --- RIWAYAT DATA SURAT RUJUKAN ---\n")

    df_riwayat_rujukan = pd.read_csv(file_riwayat_rujukan, dtype=str)
    if len(df_riwayat_rujukan) == 0:
        print("    [!] Belum ada riwayat surat rujukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    judul = ["Tanggal", "No Rujukan", "Nama Pasien", "NIK", "Asal Rujukan", "Status"]
    daftar_baris = []
    for i in range(len(df_riwayat_rujukan)):
        daftar_baris.append([
            ambil_nilai_sel(df_riwayat_rujukan, i, "tanggal", "-"),
            ambil_nilai_sel(df_riwayat_rujukan, i, "nomor rujukan", "-"),
            ambil_nilai_sel(df_riwayat_rujukan, i, "nama pasien", "-"),
            ambil_nilai_sel(df_riwayat_rujukan, i, "nik", "-"),
            ambil_nilai_sel(df_riwayat_rujukan, i, "asal rujukan", "-"),
            ambil_nilai_sel(df_riwayat_rujukan, i, "status rujukan", "-")
        ])

    tabel(judul, daftar_baris)
    input("\n    Tekan Enter untuk kembali...")


def lihat_riwayat_rawat_inap():
    os.system("cls")
    tampilkan_header()
    print("\n    --- RIWAYAT TRANSAKSI & RAWAT INAP ---\n")

    df_riwayat_rawat = pd.read_csv(file_riwayat_rawat, dtype=str)
    if len(df_riwayat_rawat) == 0:
        print("    [!] Belum ada riwayat transaksi rawat inap.")
        input("\n    Tekan Enter untuk kembali...")
        return

    judul = ["Tanggal", "Jenis Transaksi", "Kamar", "Pasien", "Hari", "Tagihan", "Refund"]
    daftar_baris = []
    for i in range(len(df_riwayat_rawat)):
        daftar_baris.append([
            ambil_nilai_sel(df_riwayat_rawat, i, "tanggal proses", "-"),
            ambil_nilai_sel(df_riwayat_rawat, i, "jenis transaksi", "-"),
            ambil_nilai_sel(df_riwayat_rawat, i, "nomor kamar", "-"),
            ambil_nilai_sel(df_riwayat_rawat, i, "pasien", "-"),
            ambil_nilai_sel(df_riwayat_rawat, i, "hari terpakai", "0"),
            ambil_nilai_sel(df_riwayat_rawat, i, "total tagihan", "Rp 0"),
            ambil_nilai_sel(df_riwayat_rawat, i, "dana kembali", "Rp 0")
        ])

    tabel(judul, daftar_baris)
    input("\n    Tekan Enter untuk kembali...")


# ==========================================
# FITUR PASIEN
# ==========================================

def cari_data_kamar():
    while True:
        os.system("cls")
        tampilkan_header()
        print("\n    --- CARI & TAMPILKAN KAMAR TERSEDIA ---")

        df_kamar = pd.read_csv(file_kamar, dtype=str)
        indeks_tersedia = []
        for i in range(len(df_kamar)):
            if ambil_nilai_sel(df_kamar, i, "status", "-") == "Tersedia":
                indeks_tersedia.append(i)

        if len(indeks_tersedia) == 0:
            print("\n    [!] Belum ada kamar yang tersedia saat ini.")
            input("\n    Tekan Enter untuk kembali...")
            return

        print("\n    Masukkan kriteria pencarian (kosongkan jika tidak difilter):")
        fasilitas_cari = input("    Kata kunci fasilitas (mis. AC)    : ").strip().lower()

        tarif_maks = 0
        while True:
            teks_tarif = input("    Batas Tarif Maksimal per Hari (Rp): ").strip().lower().replace("rp", "").replace(".", "").replace(",", "")
            if teks_tarif == "":
                break
            if teks_tarif.isdigit() and int(teks_tarif) > 0:
                tarif_maks = int(teks_tarif)
                break
            print("    [!] Masukkan angka saja untuk batas tarif.")

        indeks_hasil = []
        for i in indeks_tersedia:
            tarif_str = ambil_nilai_sel(df_kamar, i, "tarif per hari", "0")
            tarif_kamar = int(tarif_str) if tarif_str.isdigit() else 0
            fas_kamar = ambil_nilai_sel(df_kamar, i, "fasilitas", "-").lower()

            cocok_fasilitas = True
            cocok_tarif = True

            if fasilitas_cari != "" and fasilitas_cari not in fas_kamar:
                cocok_fasilitas = False
            if tarif_maks > 0 and tarif_kamar > tarif_maks:
                cocok_tarif = False

            if cocok_fasilitas and cocok_tarif:
                indeks_hasil.append(i)

        # Nested loop untuk mengurutkan dari tarif termurah
        for i in range(len(indeks_hasil)):
            for j in range(i + 1, len(indeks_hasil)):
                tarif_i_str = ambil_nilai_sel(df_kamar, indeks_hasil[i], "tarif per hari", "0")
                tarif_j_str = ambil_nilai_sel(df_kamar, indeks_hasil[j], "tarif per hari", "0")
                tarif_i = int(tarif_i_str) if tarif_i_str.isdigit() else 0
                tarif_j = int(tarif_j_str) if tarif_j_str.isdigit() else 0
                if tarif_j < tarif_i:
                    temp = indeks_hasil[i]
                    indeks_hasil[i] = indeks_hasil[j]
                    indeks_hasil[j] = temp

        print("\n    --- HASIL PENCARIAN KAMAR ---")
        if len(indeks_hasil) == 0:
            print("    [!] Tidak ada kamar yang sesuai dengan kriteria.")
        else:
            cetak_tabel_kamar(df_kamar, indeks_hasil)

        lanjut = input("\n    Cari lagi? (y/n): ").strip().lower()
        if lanjut != "y":
            return


def reservasi_kamar(nama_pasien):
    os.system("cls")
    tampilkan_header()
    print("\n    --- RESERVASI KAMAR RAWAT INAP ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)

    for i in range(len(df_kamar)):
        psn = ambil_nilai_sel(df_kamar, i, "pasien", "-").lower()
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        no_k = ambil_nilai_sel(df_kamar, i, "nomor kamar", "-")
        if psn == nama_pasien.lower() and (st == "Dipesan" or st == "Terisi"):
            print(f"    [!] Anda sudah memiliki kamar aktif: {no_k} ({st}).")
            input("\n    Tekan Enter untuk kembali...")
            return

    punya_rujukan = input("    Apakah Anda memiliki surat rujukan rawat inap? (y/n): ").strip().lower()
    if punya_rujukan != "y":
        print("\n    [!] Pemesanan kamar rawat inap wajib memiliki surat rujukan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    indeks_tersedia = []
    for i in range(len(df_kamar)):
        if ambil_nilai_sel(df_kamar, i, "status", "-") == "Tersedia":
            indeks_tersedia.append(i)

    if len(indeks_tersedia) == 0:
        print("\n    [!] Semua kamar rawat inap sedang penuh.")
        input("\n    Tekan Enter untuk kembali...")
        return

    input_nama = input("    Masukkan Nama Lengkap (0 = batal)   : ").strip()
    if input_nama == "0":
        return
    input_nik = input("    Masukkan NIK (16 digit)               : ").strip()
    no_rujukan = input("    Masukkan Nomor Surat Rujukan          : ").strip().upper()

    if input_nama == "" or input_nik == "" or no_rujukan == "":
        print("\n    [!] Nama, NIK, dan Nomor Surat Rujukan wajib diisi!")
        input("\n    Tekan Enter untuk kembali...")
        return

    df_akun = pd.read_csv(file_akun, dtype=str)
    nik_akun = ""
    for i in range(len(df_akun)):
        nama_ak = ambil_nilai_sel(df_akun, i, "nama lengkap", "")
        if nama_ak.lower() == nama_pasien.lower():
            nik_akun = ambil_nilai_sel(df_akun, i, "nik", "")
            break

    if input_nama.lower() != nama_pasien.lower() or input_nik != nik_akun:
        print("\n    [!] Nama atau NIK tidak sesuai dengan data registrasi akun Anda!")
        input("\n    Tekan Enter untuk kembali...")
        return

    df_rujukan = pd.read_csv(file_rujukan, dtype=str)
    index_rujukan = -1
    for i in range(len(df_rujukan)):
        if ambil_nilai_sel(df_rujukan, i, "nomor rujukan", "").upper() == no_rujukan:
            index_rujukan = i
            break

    if index_rujukan == -1:
        print("\n    [!] Nomor surat rujukan tidak ditemukan atau belum diinput admin.")
        input("\n    Tekan Enter untuk kembali...")
        return

    nama_ruj = ambil_nilai_sel(df_rujukan, index_rujukan, "nama pasien", "")
    nik_ruj = ambil_nilai_sel(df_rujukan, index_rujukan, "nik", "")
    if nama_ruj.lower() != input_nama.lower() or nik_ruj != input_nik:
        print("\n    [!] Data Nama atau NIK pada surat rujukan tidak cocok dengan identitas Anda!")
        input("\n    Tekan Enter untuk kembali...")
        return

    st_rujukan = ambil_nilai_sel(df_rujukan, index_rujukan, "status rujukan", "-")
    if st_rujukan.lower() != "aktif":
        print(f"\n    [!] Surat rujukan '{no_rujukan}' sudah terpakai / tidak aktif.")
        input("\n    Tekan Enter untuk kembali...")
        return

    print("\n    [OK] Surat rujukan valid! Silakan pilih kamar tersedia:\n")
    cetak_tabel_kamar(df_kamar, indeks_tersedia)

    nomor = input("\n    Nomor Kamar yang dipilih (0 = batal): ").strip().upper()
    if nomor == "0":
        return

    index_kamar = -1
    for i in range(len(df_kamar)):
        no_k = ambil_nilai_sel(df_kamar, i, "nomor kamar", "").upper()
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        if no_k == nomor and st == "Tersedia":
            index_kamar = i
            break

    if index_kamar == -1:
        print("\n    [!] Nomor kamar tidak ditemukan atau sudah dipesan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    while True:
        lama_teks = input("    Perkiraan lama rawat inap (hari)     : ").strip()
        if lama_teks.isdigit() and 1 <= int(lama_teks) <= 365:
            lama = int(lama_teks)
            break
        print("    [!] Masukkan angka hari antara 1 sampai 365.")

    tarif_str = ambil_nilai_sel(df_kamar, index_kamar, "tarif per hari", "0")
    tarif = int(tarif_str) if tarif_str.isdigit() else 0
    total_biaya = tarif * lama

    no_ruj_asli = ambil_nilai_sel(df_rujukan, index_rujukan, "nomor rujukan", "-")
    asal_ruj = ambil_nilai_sel(df_rujukan, index_rujukan, "asal rujukan", "-")
    nama_psn_ruj = ambil_nilai_sel(df_rujukan, index_rujukan, "nama pasien", "-")
    nik_psn_ruj = ambil_nilai_sel(df_rujukan, index_rujukan, "nik", "-")

    print(f"\n    Perkiraan Total Tagihan : Rp {total_biaya:,}".replace(",", "."))
    print(f"    Surat Rujukan           : {no_ruj_asli} | {asal_ruj}")

    yakin = input(f"\n    Yakin ingin mereservasi kamar {nomor}? (y/n): ").strip().lower()
    if yakin != "y":
        print("\n    [!] Reservasi dibatalkan.")
        input("\n    Tekan Enter untuk kembali...")
        return

    hari_ini = datetime.date.today()
    tgl_keluar = hari_ini + datetime.timedelta(days=lama)

    df_kamar.loc[index_kamar, "status"] = "Dipesan"
    df_kamar.loc[index_kamar, "pasien"] = nama_pasien
    df_kamar.loc[index_kamar, "tgl masuk"] = str(hari_ini)
    df_kamar.loc[index_kamar, "tgl keluar"] = str(tgl_keluar)

    df_rujukan.loc[index_rujukan, "status rujukan"] = "Terpakai"

    df_kamar.to_csv(file_kamar, index=False)
    df_rujukan.to_csv(file_rujukan, index=False)

    df_riwayat_rujukan = pd.read_csv(file_riwayat_rujukan, dtype=str)
    baris_riw = len(df_riwayat_rujukan)
    df_riwayat_rujukan.loc[baris_riw, "tanggal"] = str(datetime.date.today())
    df_riwayat_rujukan.loc[baris_riw, "nomor rujukan"] = no_ruj_asli
    df_riwayat_rujukan.loc[baris_riw, "nama pasien"] = nama_psn_ruj
    df_riwayat_rujukan.loc[baris_riw, "nik"] = nik_psn_ruj
    df_riwayat_rujukan.loc[baris_riw, "asal rujukan"] = asal_ruj
    df_riwayat_rujukan.loc[baris_riw, "status rujukan"] = "Terpakai"
    df_riwayat_rujukan.to_csv(file_riwayat_rujukan, index=False)

    print(f"\n    [OK] Kamar {nomor} berhasil dipesan! Silakan lanjut ke menu Pembayaran.")
    input("\n    Tekan Enter untuk kembali...")


def cek_status_reservasi(nama_pasien):
    os.system("cls")
    tampilkan_header()
    print("\n    --- STATUS RESERVASI KAMAR ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    index_saya = -1
    for i in range(len(df_kamar)):
        psn = ambil_nilai_sel(df_kamar, i, "pasien", "-").lower()
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        if psn == nama_pasien.lower() and (st == "Dipesan" or st == "Terisi"):
            index_saya = i
            break

    if index_saya == -1:
        print("    [!] Anda belum memiliki reservasi kamar aktif.")
        input("\n    Tekan Enter untuk kembali...")
        return

    tgl_masuk_str = ambil_nilai_sel(df_kamar, index_saya, "tgl masuk", str(datetime.date.today()))
    tgl_keluar_str = ambil_nilai_sel(df_kamar, index_saya, "tgl keluar", str(datetime.date.today()))
    masuk = datetime.datetime.strptime(tgl_masuk_str, "%Y-%m-%d").date()
    keluar = datetime.datetime.strptime(tgl_keluar_str, "%Y-%m-%d").date()
    lama = (keluar - masuk).days
    if lama < 1:
        lama = 1

    tarif_str = ambil_nilai_sel(df_kamar, index_saya, "tarif per hari", "0")
    tarif = int(tarif_str) if tarif_str.isdigit() else 0
    total = tarif * lama

    no_kamar = ambil_nilai_sel(df_kamar, index_saya, "nomor kamar", "-")
    tipe_kamar = ambil_nilai_sel(df_kamar, index_saya, "tipe kamar", "-")
    fasilitas = ambil_nilai_sel(df_kamar, index_saya, "fasilitas", "-")
    status_kamar = ambil_nilai_sel(df_kamar, index_saya, "status", "-")

    print(f"    Nomor Kamar   : {no_kamar}")
    print(f"    Tipe Kamar    : {tipe_kamar}")
    print(f"    Tarif/Hari    : Rp {tarif:,}".replace(",", "."))
    print(f"    Fasilitas     : {fasilitas}")
    print(f"    Tgl Masuk     : {tgl_masuk_str}")
    print(f"    Tgl Keluar    : {tgl_keluar_str} ({lama} hari)")
    print(f"    Total Biaya   : Rp {total:,}".replace(",", "."))
    if status_kamar == "Dipesan":
        print("    Status        : Dipesan (Menunggu Pembayaran)")
    else:
        print("    Status        : Terisi (Lunas / Sedang Ditempati)")

    input("\n    Tekan Enter untuk kembali...")


def proses_pembayaran(nama_pasien):
    os.system("cls")
    tampilkan_header()
    print("\n    --- PEMBAYARAN BIAYA RAWAT INAP ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    index_bayar = -1
    for i in range(len(df_kamar)):
        psn = ambil_nilai_sel(df_kamar, i, "pasien", "-").lower()
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        if psn == nama_pasien.lower() and st == "Dipesan":
            index_bayar = i
            break

    if index_bayar == -1:
        print("    [!] Tidak ada tagihan reservasi yang perlu dibayar.")
        input("\n    Tekan Enter untuk kembali...")
        return

    tgl_masuk_str = ambil_nilai_sel(df_kamar, index_bayar, "tgl masuk", str(datetime.date.today()))
    tgl_keluar_str = ambil_nilai_sel(df_kamar, index_bayar, "tgl keluar", str(datetime.date.today()))
    masuk = datetime.datetime.strptime(tgl_masuk_str, "%Y-%m-%d").date()
    keluar = datetime.datetime.strptime(tgl_keluar_str, "%Y-%m-%d").date()
    lama = (keluar - masuk).days
    if lama < 1:
        lama = 1

    tarif_str = ambil_nilai_sel(df_kamar, index_bayar, "tarif per hari", "0")
    tarif = int(tarif_str) if tarif_str.isdigit() else 0
    total = tarif * lama

    no_kamar = ambil_nilai_sel(df_kamar, index_bayar, "nomor kamar", "-")
    tipe_kamar = ambil_nilai_sel(df_kamar, index_bayar, "tipe kamar", "-")

    print(f"    Nomor Kamar     : {no_kamar} ({tipe_kamar})")
    print(f"    Lama Rawat      : {lama} hari x Rp {tarif:,}".replace(",", "."))
    print(f"    Total Tagihan   : Rp {total:,}".replace(",", "."))
    print("    " + "-" * 45)
    print(f"    Rekening Tujuan : {rekening_rs} (a.n. {nama_rs})")
    print("    " + "-" * 45)

    while True:
        teks_bayar = input("    Masukkan nominal transfer (0 = batal): ").strip().lower().replace("rp", "").replace(".", "").replace(",", "")
        if teks_bayar == "0":
            return
        if teks_bayar.isdigit() and int(teks_bayar) > 0:
            uang_bayar = int(teks_bayar)
            break
        print("    [!] Masukkan nominal angka yang valid.")

    if uang_bayar < total:
        kurang = total - uang_bayar
        print(f"\n    [!] Pembayaran tidak dapat diproses, nominal kurang Rp {kurang:,}.".replace(",", "."))
    else:
        df_kamar.loc[index_bayar, "status"] = "Terisi"
        df_kamar.to_csv(file_kamar, index=False)

        df_riwayat_rawat = pd.read_csv(file_riwayat_rawat, dtype=str)
        baris_riw = len(df_riwayat_rawat)
        df_riwayat_rawat.loc[baris_riw, "tanggal proses"] = str(datetime.date.today())
        df_riwayat_rawat.loc[baris_riw, "jenis transaksi"] = "Pembayaran Reservasi"
        df_riwayat_rawat.loc[baris_riw, "nomor kamar"] = no_kamar
        df_riwayat_rawat.loc[baris_riw, "tipe kamar"] = tipe_kamar
        df_riwayat_rawat.loc[baris_riw, "pasien"] = ambil_nilai_sel(df_kamar, index_bayar, "pasien", "-")
        df_riwayat_rawat.loc[baris_riw, "tgl masuk"] = tgl_masuk_str
        df_riwayat_rawat.loc[baris_riw, "tgl keluar"] = tgl_keluar_str
        df_riwayat_rawat.loc[baris_riw, "hari terpakai"] = str(lama)
        df_riwayat_rawat.loc[baris_riw, "total tagihan"] = f"Rp {total:,}".replace(",", ".")
        df_riwayat_rawat.loc[baris_riw, "dana kembali"] = "Rp 0"
        df_riwayat_rawat.loc[baris_riw, "no rekening pasien"] = "-"
        df_riwayat_rawat.to_csv(file_riwayat_rawat, index=False)

        if uang_bayar > total:
            lebih = uang_bayar - total
            print(f"\n    [OK] Pembayaran lunas! Kelebihan transfer Rp {lebih:,} dikembalikan.".replace(",", "."))
        else:
            print(f"\n    [OK] Pembayaran lunas! Kamar {no_kamar} sekarang berstatus Terisi.")

    input("\n    Tekan Enter untuk kembali...")


def perpanjangan_kamar(nama_pasien):
    os.system("cls")
    tampilkan_header()
    print("\n    --- PERPANJANGAN MASA RAWAT INAP ---\n")

    df_kamar = pd.read_csv(file_kamar, dtype=str)
    index_aktif = -1
    for i in range(len(df_kamar)):
        psn = ambil_nilai_sel(df_kamar, i, "pasien", "-").lower()
        st = ambil_nilai_sel(df_kamar, i, "status", "-")
        if psn == nama_pasien.lower() and st == "Terisi":
            index_aktif = i
            break

    if index_aktif == -1:
        print("    [!] Fitur perpanjangan hanya untuk kamar yang sudah lunas (Terisi).")
        input("\n    Tekan Enter untuk kembali...")
        return

    tarif_str = ambil_nilai_sel(df_kamar, index_aktif, "tarif per hari", "0")
    tarif = int(tarif_str) if tarif_str.isdigit() else 0
    no_kamar = ambil_nilai_sel(df_kamar, index_aktif, "nomor kamar", "-")
    tipe_kamar = ambil_nilai_sel(df_kamar, index_aktif, "tipe kamar", "-")
    tgl_keluar_lama = ambil_nilai_sel(df_kamar, index_aktif, "tgl keluar", str(datetime.date.today()))

    print(f"    Nomor Kamar     : {no_kamar} ({tipe_kamar})")
    print(f"    Tarif / Hari    : Rp {tarif:,}".replace(",", "."))
    print(f"    Tgl Keluar Lama : {tgl_keluar_lama}\n")

    while True:
        tambah_teks = input("    Tambah berapa hari rawat inap? (0 = batal): ").strip()
        if tambah_teks == "0":
            return
        if tambah_teks.isdigit() and 1 <= int(tambah_teks) <= 365:
            tambahan_hari = int(tambah_teks)
            break
        print("    [!] Masukkan angka hari antara 1 sampai 365.")

    biaya_tambahan = tarif * tambahan_hari
    tgl_lama = datetime.datetime.strptime(tgl_keluar_lama, "%Y-%m-%d").date()
    tgl_baru = str(tgl_lama + datetime.timedelta(days=tambahan_hari))

    print(f"\n    Biaya Tambahan  : Rp {biaya_tambahan:,}".replace(",", "."))
    print(f"    Tgl Keluar Baru : {tgl_baru}")
    print(f"    Rekening Tujuan : {rekening_rs} (a.n. {nama_rs})")

    while True:
        teks_bayar = input("\n    Masukkan nominal transfer (0 = batal): ").strip().lower().replace("rp", "").replace(".", "").replace(",", "")
        if teks_bayar == "0":
            return
        if teks_bayar.isdigit() and int(teks_bayar) > 0:
            uang_bayar = int(teks_bayar)
            break
        print("    [!] Masukkan nominal angka yang valid.")

    if uang_bayar < biaya_tambahan:
        kurang = biaya_tambahan - uang_bayar
        print(f"\n    [!] Transfer kurang Rp {kurang:,}, perpanjangan dibatalkan.".replace(",", "."))
    else:
        df_kamar.loc[index_aktif, "tgl keluar"] = tgl_baru
        df_kamar.to_csv(file_kamar, index=False)

        df_riwayat_rawat = pd.read_csv(file_riwayat_rawat, dtype=str)
        baris_riw = len(df_riwayat_rawat)
        df_riwayat_rawat.loc[baris_riw, "tanggal proses"] = str(datetime.date.today())
        df_riwayat_rawat.loc[baris_riw, "jenis transaksi"] = "Perpanjangan Kamar"
        df_riwayat_rawat.loc[baris_riw, "nomor kamar"] = no_kamar
        df_riwayat_rawat.loc[baris_riw, "tipe kamar"] = tipe_kamar
        df_riwayat_rawat.loc[baris_riw, "pasien"] = ambil_nilai_sel(df_kamar, index_aktif, "pasien", "-")
        df_riwayat_rawat.loc[baris_riw, "tgl masuk"] = ambil_nilai_sel(df_kamar, index_aktif, "tgl masuk", "-")
        df_riwayat_rawat.loc[baris_riw, "tgl keluar"] = tgl_baru
        df_riwayat_rawat.loc[baris_riw, "hari terpakai"] = str(tambahan_hari)
        df_riwayat_rawat.loc[baris_riw, "total tagihan"] = f"Rp {biaya_tambahan:,}".replace(",", ".")
        df_riwayat_rawat.loc[baris_riw, "dana kembali"] = "Rp 0"
        df_riwayat_rawat.loc[baris_riw, "no rekening pasien"] = "-"
        df_riwayat_rawat.to_csv(file_riwayat_rawat, index=False)

        if uang_bayar > biaya_tambahan:
            lebih = uang_bayar - biaya_tambahan
            lebih_teks = f"Rp {lebih:,}".replace(",", ".")
            print(f"\n    [OK] Perpanjangan berhasil! Tanggal keluar baru: {tgl_baru}.")
            print(f"    [INFO KEMBALIAN] Kembalian sebesar {lebih_teks} sudah dikembalikan.")
        else:
            print(f"\n    [OK] Perpanjangan berhasil! Tanggal keluar baru: {tgl_baru}.")

    input("\n    Tekan Enter untuk kembali...")


# ==========================================
# MENU UTAMA, MENU ADMIN, MENU PASIEN
# ==========================================

def menu_kelola_kamar():
    while True:
        os.system("cls")
        tampilkan_header()
        print("\n    === KELOLA DATA KAMAR RAWAT INAP ===")
        print("    [1] Lihat Data Kamar")
        print("    [2] Tambah Data Kamar")
        print("    [3] Ubah Data Kamar")
        print("    [4] Hapus Data Kamar")
        print("    [0] Kembali")
        pilih = input("\n    Pilih menu (0-4): ").strip()

        if pilih == "1":
            lihat_data_kamar()
        elif pilih == "2":
            tambah_data_kamar()
        elif pilih == "3":
            ubah_data_kamar()
        elif pilih == "4":
            hapus_data_kamar()
        elif pilih == "0":
            break
        else:
            print("\n    [!] Pilihan tidak tersedia.")
            input("\n    Tekan Enter untuk lanjut...")


def menu_kelola_pasien():
    while True:
        os.system("cls")
        tampilkan_header()
        print("\n    === KELOLA DATA PASIEN RAWAT INAP ===")
        print("    [1] Lihat Data Pasien Aktif")
        print("    [2] Ubah Data Pasien")
        print("    [3] Checkout Pasien & Hitung Refund")
        print("    [4] Batalkan Pemesanan Kamar")
        print("    [0] Kembali")
        pilih = input("\n    Pilih menu (0-4): ").strip()

        if pilih == "1":
            lihat_data_pasien()
        elif pilih == "2":
            ubah_data_pasien()
        elif pilih == "3":
            checkout_pasien()
        elif pilih == "4":
            batalkan_pemesanan_kamar()
        elif pilih == "0":
            break
        else:
            print("\n    [!] Pilihan tidak tersedia.")
            input("\n    Tekan Enter untuk lanjut...")


def menu_kelola_rujukan():
    while True:
        os.system("cls")
        tampilkan_header()
        print("\n    === KELOLA DATA SURAT RUJUKAN ===")
        print("    [1] Lihat Data Surat Rujukan")
        print("    [2] Tambah Data Surat Rujukan")
        print("    [3] Ubah Data Surat Rujukan")
        print("    [4] Hapus Data Surat Rujukan")
        print("    [5] Lihat Riwayat Surat Rujukan")
        print("    [0] Kembali")
        pilih = input("\n    Pilih menu (0-5): ").strip()

        if pilih == "1":
            lihat_data_rujukan()
        elif pilih == "2":
            tambah_data_rujukan()
        elif pilih == "3":
            ubah_data_rujukan()
        elif pilih == "4":
            hapus_data_rujukan()
        elif pilih == "5":
            lihat_riwayat_rujukan()
        elif pilih == "0":
            break
        else:
            print("\n    [!] Pilihan tidak tersedia.")
            input("\n    Tekan Enter untuk lanjut...")


def menu_admin(username):
    while True:
        os.system("cls")
        tampilkan_header()
        print(f"\n    === DASHBOARD ADMIN ({username}) ===")
        print("    [1] Kelola Data Kamar Rawat Inap")
        print("    [2] Kelola Data Pasien")
        print("    [3] Kelola Data Surat Rujukan")
        print("    [4] Lihat Riwayat Transaksi & Rawat Inap")
        print("    [0] Logout")
        pilih = input("\n    Pilih menu (0-4): ").strip()

        if pilih == "1":
            menu_kelola_kamar()
        elif pilih == "2":
            menu_kelola_pasien()
        elif pilih == "3":
            menu_kelola_rujukan()
        elif pilih == "4":
            lihat_riwayat_rawat_inap()
        elif pilih == "0":
            break
        else:
            print("\n    [!] Pilihan tidak tersedia.")
            input("\n    Tekan Enter untuk lanjut...")


def menu_pasien(nama_pasien):
    while True:
        os.system("cls")
        tampilkan_header()
        print(f"\n    === DASHBOARD PASIEN ({nama_pasien}) ===")
        print("    [1] Cari & Lihat Kamar Tersedia")
        print("    [2] Reservasi Kamar Rawat Inap")
        print("    [3] Cek Status Reservasi")
        print("    [4] Pembayaran Biaya Rawat Inap")
        print("    [5] Perpanjangan Masa Rawat Inap")
        print("    [0] Logout")
        pilih = input("\n    Pilih menu (0-5): ").strip()

        if pilih == "1":
            cari_data_kamar()
        elif pilih == "2":
            reservasi_kamar(nama_pasien)
        elif pilih == "3":
            cek_status_reservasi(nama_pasien)
        elif pilih == "4":
            proses_pembayaran(nama_pasien)
        elif pilih == "5":
            perpanjangan_kamar(nama_pasien)
        elif pilih == "0":
            break
        else:
            print("\n    [!] Pilihan tidak tersedia.")
            input("\n    Tekan Enter untuk lanjut...")


def main():
    siapkan_file_data()
    while True:
        os.system("cls")
        tampilkan_header()
        print("\n    Selamat datang di Sistem Informasi Rumah Sakit!")
        print("    [1] Login (Admin / Pasien)")
        print("    [2] Registrasi Pasien Baru")
        print("    [0] Keluar Aplikasi")
        pilih = input("\n    Pilih menu (0-2): ").strip()

        if pilih == "1":
            login()
        elif pilih == "2":
            registrasi_pasien()
        elif pilih == "0":
            os.system("cls")
            tampilkan_header()
            print("\n    Terima kasih telah menggunakan layanan rumah sakit kami. Semoga lekas sehat!\n")
            break
        else:
            print("\n    [!] Pilihan tidak tersedia, masukkan 0, 1, atau 2.")
            input("\n    Tekan Enter untuk lanjut...")


main()