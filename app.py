# ============================================================
#   CHATBOT D'AJIKS COFFEE & BILLIARD
#   ⭐⭐⭐⭐⭐ VERSI RAILWAY - PRODUCTION
#   Online 24 jam! Tidak perlu Ngrok!
# ============================================================

import datetime
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ========================
# KONFIGURASI
# Token diambil dari environment variable Railway
# Lebih aman dari hardcode!
# ========================

FONNTE_TOKEN = os.environ.get("FONNTE_TOKEN", "BhyKhA1kyYo24FbN4QtA")

# ========================
# VARIABEL D'AJIKS
# ========================

nama_bisnis     = "D'Ajiks Coffee & Billiard"
nomor_reservasi = "0851-2196-0870"
jam_coffee      = "09.10 AM - 00.00 (tengah malam) WITA"
jam_billiard    = "10.15 AM - 02.00 AM WITA"
harga_siang     = "Rp 25.000/jam (10.00 - 18.00 WITA)"
harga_malam     = "Rp 40.000/jam (18.00 - 02.00 WITA)"

daftar_meja = {
    "1": "Meja 1 - Lantai Bawah ✅ Aktif",
    "2": "Meja 2 - Lantai Bawah ✅ Aktif",
    "3": "Meja 3 - Lantai Bawah ⚠️ Semi Aktif",
    "4": "Meja 4 - Lantai Atas ✅ Aktif",
    "5": "Meja 5 - Lantai Atas ✅ Aktif",
    "6": "Meja 6 - Lantai Atas ✅ Aktif",
    "7": "Meja 7 - Lantai Atas ✅ Aktif",
}

# ========================
# KATA KUNCI
# ========================

kata_menu         = ["menu", "makan", "minum", "makanan", "minuman", "kopi",
                     "coffee", "drink", "food", "snack", "daftar", "ada apa"]
kata_harga        = ["harga", "price", "pricelist", "tarif", "biaya",
                     "berapa", "bayar", "rate", "per jam", "jam ini",
                     "jam bgini", "jam sekarang", "skrg", "sekarang",
                     "bgini", "saat ini", "malam ini", "siang ini"]
kata_reservasi    = ["reservasi", "booking", "book", "pesan meja", "reserve",
                     "mau main", "ingin main"]
kata_cek_meja     = ["kosong", "tersedia", "available", "ada meja",
                     "meja kosong", "cek meja", "full", "penuh"]
kata_jam          = ["jam buka", "jam tutup", "operasional", "buka jam",
                     "tutup jam", "open", "close", "jam berapa buka"]
kata_pesan        = ["order", "mau pesan", "minta", "beli", "pesen",
                     "ingin pesan", "mau order"]
kata_halo         = ["halo", "hai", "hi", "hello", "selamat", "permisi",
                     "assalamualaikum", "pagi", "siang", "malam", "sore"]
kata_terima_kasih = ["terima kasih", "makasih", "thanks", "thank you",
                     "thx", "siap", "oke siap"]

# ========================
# CEK KATA KUNCI
# ========================

def cek_kata(pesan, daftar_kata):
    pesan = pesan.lower()
    for kata in daftar_kata:
        if kata in pesan:
            return True
    return False

# ========================
# RESPON CHATBOT
# ========================

def balas_halo():
    return (
        f"Halo Kak! Selamat datang di {nama_bisnis}! ☕🎱\n\n"
        "Ada yang bisa kami bantu hari ini?\n"
        "Silakan tanya apa saja ya! 😊\n\n"
        "Contoh:\n"
        "💬 'menu'\n"
        "💬 'harga billiard'\n"
        "💬 'mau booking meja'\n"
        "💬 'meja kosong?'\n"
        "💬 'jam buka'"
    )

def balas_menu():
    return (
        "☕ MENU D'AJIKS ☕\n\n"
        "🍽️ MAIN COURSE\n"
        "• Nasi Goreng D'Ajiks — Rp 25.000\n"
        "• Nasi Goreng Tuna Asap — Rp 27.000\n"
        "• Bakso Ayam — Rp 27.000\n"
        "• Bandeng Crispy — Rp 35.000\n"
        "• Nasi Jinggo D'Ajiks — Rp 25.000\n"
        "• Ayam Betutu Kampung — Rp 45.000\n"
        "• Ayam Betutu Kota — Rp 30.000\n\n"
        "🍟 SNACK\n"
        "• Risol Mayo/pcs — Rp 6.000\n"
        "• Ubi Goreng — Rp 20.000\n"
        "• Pisang Goreng — Rp 20.000\n"
        "• Pisang Goreng Keju/Coklat — Rp 25.000\n"
        "• Kerupuk Pangsit — Rp 22.000\n"
        "• Kentang Goreng — Rp 20.000\n\n"
        "☕ COFFEE\n"
        "• Espresso — Rp 15.000\n"
        "• Latte hot/cold — Rp 25.000/27.000\n"
        "• Manual Brew/V60 — Rp 30.000/35.000\n"
        "• Mochacinno hot/cold — Rp 26.000/28.000\n"
        "• Hot Kopi Susu — Rp 16.000\n"
        "• Americano hot/cold — Rp 23.000/25.000\n"
        "• Americano Honeyberry — Rp 26.000\n"
        "• Americano Segaraningberry — Rp 26.000\n"
        "• Americano Segara Spark — Rp 26.000\n\n"
        "🧊 ICE COFFEE\n"
        "• Aren — Rp 24.000\n"
        "• Pandan — Rp 26.000\n"
        "• Caramel — Rp 26.000\n"
        "• Vanilla Latte — Rp 26.000\n"
        "• Tiramisu — Rp 26.000\n"
        "• Green Banana — Rp 26.000\n\n"
        "🥤 NON COFFEE\n"
        "• Chocolate — Rp 23.000\n"
        "• Matcha — Rp 25.000\n"
        "• Red Velvet — Rp 23.000\n"
        "• Lotus — Rp 28.000\n"
        "• Lychee Tea — Rp 20.000\n"
        "• Lemon Tea — Rp 20.000\n"
        "• Pink Panther — Rp 23.000\n\n"
        "✨ SIGNATURE\n"
        "• Kintamani Whisper — Rp 28.000\n"
        "• Dewata Goldnut — Rp 28.000\n"
        "• Lost In Lovina — Rp 28.000\n"
        "• Matcha Strawberry Cloud — Rp 28.000\n"
        "• Jembrana Breeze — Rp 28.000\n"
        "• Golden Uluwatu — Rp 28.000\n\n"
        f"📲 Untuk pesan: {nomor_reservasi}"
    )

def balas_harga(pesan=""):
    kata_sekarang = ["bgini", "sekarang", "skrg", "jam ini",
                     "jam sekarang", "saat ini", "malam ini", "siang ini"]
    tanya_sekarang = any(k in pesan.lower() for k in kata_sekarang)
    jam_sekarang = datetime.datetime.now().hour

    if tanya_sekarang:
        if 10 <= jam_sekarang < 18:
            harga_now = "Rp 25.000/jam (tarif siang) 🌤️"
        else:
            harga_now = "Rp 40.000/jam (tarif malam) 🌙"
        return (
            f"🎱 HARGA MEJA BILLIARD D'AJIKS 🎱\n\n"
            f"🌤️ Siang: {harga_siang}\n"
            f"🌙 Malam: {harga_malam}\n\n"
            f"💡 Jam sekarang ({jam_sekarang:02d}.00 WITA):\n"
            f"Harga berlaku: {harga_now}\n\n"
            "📌 Tersedia sistem Open/Loss Time\n\n"
            f"📲 Reservasi: {nomor_reservasi}"
        )
    return (
        f"🎱 HARGA MEJA BILLIARD D'AJIKS 🎱\n\n"
        f"🌤️ Siang: {harga_siang}\n"
        f"🌙 Malam: {harga_malam}\n\n"
        "📌 Tersedia sistem Open/Loss Time\n\n"
        f"📲 Reservasi: {nomor_reservasi}"
    )

def balas_cek_meja():
    meja_list = "\n".join([f"• Meja {k}: {v}" for k, v in daftar_meja.items()])
    return (
        "🎱 KETERSEDIAAN MEJA D'AJIKS 🎱\n\n"
        f"{meja_list}\n\n"
        "Untuk cek real-time hubungi admin:\n"
        f"📲 {nomor_reservasi}"
    )

def balas_jam():
    return (
        f"⏰ JAM OPERASIONAL D'AJIKS ⏰\n\n"
        f"☕ Coffee   : {jam_coffee}\n"
        f"🎱 Billiard : {jam_billiard}\n\n"
        "Buka setiap hari! Sampai jumpa! 😊✨"
    )

def balas_reservasi():
    return (
        "🎱 RESERVASI MEJA BILLIARD 🎱\n\n"
        "Hubungi admin kami ya Kak! 😊\n\n"
        f"📲 WhatsApp: {nomor_reservasi}\n\n"
        "Sebutkan:\n"
        "• Nama Kakak\n"
        "• Jam main\n"
        "• Pilihan meja (1-7)\n"
        "• Pre-order makanan/minuman\n\n"
        "📌 Mohon hadir 10 menit lebih awal!\n\n"
        "Jika terlambat, kami berikan 2 opsi:\n"
        "1️⃣ Main mulai sesuai jam reservasi\n"
        "2️⃣ Reservasi hangus & diberikan ke\n"
        "   customer yang hadir lebih awal 🙏"
    )

def balas_pesan():
    return (
        "🛎️ PESAN MAKANAN & MINUMAN 🛎️\n\n"
        "Hubungi admin kami ya Kak!\n\n"
        f"📲 WhatsApp: {nomor_reservasi}\n\n"
        "Sebutkan menu dan nomor meja,\n"
        "admin siap membantu! 😊☕"
    )

def balas_terima_kasih():
    return (
        "😊 Sama-sama Kak!\n"
        f"Sampai jumpa di {nama_bisnis}! ☕🎱"
    )

def tidak_dikenali():
    return (
        "🤔 Maaf Kak, kami kurang paham.\n"
        "Coba ketik:\n\n"
        "💬 'menu'\n"
        "💬 'harga'\n"
        "💬 'booking'\n"
        "💬 'meja kosong'\n"
        "💬 'jam buka'\n"
        "💬 'mau pesan'"
    )

# ========================
# OTAK CHATBOT
# ========================

def proses_pesan(pesan):
    if cek_kata(pesan, kata_halo):
        return balas_halo()
    elif cek_kata(pesan, kata_menu):
        return balas_menu()
    elif cek_kata(pesan, kata_harga):
        return balas_harga(pesan)
    elif cek_kata(pesan, kata_reservasi):
        return balas_reservasi()
    elif cek_kata(pesan, kata_cek_meja):
        return balas_cek_meja()
    elif cek_kata(pesan, kata_jam):
        return balas_jam()
    elif cek_kata(pesan, kata_pesan):
        return balas_pesan()
    elif cek_kata(pesan, kata_terima_kasih):
        return balas_terima_kasih()
    else:
        return tidak_dikenali()

# ========================
# KIRIM PESAN VIA FONNTE
# ========================

def kirim_pesan_fonnte(nomor_tujuan, pesan):
    url = "https://api.fonnte.com/send"
    headers = {"Authorization": FONNTE_TOKEN}
    data = {
        "target" : nomor_tujuan,
        "message": pesan,
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        print(f"✅ Pesan terkirim ke {nomor_tujuan}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Gagal kirim pesan: {e}")

# ========================
# WEBHOOK
# ========================

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print(f"\n📩 Data masuk: {data}")

        # FILTER ANTI-LOOP
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

        print(f"👤 Dari: {nomor_pengirim}")
        print(f"💬 Pesan: {pesan_masuk}")

        balasan = proses_pesan(pesan_masuk)
        kirim_pesan_fonnte(nomor_pengirim, balasan)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error"}), 500

@app.route("/", methods=["GET"])
def home():
    return "✅ Chatbot D'Ajiks ONLINE 24 JAM! ☕🎱", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
