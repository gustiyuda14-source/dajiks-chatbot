# ============================================================
#   CHATBOT D'AJIKS COFFEE & BILLIARD
#   ⭐⭐⭐⭐⭐ VERSI FINAL PRODUCTION
#   Live Handover + Reservasi Cerdas + Status Buka Otomatis
# ============================================================

import datetime
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

FONNTE_TOKEN = os.environ.get("FONNTE_TOKEN", "BhyKhA1kyYo24FbN4QtA")

# ========================
# VARIABEL D'AJIKS
# ========================

nama_bisnis  = "D'Ajiks Coffee & Billiard"
nomor_bisnis = "0851-2196-0870"
jam_coffee   = "09.10 - 00.00 WITA"
jam_billiard = "10.15 - 02.00 WITA"
harga_siang  = "Rp 25.000/jam (10.00 - 18.00 WITA)"
harga_malam  = "Rp 40.000/jam (18.00 - 02.00 WITA)"

NAMA_ADMIN = ["nesya", "ketut", "yudek", "ara", "gusti", "endi", "arya", "faat"]

daftar_meja = {
    "1": "Meja 1 — Lantai Bawah ✅",
    "2": "Meja 2 — Lantai Bawah ✅",
    "3": "Meja 3 — Lantai Bawah ⚠️ Semi Aktif",
    "4": "Meja 4 — Lantai Atas ✅",
    "5": "Meja 5 — Lantai Atas ✅",
    "6": "Meja 6 — Lantai Atas ✅",
    "7": "Meja 7 — Lantai Atas ✅",
}

mode_manual = {}

# ========================
# KATA KUNCI
# ========================

kata_menu = ["menu","makan","minum","makanan","minuman","kopi","coffee","drink","food","snack","daftar menu","ada apa","ada menu","list menu","mau liat menu","lihat menu","makanannya","minumannya"]
kata_harga = ["harga","price","pricelist","tarif","biaya","berapa","bayar","rate","per jam","jam ini","jam bgini","jam sekarang","skrg","bgini","saat ini","malam ini","siang ini"]
kata_reservasi = ["reservasi","booking","book","pesan meja","reserve","mau main","ingin main","mau booking","mau reservasi","mau pesan meja","ingin booking","mau daftar"]
kata_cek_meja = ["kosong","tersedia","available","ada meja","meja kosong","cek meja","full","penuh","meja ada","ada yang kosong","meja berapa","ada meja kosong","meja masih","meja nya"]
kata_jam = ["jam buka","jam tutup","operasional","buka jam","tutup jam","sudah buka","udah buka","buka gak","buka ga","masih buka","lagi buka","buka belum","sudah tutup","masih tutup","jam operasional","jam berapa buka","open","close","buka kak","buka kakk","udah buka kak","masih buka kak"]
kata_pesan_makan = ["mau pesan","mau order","pesan makanan","pesan minuman","mau makan","mau minum","order makanan","order minuman","pesen","mau pesen","bisa pesan"]
kata_halo = ["halo","hai","hi","hello","selamat","permisi","assalamualaikum","pagi","siang","malam","sore","hei","hey","hallo","hlo","haloo"]
kata_terima_kasih = ["terima kasih","makasih","thanks","thank you","thx","siap kak","oke kak","ok kak","noted","mantap","oke thanks","sip kak","oke siap"]

def cek_kata(pesan, daftar_kata):
    pesan = pesan.lower()
    for kata in daftar_kata:
        if kata in pesan:
            return True
    return False

def cek_status_buka():
    now  = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    jam  = now.hour
    menit = now.minute
    wkt  = jam + menit / 60
    coffee_buka   = wkt >= 9 + 10/60
    billiard_buka = wkt >= 10 + 15/60 or wkt < 2.0
    return coffee_buka, billiard_buka, jam, menit

def cek_pamit_admin(pesan):
    pesan_lower = pesan.lower()
    if "pamit undur diri" in pesan_lower:
        for nama in NAMA_ADMIN:
            if nama in pesan_lower:
                return True, nama.capitalize()
    return False, None

def cek_ada_info_reservasi(pesan):
    pesan_lower = pesan.lower()
    indikator = ["meja","jam","aren","latte","kopi","coffee","americano","pandan","caramel","tiramisu","matcha","chocolate","nasi","ayam","bandeng","bakso","pisang","kentang","risol","vanilla","green","espresso","mochacinno"]
    ada_angka     = any(char.isdigit() for char in pesan)
    ada_indikator = any(k in pesan_lower for k in indikator)
    return ada_angka or ada_indikator

def kirim_pesan(nomor, pesan):
    url     = "https://api.fonnte.com/send"
    headers = {"Authorization": FONNTE_TOKEN}
    data    = {"target": nomor, "message": pesan}
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"✅ Terkirim ke {nomor}: {response.json()}")
    except Exception as e:
        print(f"❌ Gagal kirim: {e}")

def kirim_notif_staff(nomor_customer, pesan_customer):
    notif = (
        "🚨🚨🚨 PERHATIAN STAFF D'AJIKS 🚨🚨🚨\n\n"
        "⚠️ ADA CUSTOMER BUTUH BANTUAN SEGERA!\n\n"
        f"📲 Nomor: {nomor_customer}\n"
        f"💬 Pesan: {pesan_customer}\n\n"
        "🎯 Customer tanya KETERSEDIAAN MEJA!\n\n"
        "👉 Balas langsung ke customer tsb!\n"
        "✅ Setelah selesai ketik:\n"
        "   'Admin [nama] pamit undur diri ya Kak'\n\n"
        "⏰ Mohon fast respon! 🙏"
    )
    kirim_pesan(nomor_bisnis.replace("-", ""), notif)

# ========================
# RESPON
# ========================

def balas_halo():
    return (
        "╔════════════════════════╗\n"
        "  Selamat datang di\n"
        "  D'Ajiks Coffee & Billiard\n"
        "  ☕ & 🎯\n"
        "╚════════════════════════╝\n\n"
        "Halo Kak! Ada yang bisa\n"
        "kami bantu hari ini? 😊\n\n"
        "Ketik salah satu:\n"
        "☕ 'menu'\n"
        "🎯 'harga billiard'\n"
        "📅 'booking meja'\n"
        "🔍 'meja kosong'\n"
        "⏰ 'jam buka'\n"
        "🛎️ 'mau pesan'"
    )

def balas_menu():
    return (
        "╔════════════════════════╗\n"
        "     ☕ MENU D'AJIKS ☕\n"
        "╚════════════════════════╝\n\n"
        "🍽️ MAIN COURSE\n"
        "▸ Nasi Goreng D'Ajiks   Rp 25rb\n"
        "▸ Nasi Goreng Tuna Asap Rp 27rb\n"
        "▸ Bakso Ayam            Rp 27rb\n"
        "▸ Bandeng Crispy        Rp 35rb\n"
        "▸ Nasi Jinggo D'Ajiks   Rp 25rb\n"
        "▸ Ayam Betutu Kampung   Rp 45rb\n"
        "▸ Ayam Betutu Kota      Rp 30rb\n\n"
        "🍟 SNACK\n"
        "▸ Risol Mayo/pcs        Rp  6rb\n"
        "▸ Ubi Goreng            Rp 20rb\n"
        "▸ Pisang Goreng         Rp 20rb\n"
        "▸ Pisang Goreng Kj/Ckt  Rp 25rb\n"
        "▸ Kerupuk Pangsit       Rp 22rb\n"
        "▸ Kentang Goreng        Rp 20rb\n\n"
        "☕ COFFEE\n"
        "▸ Espresso              Rp 15rb\n"
        "▸ Latte hot/cold        25/27rb\n"
        "▸ Manual Brew/V60       30/35rb\n"
        "▸ Mochacinno hot/cold   26/28rb\n"
        "▸ Hot Kopi Susu         Rp 16rb\n"
        "▸ Americano hot/cold    23/25rb\n"
        "▸ Americano Honeyberry  Rp 26rb\n"
        "▸ Americano Segaraning  Rp 26rb\n"
        "▸ Americano Segara Sprk Rp 26rb\n\n"
        "🧊 ICE COFFEE\n"
        "▸ Aren / Pandan         Rp 24/26rb\n"
        "▸ Caramel / Tiramisu    Rp 26rb\n"
        "▸ Vanilla Latte         Rp 26rb\n"
        "▸ Green Banana          Rp 26rb\n\n"
        "🥤 NON COFFEE\n"
        "▸ Chocolate / Red Velvet Rp 23rb\n"
        "▸ Matcha                Rp 25rb\n"
        "▸ Lotus                 Rp 28rb\n"
        "▸ Lychee / Lemon Tea    Rp 20rb\n"
        "▸ Pink Panther          Rp 23rb\n\n"
        "✨ SIGNATURE (semua Rp 28rb)\n"
        "▸ Kintamani Whisper\n"
        "▸ Dewata Goldnut\n"
        "▸ Lost In Lovina\n"
        "▸ Matcha Strawberry Cloud\n"
        "▸ Jembrana Breeze\n"
        "▸ Golden Uluwatu\n\n"
        f"📲 Order: {nomor_bisnis}"
    )

def balas_harga(pesan=""):
    kata_skrg = ["bgini","sekarang","skrg","jam ini","jam sekarang","saat ini","malam ini","siang ini"]
    tanya_skrg = any(k in pesan.lower() for k in kata_skrg)
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    jam = now.hour

    hasil = (
        "╔════════════════════════╗\n"
        "   🎯 TARIF BILLIARD D'AJIKS\n"
        "╚════════════════════════╝\n\n"
        f"🌤️ Siang : {harga_siang}\n"
        f"🌙 Malam : {harga_malam}\n\n"
        "📌 Sistem Open/Loss Time tersedia\n"
        "   (bayar sesuai total jam main)\n"
    )

    if tanya_skrg:
        if 10 <= jam < 18:
            tarif_now = "Rp 25.000/jam 🌤️ (siang)"
        else:
            tarif_now = "Rp 40.000/jam 🌙 (malam)"
        hasil += f"\n💡 Jam {jam:02d}.00 WITA → {tarif_now}\n"

    hasil += f"\n📲 Reservasi: {nomor_bisnis}"
    return hasil

def balas_jam():
    coffee_buka, billiard_buka, jam, menit = cek_status_buka()
    st_coffee   = "🟢 BUKA" if coffee_buka else "🔴 BELUM BUKA"
    st_billiard = "🟢 BUKA" if billiard_buka else "🔴 BELUM BUKA"
    return (
        "╔════════════════════════╗\n"
        "   ⏰ JAM OPERASIONAL D'AJIKS\n"
        "╚════════════════════════╝\n\n"
        f"☕ Coffee   : {jam_coffee}\n"
        f"   Status  : {st_coffee}\n\n"
        f"🎯 Billiard : {jam_billiard}\n"
        f"   Status  : {st_billiard}\n\n"
        f"🕐 Sekarang : {jam:02d}.{menit:02d} WITA\n\n"
        "Buka setiap hari!\n"
        f"Sampai jumpa di {nama_bisnis}! 😊✨"
    )

def balas_cek_meja():
    meja_list = "\n".join([f"▸ {v}" for v in daftar_meja.values()])
    return (
        "╔════════════════════════╗\n"
        "   🎯 KETERSEDIAAN MEJA\n"
        "╚════════════════════════╝\n\n"
        f"{meja_list}\n\n"
        "⏳ Mohon tunggu sebentar Kak!\n"
        "Kami sambungkan ke staff kami\n"
        "untuk info real-time ya! 😊🙏"
    )

def balas_reservasi():
    return (
        "╔════════════════════════╗\n"
        "   📅 RESERVASI MEJA BILLIARD\n"
        "╚════════════════════════╝\n\n"
        "Bisa dibantu Kak untuk list\n"
        "reservasinya dipenuhi sesuai\n"
        "format berikut ya 😊\n\n"
        "👤 Nama      : [nama Kakak]\n"
        "⏰ Jam Main  : [jam mulai]\n"
        "🎯 Meja      : [nomor meja 1-7]\n"
        "☕ Pre-order : [menu / kosongkan]\n\n"
        "Contoh:\n"
        "Gusti\n"
        "19.00\n"
        "Meja 4\n"
        "Aren 1\n\n"
        "📌 Harap hadir 10 menit lebih awal!\n\n"
        "Jika terlambat, 2 opsi:\n"
        "1️⃣ Main sesuai jam reservasi\n"
        "2️⃣ Reservasi hangus → ke customer\n"
        f"   yang hadir lebih awal 🙏\n\n"
        f"📲 Info: {nomor_bisnis}"
    )

def balas_konfirmasi_reservasi(pesan):
    return (
        "╔════════════════════════╗\n"
        "   ✅ RESERVASI TERCATAT!\n"
        "╚════════════════════════╝\n\n"
        "📋 Info yang kami terima:\n\n"
        f"{pesan}\n\n"
        "⏳ Menunggu konfirmasi admin ya Kak!\n\n"
        "📌 Harap hadir 10 menit lebih awal\n"
        "dari waktu reservasi.\n\n"
        "Jika terlambat:\n"
        "1️⃣ Main sesuai jam reservasi\n"
        "2️⃣ Reservasi hangus → ke customer\n"
        f"   yang hadir lebih awal 🙏\n\n"
        f"📲 Konfirmasi: {nomor_bisnis}"
    )

def balas_pesan_makan():
    return (
        "╔════════════════════════╗\n"
        "   🛎️ PESAN MAKAN & MINUM\n"
        "╚════════════════════════╝\n\n"
        "Siap Kak! Hubungi admin kami\n"
        "langsung ya untuk order! 😊\n\n"
        f"📲 WhatsApp: {nomor_bisnis}\n\n"
        "Sebutkan menu dan nomor meja\n"
        "kamu, admin siap membantu! ☕"
    )

def balas_terima_kasih():
    return (
        "😊 Sama-sama Kak!\n"
        "Senang bisa membantu!\n\n"
        f"Sampai jumpa di\n"
        f"{nama_bisnis}! ☕🎯"
    )

def tidak_dikenali():
    return (
        "🤔 Maaf Kak, kami kurang paham.\n\n"
        "Coba ketik:\n"
        "☕ 'menu'\n"
        "🎯 'harga'\n"
        "📅 'booking'\n"
        "🔍 'meja kosong'\n"
        "⏰ 'jam buka'\n"
        "🛎️ 'mau pesan'"
    )

# ========================
# OTAK CHATBOT
# ========================

def proses_pesan(pesan, nomor_pengirim):

    # Cek pamit admin
    is_pamit, nama_admin = cek_pamit_admin(pesan)
    if is_pamit:
        mode_manual[nomor_pengirim] = False
        return pesan  # Pesan pamit diteruskan ke customer

    # Cek /selesai
    if pesan.strip().lower() == "/selesai":
        mode_manual[nomor_pengirim] = False
        return (
            "✅ Terima kasih sudah menghubungi\n"
            f"{nama_bisnis}!\n\n"
            "Jika ada yang ingin ditanyakan\n"
            "lagi, kami siap membantu! 😊☕🎯"
        )

    # Mode manual aktif — chatbot diam
    if mode_manual.get(nomor_pengirim, False):
        return None

    # Proses kata kunci
    if cek_kata(pesan, kata_halo):
        return balas_halo()
    elif cek_kata(pesan, kata_menu):
        return balas_menu()
    elif cek_kata(pesan, kata_harga):
        return balas_harga(pesan)
    elif cek_kata(pesan, kata_jam):
        return balas_jam()
    elif cek_kata(pesan, kata_cek_meja):
        mode_manual[nomor_pengirim] = True
        kirim_notif_staff(nomor_pengirim, pesan)
        return balas_cek_meja()
    elif cek_kata(pesan, kata_reservasi):
        return balas_reservasi()
    elif cek_kata(pesan, kata_pesan_makan):
        return balas_pesan_makan()
    elif cek_kata(pesan, kata_terima_kasih):
        return balas_terima_kasih()
    elif cek_ada_info_reservasi(pesan):
        return balas_konfirmasi_reservasi(pesan)
    else:
        return tidak_dikenali()

# ========================
# WEBHOOK
# ========================

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print(f"\n📩 Data masuk: {data}")

        if data.get("is_from_me") == True:
            return jsonify({"status": "ignored"}), 200
        if data.get("sender") == data.get("device"):
            return jsonify({"status": "ignored"}), 200
        if data.get("message_type") in ["notification", "system"]:
            return jsonify({"status": "ignored"}), 200

        nomor_pengirim = data.get("sender", "")
        pesan_masuk    = data.get("message", "")

        if not nomor_pengirim or not pesan_masuk:
            return jsonify({"status": "ignored"}), 200

        print(f"👤 Dari  : {nomor_pengirim}")
        print(f"💬 Pesan : {pesan_masuk}")

        balasan = proses_pesan(pesan_masuk, nomor_pengirim)

        if balasan is None:
            print("⏸️ Mode manual — chatbot diam")
            return jsonify({"status": "manual_mode"}), 200

        kirim_pesan(nomor_pengirim, balasan)
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error", "detail": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "✅ Chatbot D'Ajiks ONLINE 24 JAM! ☕🎯", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
