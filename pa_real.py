"""
=====================================================
=                  LIBRARY LIST                     =
=====================================================
"""
import json
import os
import pwinput
import time
from datetime import datetime
from prettytable import PrettyTable



"""
=====================================================
=             VARIABLING JSON FILE                  =
=====================================================
"""
users     = "akun.json"
transaksi = "transaksi.json"
produk_file    = "produk.json"



"""
=====================================================
=             FUNCTION CLEAR SCREEN                 =
=====================================================
"""
def clear_screen():
    if os.name == 'nt':
        os.system('cls')



"""
=====================================================
=                 FUNCTION ENTER                    =
=====================================================
"""
def pause(ent="\nTekan Enter untuk kembali..."):
    input(ent)



"""
=====================================================
=               READ PRODUK.JSON                    =
=====================================================
"""
def Produk_json():
    with open(produk_file, "r") as f:
        produk = json.load(f)
        for i, p in enumerate(produk):
            if "id" not in p:
                p["id"] = i + 1
        return produk



"""
=====================================================
=                  PRODUCT TABLE                    =
=====================================================
"""
def tabel_produk(produk):
    tabel_produk = PrettyTable()
    tabel_produk.field_names = ["No", "Nama Produk", "Harga (Rp)", "Stok"]
    for i, p in enumerate(produk, start=1):
        tabel_produk.add_row([i, p['nama'], f"{p['harga']:,}", p['stok']])
    print(tabel_produk)



"""
=====================================================
=                SAVE PRODUK.JSON                   =
=====================================================
"""
def produk_append(produk):
    with open(produk_file, "w") as f:
        json.dump(produk, f, indent=4)



"""
=====================================================
=             READ TRANSAKSI.JSON                   =
=====================================================
"""
def read_transaksi():
    if not os.path.exists(transaksi):
        save_transaksi([])
        return []
    try:
        with open(transaksi, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("Gagal membaca transaksi.json — memulai riwayat kosong.")
        return []



"""
=====================================================
=                KERANJANG TABLE                    =
=====================================================
"""
def tabel_keranjang(keranjang):
    t = PrettyTable()
    t.field_names = ["No", "Nama Produk", "Harga", "Jumlah", "Subtotal", "Diskon", "Total Bayar"]
    for i, it in enumerate(keranjang, start=1):
        t.add_row([
            i,
            it["nama"],
            f"{it['harga']:,}",
            it["jumlah"],
            f"{it['subtotal']:,}",
            f"{it['diskon']:,}" if it['diskon']>0 else "-",
            f"{it['total_bayar']:,}"
        ])
    print(t)



"""
=====================================================
=              SAVE TRANSAKSI.JSON                  =
=====================================================
"""
def save_transaksi(produk):
    with open(transaksi, "w", encoding="utf-8") as f:
        json.dump(produk, f, indent=4, ensure_ascii=False)



"""
=====================================================
=                 READ AKUN.JSON                    =
=====================================================
"""
def akun_json():
    if os.path.exists(users):
        with open(users, "r") as f:
            return json.load(f)
    return {}



"""
=====================================================
=                 SAVE AKUN.JSON                    =
=====================================================
"""
def akun_append(akun):
    with open(users, 'w') as f:
        json.dump(akun,f, indent=4)



"""
=====================================================
=            FUNCTION SIGN UP PRODUK                =
=====================================================
"""
def sign_up():
    while True:
        clear_screen()
        akun = akun_json()
        username = input("username: ").strip()
        if not username:
            print("Username tidak boleh kosong! ")
            pause()
            return
        if username in akun:
            print("Username sudah ada, silahkan buat akun baru ")
            pause()
            return
        pin = input("pin: ").strip()
        if not pin:
            print("Pin tidak boleh kosong! ")
            pause()
            return
        akun[username] = {
        "pin": pin,
        "role" : "Pelanggan", 
        "balance" : 0
        }
        akun_append(akun)
        print(f"Akun dengan nama {username} berhasil dibuat!")
        pause()
        break



"""
=====================================================
=               FUNCTION ADD PRODUK                 =
=====================================================
"""
def Tambah_produk_admin():
    clear_screen()
    print("Tambah produk baru:")
    produk = Produk_json()
    nama = input("Nama produk: ")
    if not nama:
        print("Nama tidak boleh kosong")
        pause()
        return
    kategori = input("Kategori: ")
    if not kategori:
        print("Kategori tidak boleh kosong")
        pause()
        return
    harga = int(input("Harga (angka): "))
    if not harga:
        print("Harga tidak boleh kosong")
        pause()
        return
    stok = int(input("Stok (angka): "))
    if not stok:
        print("Stok tidak boleh kosong")
        pause()
        return
    tags_input = input("Tags (pisah koma, contoh: hydrating, all): ")
    tags = [tabel.strip().lower() for tabel in tags_input.split(",")] if tags_input else []
    new = {"nama": nama, "kategori": kategori, "harga": harga, "stok": stok, "tags": tags}
    produk.append(new)
    produk_append(produk)
    print(f"\nProduk '{nama}' berhasil ditambahkan")
    pause()



"""
=====================================================
=            FUNCTION UPDATE PRODUK                 =
=====================================================
"""
def Ubah_produk_admin():
    clear_screen()
    produk = Produk_json()
    print("Ubah data produk:")
    tabel_produk(produk)
    id = input("Pilih nomor (No) produk yang ingin diubah: ")
    if not id:
        print("Nomor tidak valid.")
        pause()
        return
    idx = int(id) - 1
    if not (0 <= idx < len(produk)):
        print("Nomor tidak valid.")
        pause()
        return
    p = produk[idx]
    if not p:
        print("Nomor tidak valid.")
        pause()
        return
    print(f"Mengubah produk: {p['nama']} (ID {p['id']}) — kosongkan untuk tidak mengubah")
    nama = input(f"Nama baru [{p['nama']}]: ").strip()
    if not nama:
        print("Nama tidak boleh kosong")
        pause()
        return
    kategori = input(f"Kategori baru [{p.get('kategori','')}]: ").strip()
    if not kategori:
        print("Kategori tidak boleh kosong")
        pause()
        return
    harga = input(f"Harga baru [{p['harga']}]: ").strip()
    if not harga:
        print("Harga tidak boleh kosong")
        pause()
        return
    stok = input(f"Stok baru [{p['stok']}]: ").strip()
    if not stok:
        print("Stok tidak boleh kosong")
        pause()
        return
    tag = input(f"Tags baru (pisah koma) [{', '.join(p.get('tags',[]))}]: ").strip()
    if nama:
        p['nama'] = nama
    if kategori:
        p['kategori'] = kategori
    if harga:
        p['harga'] = int(harga)
    if stok:
        p['stok'] = int(stok)
    if tag:
        p['tags'] = [t.strip().lower() for t in tag.split(",")]
    produk_append(produk)
    print("Data produk berhasil diubah ")
    pause()




"""
=====================================================
=             FUNCTION DELETE PRODUK                =
=====================================================
"""
def Hapus_produk_admin():
    clear_screen()
    produk = Produk_json()
    print("Hapus produk:")
    tabel_produk(produk)
    id = input("Pilih nomor (No) produk yang ingin dihapus: ")
    if not id:
        print("Nomor tidak valid.")
        pause()
        return
    idx = int(id) - 1
    if not (0 <= idx < len(produk)):
        print("Nomor tidak valid.")
        pause()
        return
    confirm = input(f"Yakin hapus '{produk[idx]['nama']}'? (y/n): ").lower()
    if confirm == "y":
        removed = produk.pop(idx)
        produk_append(produk)
        print(f"Produk '{removed['nama']}' dihapus.")
        return
        produk()
    else:
        print("Penghapusan dibatalkan")
        return
        pause()



"""
=====================================================
=             FUNCTION RECOMENDATION                =
=====================================================
"""
def rekomendasi_produk(username):
    clear_screen()
    print("Rekomendasi produk sesuai kondisi kulit")
    jawab = input("Mau dapat rekomendasi produk? (y/n): ").lower()
    if jawab != 'y':
        return
    print("\nPilih jenis kulit:")
    print("1. Berminyak")
    print("2. Kering")
    print("3. Sensitif")
    print("4. Normal")
    print("5. Kombinasi")
    jenis_map = {
        "1": "berminyak",
        "2": "kering",
        "3": "sensitif",
        "4": "normal",
        "5": "kombinasi"
    }
    pilih = input("Masukkan nomor jenis kulit: ").strip()
    jenis = jenis_map.get(pilih)
    if not jenis:
        print("Pilihan tidak valid.")
        return
    # pemetaan kasar tag favorite per jenis kulit
    tag_map = {
        "berminyak": ["oil-control", "acne", "gentle"],
        "kering": ["hydrating", "repair", "natural"],
        "sensitif": ["gentle", "repair", "all"],
        "normal": ["brightening", "hydrating", "all"],
        "kombinasi": ["oil-control", "hydrating", "all"]
    }
    target_tags = tag_map.get(jenis, [])
    data = Produk_json()
    # cari produk yang memiliki salah satu tag target
    hasil = []
    for tag in data:
        p_tags = [t.lower() for t in tag.get("tags",[])]
        if any(tag in p_tags for tag in target_tags) or jenis in (p_tags or []):
            hasil.append(tag)
    clear_screen()
    print(f"Rekomendasi untuk jenis kulit: {jenis}\n")
    if not hasil:
        print("Maaf, tidak ada rekomendasi produk yang cocok berdasarkan database kami.")
        pause()
        return
    # tampilkan tabel rekomendasi
    table = PrettyTable()
    table.field_names = ["No", "Nama Produk", "Kategori", "Harga", "Stok", "Alasan singkat"]
    for i, p in enumerate(hasil, start=1):
        alasan = []
        for t in target_tags:
            if t in [tag.lower() for tag in p.get("tags",[])]: 
                alasan.append(t)
        alasan_txt = ", ".join(alasan) if alasan else "-"
        table.add_row([i, p['nama'], p.get('kategori','-'), f"{p['harga']:,}", p['stok'], alasan_txt])
    print(table)
    pilih_terima = input("\nTerima rekomendasi ini dan lihat penjelasan produk lebih detail? (y/n): ").lower()
    if pilih_terima == 'y':
        # tampilkan penjelasan sederhana per produk
        clear_screen()
        print(f"Penjelasan produk untuk jenis kulit '{jenis}':\n")
        for p in hasil:
            print(f"--- {p['nama']} ---")
            # buat penjelasan sederhana based on tags
            tags = p.get("tags", [])
            explanations = []
            if "hydrating" in tags:
                explanations.append("Melembapkan kulit dan cocok untuk kulit kering.")
            if "oil-control" in tags:
                explanations.append("Mengurangi produksi minyak berlebih; cocok untuk kulit berminyak.")
            if "gentle" in tags:
                explanations.append("Formulasi lembut; cocok untuk kulit sensitif.")
            if "acne" in tags:
                explanations.append("Mengandung bahan untuk membantu mengatasi jerawat.")
            if "brightening" in tags:
                explanations.append("Membantu mencerahkan kulit dan meratakan warna kulit.")
            if "spf" in tags:
                explanations.append("Mengandung proteksi sinar UV. Penting untuk penggunaan siang hari.")
            if not explanations:
                explanations.append("Cocok untuk penggunaan umum / semua jenis kulit.")
            for l in explanations:
                print(f"- {l}")
            print()
        pause()
    else:
        print("Rekomendasi dibatalkan.")
        pause()



"""
=====================================================
=                 SEARCHING HELPER                  =
=====================================================
"""
def search(produk, keyword):
    kw = keyword.lower().strip()
    return [p for p in produk if kw in p["nama"].lower() or kw in p.get("kategori","").lower() or any(kw in tag for tag in p.get("tags",[]))]



"""
=====================================================
=               FUNCTION SEARCHING                  =
=====================================================
"""
def pembeli_search(username):
    clear_screen()
    produk = Produk_json()
    tabel_produk(produk)
    print("Pencarian produk (ketik kata kunci, contoh: 'mask' atau 'ma'):")
    kw = input("Kata kunci: ").strip()
    if not kw:
        print("Kata kunci kosong.")
        pause()
        return
    hasil = search(produk, kw)
    if not hasil:
        print("Tidak ditemukan produk dengan kata kunci tersebut.")
        pause()
        return
    # tampilkan hasil
    clear_screen()
    t = PrettyTable()
    t.field_names = ["ID", "Nama", "Kategori", "Harga", "Stok"]
    for i, p in enumerate(hasil, start=1):
        t.add_row([p.get('id','-'), p['nama'], p.get('kategori','-'), f"{p['harga']:,}", p['stok']])
    print(t)
    pilih = input("\nIngin menambahkan salah satu hasil ke keranjang? (y/n): ").lower()
    if pilih != 'y':
        pause()
        return
    try:
        no = int(input("Pilih nomor (No) produk hasil pencarian: ")) - 1
        if not (0 <= no < len(hasil)):
            print("Nomor tidak valid.")
            pause()
            return
        # find original index in data to check stok properly
        prod_name = hasil[no]['nama']
        original = next((p for p in produk if p['nama'] == prod_name), None)
        if not original:
            print("Produk tidak ditemukan di database (konflik).")
            pause()
            return
        jumlah = int(input(f"Masukkan jumlah {original['nama']}: "))
        if jumlah <= 0:
            print("Jumlah harus > 0.")
            pause()
            return
        if jumlah > original['stok']:
            print("Stok tidak mencukupi.")
            pause()
            return
        subtotal = original['harga'] * jumlah
        diskon = 0
        if subtotal >= 500000:
            diskon = int(subtotal * 0.15)
        elif subtotal >= 300000:
            diskon = int(subtotal * 0.1)
        total_bayar = subtotal - diskon
        # add to cart
        found = next((it for it in KERANJANG if it['nama'] == original['nama']), None)
        if found:
            found['jumlah'] += jumlah
            found['subtotal'] += subtotal
            found['diskon'] += diskon
            found['total_bayar'] += total_bayar
        else:
            KERANJANG.append({
                "nama": original['nama'],
                "harga": original['harga'],
                "jumlah": jumlah,
                "subtotal": subtotal,
                "diskon": diskon,
                "total_bayar": total_bayar
            })
        print(f"\n{original['nama']} berhasil ditambahkan ke keranjang.")
    except ValueError:
        print("Input tidak valid.")
    pause()



"""
=====================================================
=                FUNCTION INVOICE                   =
=====================================================
"""
def pembeli_view_invoice(username):
    clear_screen()
    print("==============================================================")
    print("=                           INVOICE                          =")
    print("==============================================================")
    transaksi = read_transaksi()
    user_tr = [t for t in transaksi if t.get("pembeli") == username]
    if not user_tr:
        print("==============================================================")
        print("=                 Belum ada riwayat pembelian.               =")
        print("==============================================================")
        pause()
        return
    for idx, trx in enumerate(user_tr, start=1):
        print(f"--- Transaksi #{idx} | Waktu: {trx.get('waktu')} ---")
        t = PrettyTable()
        t.field_names = ["No", "Nama Produk", "Jumlah", "Total Bayar (Rp)"]
        for i, it in enumerate(trx.get("items",[]), start=1):
            t.add_row([i, it['nama'], it['jumlah'], f"{it['total_bayar']:,}"])
        print(t)
        print(f"Total transaksi: Rp{trx.get('total'):,}\n")
    print("==============================================================")
    print("=                 TERIMAKASIH SUDAH MEMBELI                  =")
    print("==============================================================")
    pause()



"""
=====================================================
=        FUNCTION ADD ITEMS TO KERANJANG            =
=====================================================
"""
KERANJANG = []
def pembeli_add_to_cart(username):
    clear_screen()
    produk = Produk_json()
    print("Tambah barang ke keranjang:")
    tabel_produk(produk)
    try:
        searching = input("Search?(y/n): ")
        if searching == "y":
            print("tabel_produk")
            pembeli_search(username)
        else:
            no = int(input("Pilih nomor produk (No): ")) - 1
            if not (0 <= no < len(produk)):
                print("Nomor tidak valid.")
                return
            prod = produk[no]
            jumlah = int(input(f"Masukkan jumlah {prod['nama']}: "))
            if jumlah <= 0:
                print("Jumlah tidak boleh minus")
                return
            if jumlah > prod['stok']:
                print("Stok tidak mencukupi")
                return
            subtotal = prod['harga'] * jumlah
            diskon = 0
            if subtotal >= 500000:
                diskon = int(subtotal * 0.15)
            elif subtotal >= 300000:
                diskon = int(subtotal * 0.1)
            total_bayar = subtotal - diskon
            # tambahkan ke keranjang (gabungan item sama -> jumlah bertambah)
            found = next((it for it in KERANJANG if it['nama'] == prod['nama']), None)
            if found:
                found['jumlah'] += jumlah
                found['subtotal'] += subtotal
                found['diskon'] = int(found['diskon'] + diskon)
                found['total_bayar'] = int(found['total_bayar'] + total_bayar)
            else:
                KERANJANG.append({
                    "pembeli": prod['nama'],
                    "harga": prod['harga'],
                    "jumlah": jumlah,
                    "subtotal": subtotal,
                    "diskon": diskon,
                    "total_bayar": total_bayar
            })
            print(f"\n{prod['nama']} berhasil ditambahkan ke keranjang.")
            pause()
    except ValueError:
        print("Input tidak valid (harus angka).")



"""
=====================================================
=               FUNCTION CART ACCESS                =
=====================================================
"""
def pembeli_view_cart_and_checkout(username):
    clear_screen()
    akun = akun_json()
    price = akun[username]["balance"]
    pin = akun[username]['pin']
    admin_money = akun["admin"]["balance"]    
    pin_admin = akun["admin"]['pin']
    produk = Produk_json()
    print(f"Keranjang belanja ({users})")
    print(price)
    if not KERANJANG:
        print("Keranjang masih kosong.")
        pause()
        return
    tabel_keranjang(KERANJANG)
    total_semua = sum(it['total_bayar'] for it in KERANJANG)
    print(f"\nTotal keseluruhan: Rp{total_semua:,}")
    pilih = input("\nCheckout sekarang dan simpan transaksi? (y/n): ").lower()
    if pilih != 'y':
        print("Checkout dibatalkan.")
        print(price)
        pause()
        return
    # lakukan update stok & simpan transaksi
    for it in KERANJANG:
        if it['total_bayar'] < price :
            price -= it['total_bayar']
            akun[username] = {
            "pin": pin,
            "role" : "Pelanggan", 
            "balance" : price
            }
            akun_append(akun)
            admin_money += it['total_bayar']
            akun['admin'] = {
            "pin": pin_admin,
            "role" : "admin", 
            "balance" : admin_money
            }
            akun_append(akun)
        else:
            print("Balance tidak cukup!")
            pause()
            return
        # find product by name (names assumed unique)
        prod = next((p for p in produk if p['nama'] == it['nama']), None)
        if prod:
            if it['jumlah'] > prod['stok']:
                print(f"Stok tidak cukup untuk {it['nama']}. Checkout dibatalkan.")
                pause()
                return
            prod['stok'] -= it['jumlah']
        produk_append(produk)
    transaksi = read_transaksi()
    transaksi.append({
        "nama" : username,
        "role" : 'pembeli',
        "waktu": datetime.now().isoformat(),
        "items": KERANJANG.copy(),
        "total": int(total_semua)
    })
    save_transaksi(transaksi)
    KERANJANG.clear()
    print("\nCheckout berhasil. Transaksi tersimpan di riwayat.")
    print(price)
    pause()



"""
=====================================================
=                FUNCTION TOP UP                    =
=====================================================
"""
def top_up(username):
    clear_screen()
    akun = akun_json()
    price = akun[username]['balance']
    pin = akun[username]['pin']
    admin_money = akun["admin"]['balance']
    pin_admin = akun["admin"]['pin']
    jumlah = int(input("Jumlah top up: "))
    if jumlah >= 2000:
        print(f"Topup uang ke E-money sebesar Rp{jumlah}")
        print("Rp1000 akan diambil dari jumlah topup sebagai biaya administrasi")
        pause()
        sisa = jumlah - 1000
        admin_total = admin_money + 1000
        total = price + sisa
        akun['admin'] = {
        "pin": pin_admin,
        "role" : "admin", 
        "balance" : admin_total
        }
        akun_append(akun)
        akun[username] = {
        "pin": pin,
        "role" : "Pelanggan", 
        "balance" : total
        }
        akun_append(akun)
    elif jumlah < 2000:
        print("Minimal top up adalah Rp2000")
        pause()
        return



"""
=====================================================
=              FUNCTION MENU ADMIN                  =
=====================================================
"""
def menu_admin(username):
    while True:
        clear_screen()
        produk = Produk_json()
        tabel_produk(produk)
        print(f"--- MENU ADMIN ({username}) ---")
        print("1. Tambah Produk")
        print("2. Ubah Produk")
        print("3. Hapus Produk")
        print("4. Kembali / Logout")
        Pilihan = input("Pilih: ")
        if Pilihan == "1":
            Tambah_produk_admin()
        elif Pilihan == "2":
            Ubah_produk_admin()
        elif Pilihan == "3":
            Hapus_produk_admin()
        elif Pilihan == "4":
            pause()
            clear_screen()
            break
        else:
            print("Pilihan tidak valid.")
            pause()



"""
=====================================================
=               FUNCTION MENU PEMBELI               =
=====================================================
"""
def menu_pembeli(username):
    while True:
        clear_screen()
        print(f"--- MENU PEMBELI ({username}) ---")
        print("1. Lihat & Pesan Produk")
        print("2. Rekomendasi Produk")
        print("3. Lihat Keranjang & Checkout")
        print("4. Invoice")
        print("5. Topup")
        print("6. Logout")
        Pilihan = input("Pilih: ").strip()
        if Pilihan == "1":
            pembeli_add_to_cart(username);pause
        elif Pilihan == "2":
            rekomendasi_produk(username)
        elif Pilihan == "3":
            pembeli_view_cart_and_checkout(username)
        elif Pilihan == "4":
            pembeli_view_invoice(username)
        elif Pilihan == "5":
            top_up(username)
        elif Pilihan == "6":
            clear_screen()
            break
        else:
            print("Pilihan tidak valid."); pause()



"""
=====================================================
=                    MENU LOGIN                     =
=====================================================
"""
def main():
    clear_screen()
    Produk_json()
    akun = akun_json()
    try:
        while True:
            print("=== LOGIN ===")
            username = input("Username: ").strip()
            if not username:
                print("Username harus di isi!")
                pause()
                break
            if username not in akun:
                print("Username tidak ditemukan! ")
                pause()
                return
            pin = pwinput.pwinput("Pin: ").strip()
            if not pin:
                print("Pin harus di isi!")
                pause()
                break
            if pin != akun[username]['pin']:
                print("Pin salah! ")
                pause()
                return
            if akun[username]["pin"] == pin:
                print(f"Login berhasil selamat datang {username}")
                print(f"Role: {akun[username]['role']}")
                print(f"Balance: Rp{akun[username]['balance']}")
                pause()
            role = akun[username]['role']
            if role == "admin":
                menu_admin(username)
            else:
                menu_pembeli(username)
                
    except ValueError:
        print ("Input harus angka")



"""
=====================================================
=                     MENU UTAMA                    =
=====================================================
"""
try:
    clear_screen()
    while True:
        print("======= MENU UTAMA =======")
        print("1. Log in")
        print("2. sign up")
        print("3. Out looping")
        perintah = int(input("Masukkan pilihan berdasarkan angka: "))
        if perintah == 1:
            main()
        elif perintah == 2:
            sign_up()
        elif perintah == 3:
            break
        else:
            print("Perintah tidak valid")



#"""
#=====================================================
#=                 ERROR HANDLING                    =
#=====================================================
#"""
except ValueError:
    print ("Input harus angka")
except KeyboardInterrupt:
    print ("Error CTRL + C")
except EOFError: 
    print ("Error CTRL + Z + Enter")