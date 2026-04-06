# ============================================================
#   CHATBOT D'AJIKS COFFEE & BILLIARD
#   ⭐⭐⭐⭐⭐ VERSI FINAL PRODUCTION
#   CS Ramah + Konsep Meja Kosong + Menu Link + Telegram
# ============================================================

import datetime
import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

FONNTE_TOKEN     = os.environ.get("FONNTE_TOKEN", "BhyKhA1kyYo24FbN4QtA")
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "8525358233:AAEisOTrLHjjRpC-5btLlCScPEok31WDoSA")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1210429557")

nama_bisnis  = "D'Ajiks Coffee & Billiard"
nomor_bisnis = "0851-2196-0870"
jam_coffee   = "09.10 - 00.00 WITA"
jam_billiard = "10.15 - 02.00 WITA"
harga_siang  = "Rp 25.000/jam (10.00 - 18.00 WITA)"
harga_malam  = "Rp 40.000/jam (18.00 - 02.00 WITA)"

LINK_MENU_MAKANAN   = "https://i.ibb.co/ccr83sLh/IMG-20260406-WA0005.jpg"
LINK_MENU_MINUMAN   = "https://ibb.co/67kPrxF9"
LINK_MENU_SIGNATURE = "https://ibb.co/5h09pngy"

NAMA_ADMIN = ["nesya","ketut","yudek","ara","gusti","endi","arya","faat"]

daftar_meja = {
    1: {"nama": "Meja 1", "lantai": "Bawah", "status": "kosong"},
    2: {"nama": "Meja 2", "lantai": "Bawah", "status": "kosong"},
    3: {"nama": "Meja 3", "lantai": "Bawah", "status": "semi"},
    4: {"nama": "Meja 4", "lantai": "Atas",  "status": "kosong"},
    5: {"nama": "Meja 5", "lantai": "Atas",  "status": "kosong"},
    6: {"nama": "Meja 6", "lantai": "Atas",  "status": "kosong"},
    7: {"nama": "Meja 7", "lantai": "Atas",  "status": "kosong"},
}

mode_manual = {}

# Track customer yang sudah pernah chat
pelanggan_baru = {}

nama_menu_list = [
    "nasi goreng","bakso","bandeng","ayam betutu","nasi jinggo",
    "risol","ubi goreng","pisang goreng","kerupuk","kentang goreng",
    "espresso","latte","manual brew","v60","mochacinno","kopi susu",
    "americano","honeyberry","segaraningberry","segara spark",
    "aren","pandan","caramel","vanilla latte","tiramisu","green banana",
    "chocolate","matcha","red velvet","lotus","lychee","lemon tea","pink panther",
    "kintamani","dewata","lost in lovina","jembrana","golden uluwatu","strawberry cloud",
]

kata_menu = ["menu","makanan","minuman","kopi","coffee","drink","food","snack",
             "daftar menu","ada apa","ada menu","list menu","mau liat menu",
             "lihat menu","makanannya","minumannya","minum apa"]

kata_harga = ["harga","price","pricelist","tarif","biaya","berapa","bayar",
              "rate","per jam","jam ini","jam bgini","jam sekarang","skrg",
              "bgini","saat ini","malam ini","siang ini"]

kata_reservasi = ["reservasi","booking","book","pesan meja","reserve","mau main",
                  "ingin main","mau booking","mau reservasi","mau pesan meja",
                  "ingin booking","mau daftar"]

kata_cek_meja = ["kosong","tersedia","available","ada meja","meja kosong","cek meja",
                 "full","penuh","meja ada","ada yang kosong","meja berapa",
                 "ada meja kosong","meja masih","meja ready","ada meja ready",
                 "meja available"]

kata_jam = ["jam buka","jam tutup","operasional","buka jam","tutup jam","sudah buka",
            "udah buka","buka gak","buka ga","masih buka","lagi buka","buka belum",
            "sudah tutup","masih tutup","jam operasional","jam berapa buka",
            "buka kak","buka kakk","udah buka kak","masih buka kak"]

kata_halo = ["halo","hai","hi","hello","selamat","permisi","assalamualaikum",
             "pagi","siang","malam","sore","hei","hey","hallo","hlo","haloo"]

kata_ada_meja = ["ada kak","ada meja","masih ada","ada kok","ada ko",
                 "tersedia kak","masih kosong","ada kosong","iya ada",
                 "ada 1","ada 2","ada 3","ada 4","ada 5","ada 6","ada 7"]

def cek_kata(pesan, daftar_kata):
    p = pesan.lower()
    for kata in daftar_kata:
        if kata in p:
            return True
    return False

def cek_terima_kasih(pesan):
    p = pesan.lower()
    return "terima" in p and "kasih" in p

def cek_sebut_menu(pesan):
    p = pesan.lower()
    for nama in nama_menu_list:
        if nama in p:
            return True, nama
    return False, None

def cek_pamit_admin(pesan):
    p = pesan.lower()
    if "pamit undur diri" in p:
        for nama in NAMA_ADMIN:
            if nama in p:
                return True, nama.capitalize()
    return False, None

def cek_ada_info_reservasi(pesan):
    p = pesan.lower()
    indikator = ["meja","jam","aren","latte","kopi","coffee","americano","pandan",
                 "caramel","tiramisu","matcha","chocolate","nasi","ayam","bandeng",
                 "bakso","pisang","kentang","risol","vanilla","green","espresso","mochacinno"]
    ada_angka     = any(char.isdigit() for char in pesan)
    ada_indikator = any(k in p for k in indikator)
    return ada_angka or ada_indikator

def cek_konfirmasi_ada_meja(pesan):
    p = pesan.lower()
    return any(k in p for k in kata_ada_meja)

def cek_status_buka():
    now   = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    jam   = now.hour
    menit = now.minute
    wkt   = jam + menit / 60
    coffee_buka   = wkt >= 9 + 10/60
    billiard_buka = wkt >= 10 + 15/60 or wkt < 2.0
    return coffee_buka, billiard_buka, jam, menit

# ========================
# KIRIM PESAN
# ========================

def kirim_wa(nomor, pesan):
    url     = "https://api.fonnte.com/send"
    headers = {"Authorization": FONNTE_TOKEN}
    data    = {"target": nomor, "message": pesan}
    try:
        r = requests.post(url, headers=headers, data=data)
        print(f"✅ WA ke {nomor}: {r.json()}")
    except Exception as e:
        print(f"❌ Gagal WA: {e}")

def kirim_telegram(pesan, reply_markup=None):
    url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": pesan, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        r = requests.post(url, data=data)
        print(f"🔔 Telegram: {r.json()}")
    except Exception as e:
        print(f"❌ Gagal Telegram: {e}")

def kirim_notif_umum(nomor, pesan, kategori):
    now   = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    waktu = f"{now.hour:02d}.{now.minute:02d} WITA"
    kirim_telegram(
        f"🔔 <b>PESAN MASUK D'AJIKS</b>\n\n"
        f"📲 <b>Nomor:</b> {nomor}\n"
        f"💬 <b>Pesan:</b> {pesan}\n"
        f"📌 <b>Kategori:</b> {kategori}\n"
        f"🕐 <b>Waktu:</b> {waktu}"
    )

def kirim_notif_reservasi(nomor, pesan):
    now   = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    waktu = f"{now.hour:02d}.{now.minute:02d} WITA"
    kirim_telegram(
        f"📅 <b>RESERVASI BARU!</b>\n\n"
        f"📲 <b>Nomor:</b> {nomor}\n"
        f"📋 <b>Detail:</b>\n{pesan}\n\n"
        f"🕐 <b>Waktu:</b> {waktu}\n\n"
        f"⚠️ Segera konfirmasi ke customer!"
    )

def kirim_notif_menu(nomor, pesan, nama_menu):
    now   = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    waktu = f"{now.hour:02d}.{now.minute:02d} WITA"
    kirim_telegram(
        f"🛎️ <b>CUSTOMER TANYA MENU SPESIFIK!</b>\n\n"
        f"📲 <b>Nomor:</b> {nomor}\n"
        f"💬 <b>Pesan:</b> {pesan}\n"
        f"🍽️ <b>Menu:</b> {nama_menu}\n"
        f"🕐 <b>Waktu:</b> {waktu}\n\n"
        f"⚡ Chatbot sudah PAUSE!\n"
        f"Balas manual ke customer ya!\n"
        f"Ketik <b>'terima kasih'</b> untuk aktifkan kembali!"
    )

# ========================
# KONSEP MEJA KOSONG
# Dashboard interaktif Telegram
# ========================

def kirim_dashboard_meja(nomor_customer, pesan_customer):
    now   = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    waktu = f"{now.hour:02d}.{now.minute:02d} WITA"

    lantai_bawah = ""
    lantai_atas  = ""

    for num, info in daftar_meja.items():
        if info["status"] == "kosong":
            icon = "🟢"; label = "Kosong"
        elif info["status"] == "terisi":
            icon = "⬛"; label = "Terisi"
        else:
            icon = "⚠️"; label = "Semi Aktif"

        baris = f"{icon} {info['nama']} — {label}\n"
        if info["lantai"] == "Bawah":
            lantai_bawah += baris
        else:
            lantai_atas += baris

    pesan = (
        f"🚨 <b>CUSTOMER TANYA MEJA KOSONG!</b>\n\n"
        f"📲 <b>Nomor:</b> {nomor_customer}\n"
        f"💬 <b>Pesan:</b> {pesan_customer}\n"
        f"🕐 <b>Waktu:</b> {waktu}\n\n"
        f"🎯 <b>STATUS MEJA D'AJIKS:</b>\n\n"
        f"🏢 <b>LANTAI BAWAH</b>\n{lantai_bawah}\n"
        f"🏢 <b>LANTAI ATAS</b>\n{lantai_atas}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👆 Tap meja kosong untuk kirim ke customer!"
    )

    buttons = []
    row = []
    for num, info in daftar_meja.items():
        if info["status"] == "kosong":
            btn = {"text": f"✅ {info['nama']} ({info['lantai']})",
                   "callback_data": f"pilih:{num}:{nomor_customer}"}
        elif info["status"] == "terisi":
            btn = {"text": f"❌ {info['nama']}", "callback_data": "terisi"}
        else:
            btn = {"text": f"⚠️ {info['nama']}", "callback_data": "semi"}

        row.append(btn)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([{
        "text": "😔 Semua Penuh — Beritahu Customer",
        "callback_data": f"penuh:{nomor_customer}"
    }])

    kirim_telegram(pesan, {"inline_keyboard": buttons})

# ========================
# TELEGRAM CALLBACK HANDLER
# Tombol yang ditekan admin
# ========================

@app.route("/telegram_callback", methods=["POST"])
def telegram_callback():
    try:
        data     = request.json
        callback = data.get("callback_query", {})
        cb_data  = callback.get("data", "")
        cb_id    = callback.get("id", "")

        # Jawab callback agar tombol tidak loading
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
            data={"callback_query_id": cb_id}
        )

        # Pilih meja kosong
        if cb_data.startswith("pilih:"):
            _, num_str, nomor_customer = cb_data.split(":")
            num  = int(num_str)
            info = daftar_meja[num]

            pesan_customer = (
                f"Kabar gembira Kak! 🎉\n\n"
                f"✅ <b>{info['nama']}</b> di Lantai {info['lantai']}\n"
                f"saat ini masih <b>KOSONG</b> dan\n"
                f"siap untuk Kakak gunakan! 🎯\n\n"
                f"Mau langsung booking sekarang Kak?\n"
                f"Bisa dibantu isi format reservasi\n"
                f"berikut ya! 😊\n\n"
                f"👤 Nama      : [nama Kakak]\n"
                f"⏰ Jam Main  : [jam mulai]\n"
                f"🎯 Meja      : Meja {num}\n"
                f"☕ Pre-order : [menu / kosongkan]\n\n"
                f"📌 Harap hadir 10 menit lebih awal!\n\n"
                f"Jika terlambat, 2 opsi:\n"
                f"1️⃣ Main sesuai jam reservasi\n"
                f"2️⃣ Reservasi hangus → ke customer\n"
                f"   yang hadir lebih awal 🙏\n\n"
                f"📲 Info: {nomor_bisnis}"
            )

            kirim_wa(nomor_customer, pesan_customer)
            mode_manual[nomor_customer] = False

            kirim_telegram(
                f"✅ Info <b>{info['nama']}</b> sudah terkirim\n"
                f"ke customer {nomor_customer}!\n\n"
                f"🤖 Chatbot customer aktif kembali!"
            )

        # Semua penuh
        elif cb_data.startswith("penuh:"):
            nomor_customer = cb_data.split(":")[1]

            pesan_customer = (
                f"Aduh maaf banget ya Kak 🙏\n\n"
                f"😔 Saat ini semua meja sedang\n"
                f"<b>terisi penuh</b> nih Kak!\n\n"
                f"Tapi jangan khawatir! Kalau ada\n"
                f"meja yang kosong kami akan segera\n"
                f"kabari Kakak ya! 😊\n\n"
                f"Atau Kakak bisa coba datang\n"
                f"langsung ke D'Ajiks —\n"
                f"biasanya ada yang selesai tidak\n"
                f"lama lagi! 🎯\n\n"
                f"📲 Info lebih lanjut: {nomor_bisnis}"
            )

            kirim_wa(nomor_customer, pesan_customer)
            mode_manual[nomor_customer] = False
            kirim_telegram(f"✅ Info penuh sudah terkirim ke {nomor_customer}!")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"❌ Callback error: {e}")
        return jsonify({"status": "error"}), 500

# ========================
# RESPON CS RAMAH
# ========================

def balas_halo():
    return (
        f"Halo Kak! Selamat datang di\n"
        f"{nama_bisnis}! ☕🎯\n\n"
        f"Wah senang banget ada yang\n"
        f"mampir nih! 😊✨\n\n"
        f"Ada yang bisa kami bantu\n"
        f"hari ini Kak?\n\n"
        f"💬 'menu' — lihat menu lengkap\n"
        f"🎯 'harga' — tarif billiard\n"
        f"📅 'booking' — reservasi meja\n"
        f"🔍 'meja kosong' — cek meja\n"
        f"⏰ 'jam buka' — jam operasional\n"
        f"🛎️ 'mau pesan' — order makan/minum"
    )

def balas_menu():
    return (
        f"Tentu Kak! Dengan senang hati\n"
        f"kami tunjukkan menu D'Ajiks! 😊\n\n"
        f"Silakan cek di sini ya Kak —\n\n"
        f"🍽️ Makanan:\n{LINK_MENU_MAKANAN}\n\n"
        f"☕ Minuman:\n{LINK_MENU_MINUMAN}\n\n"
        f"✨ Signature & Lainnya:\n{LINK_MENU_SIGNATURE}\n\n"
        f"Ada yang menarik perhatian\n"
        f"Kakak? 😋 Langsung order ya!\n\n"
        f"📲 {nomor_bisnis}"
    )

def balas_harga(pesan=""):
    kata_skrg  = ["bgini","sekarang","skrg","jam ini","jam sekarang",
                  "saat ini","malam ini","siang ini"]
    tanya_skrg = any(k in pesan.lower() for k in kata_skrg)
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    jam = now.hour

    hasil = (
        f"Boleh Kak! Ini tarif billiard\n"
        f"D'Ajiks ya! 🎯\n\n"
        f"╔════════════════════╗\n"
        f"   💰 TARIF BILLIARD\n"
        f"╚════════════════════╝\n\n"
        f"🌤️ Siang : {harga_siang}\n"
        f"🌙 Malam : {harga_malam}\n\n"
        f"📌 Ada sistem Open/Loss Time ya Kak!\n"
        f"   (bayar sesuai total jam main)\n"
    )

    if tanya_skrg:
        if 10 <= jam < 18:
            tarif_now = f"Rp 25.000/jam 🌤️ (tarif siang)"
        else:
            tarif_now = f"Rp 40.000/jam 🌙 (tarif malam)"
        hasil += f"\n💡 Untuk jam sekarang ({jam:02d}.00 WITA)\n   tarif berlaku: {tarif_now}\n"

    hasil += f"\nMau langsung booking Kak? 😊\n📲 {nomor_bisnis}"
    return hasil

def balas_jam():
    coffee_buka, billiard_buka, jam, menit = cek_status_buka()
    st_coffee   = "🟢 SUDAH BUKA" if coffee_buka else "🔴 BELUM BUKA"
    st_billiard = "🟢 SUDAH BUKA" if billiard_buka else "🔴 BELUM BUKA"
    return (
        f"Siap Kak! Ini jam operasional\n"
        f"D'Ajiks ya! ⏰\n\n"
        f"☕ Coffee   : {jam_coffee}\n"
        f"   Status  : {st_coffee}\n\n"
        f"🎯 Billiard : {jam_billiard}\n"
        f"   Status  : {st_billiard}\n\n"
        f"🕐 Sekarang : {jam:02d}.{menit:02d} WITA\n\n"
        f"Kami buka setiap hari Kak!\n"
        f"Ditunggu kedatangannya ya! 😊✨"
    )

def balas_cek_meja():
    lantai_bawah = ""
    lantai_atas  = ""
    for num, info in daftar_meja.items():
        if info["status"] == "kosong":
            icon = "🟢"; label = "Kosong"
        elif info["status"] == "terisi":
            icon = "⬛"; label = "Terisi"
        else:
            icon = "⚠️"; label = "Semi Aktif"
        baris = f"{icon} {info['nama']} — {label}\n"
        if info["lantai"] == "Bawah":
            lantai_bawah += baris
        else:
            lantai_atas += baris

    return (
        f"Sebentar ya Kak! Kami cekkan\n"
        f"dulu status mejanya! 😊\n\n"
        f"🏢 Lantai Bawah:\n{lantai_bawah}\n"
        f"🏢 Lantai Atas:\n{lantai_atas}\n"
        f"Staff kami akan segera konfirmasi\n"
        f"ketersediaan real-time nya ya Kak!\n\n"
        f"Mohon tunggu sebentar! 🙏"
    )

def balas_reservasi():
    return (
        f"Wah mau booking meja? Seru nih! 🎯\n\n"
        f"Bisa dibantu Kak untuk isi\n"
        f"format reservasi berikut ya! 😊\n\n"
        f"👤 Nama      : [nama Kakak]\n"
        f"⏰ Jam Main  : [jam mulai]\n"
        f"🎯 Meja      : [nomor meja 1-7]\n"
        f"☕ Pre-order : [menu / kosongkan]\n\n"
        f"Contoh:\n"
        f"Gusti\n"
        f"19.00\n"
        f"Meja 4\n"
        f"Aren 1\n\n"
        f"📌 Mohon hadir 10 menit lebih awal\n"
        f"dari waktu reservasi ya Kak!\n\n"
        f"Jika terlambat, 2 opsi:\n"
        f"1️⃣ Main sesuai jam reservasi\n"
        f"2️⃣ Reservasi hangus → ke customer\n"
        f"   yang hadir lebih awal 🙏\n\n"
        f"📲 Info: {nomor_bisnis}"
    )

def balas_konfirmasi_reservasi(pesan):
    return (
        f"Siap Kak! Reservasi sudah kami\n"
        f"catat ya! ✅\n\n"
        f"📋 Detail yang kami terima:\n\n"
        f"{pesan}\n\n"
        f"⏳ Tim kami akan segera konfirmasi\n"
        f"reservasi Kakak ya! 😊\n\n"
        f"📌 Ingat hadir 10 menit lebih awal\n"
        f"dari waktu reservasi ya Kak!\n\n"
        f"Jika terlambat, 2 opsi:\n"
        f"1️⃣ Main sesuai jam reservasi\n"
        f"2️⃣ Reservasi hangus → ke customer\n"
        f"   yang hadir lebih awal 🙏\n\n"
        f"📲 Konfirmasi: {nomor_bisnis}"
    )

def balas_pesan_makan():
    return (
        f"Wah mau order? Sip Kak! 😋\n\n"
        f"Cek dulu menu kami ya Kak —\n\n"
        f"🍽️ Makanan:\n{LINK_MENU_MAKANAN}\n\n"
        f"☕ Minuman:\n{LINK_MENU_MINUMAN}\n\n"
        f"✨ Signature:\n{LINK_MENU_SIGNATURE}\n\n"
        f"Setelah pilih menu, hubungi\n"
        f"admin kami langsung ya Kak!\n\n"
        f"📲 {nomor_bisnis}\n\n"
        f"Sebutkan menu dan nomor meja,\n"
        f"admin siap membantu! 😊☕"
    )

def balas_terima_kasih():
    return (
        f"Sama-sama Kak! 😊\n"
        f"Senang bisa membantu!\n\n"
        f"Sampai jumpa dan selamat\n"
        f"menikmati di {nama_bisnis}!\n"
        f"☕🎯✨"
    )

def tidak_dikenali():
    return (
        f"Maaf Kak, kami kurang paham\n"
        f"maksudnya nih 🙏\n\n"
        f"Bisa coba ketik salah satu\n"
        f"ini ya Kak —\n\n"
        f"💬 'menu'\n"
        f"🎯 'harga billiard'\n"
        f"📅 'booking meja'\n"
        f"🔍 'meja kosong'\n"
        f"⏰ 'jam buka'\n"
        f"🛎️ 'mau pesan'"
    )

# ========================
# OTAK CHATBOT
# ========================

def proses_pesan(pesan, nomor):

    # Cek apakah ini pesan pertama dari nomor ini
    adalah_pesan_pertama = nomor not in pelanggan_baru

    # Cek pamit admin → aktifkan chatbot
    is_pamit, nama_admin = cek_pamit_admin(pesan)
    if is_pamit:
        mode_manual[nomor] = False
        return pesan

    # Cek terima kasih → aktifkan chatbot
    if cek_terima_kasih(pesan):
        if mode_manual.get(nomor, False):
            mode_manual[nomor] = False
            kirim_notif_umum(nomor, pesan, "✅ Sesi Selesai - Chatbot Aktif")
            return balas_terima_kasih()
        else:
            kirim_notif_umum(nomor, pesan, "😊 Terima Kasih")
            return balas_terima_kasih()

    # Cek konfirmasi ada meja dari staff → aktifkan + arahkan reservasi
    if mode_manual.get(nomor, False) and cek_konfirmasi_ada_meja(pesan):
        mode_manual[nomor] = False
        return (
            f"Alhamdulillah masih ada Kak! 🎉😊\n\n"
            f"Mau langsung booking sekarang?\n"
            f"Bisa dibantu isi format reservasi\n"
            f"berikut ya Kak!\n\n"
            f"👤 Nama      : [nama Kakak]\n"
            f"⏰ Jam Main  : [jam mulai]\n"
            f"🎯 Meja      : [nomor meja 1-7]\n"
            f"☕ Pre-order : [menu / kosongkan]\n\n"
            f"📌 Mohon hadir 10 menit lebih awal!\n\n"
            f"Jika terlambat, 2 opsi:\n"
            f"1️⃣ Main sesuai jam reservasi\n"
            f"2️⃣ Reservasi hangus → ke customer\n"
            f"   yang hadir lebih awal 🙏\n\n"
            f"📲 Info: {nomor_bisnis}"
        )

    # Mode manual aktif — chatbot diam tapi tetap monitor
    if mode_manual.get(nomor, False):
        kirim_notif_umum(nomor, pesan, "💬 Mode Staff Aktif")
        return None

    # Proses normal
    if cek_kata(pesan, kata_halo):
        kirim_notif_umum(nomor, pesan, "👋 Halo")
        return balas_halo()

    elif cek_kata(pesan, kata_menu):
        kirim_notif_umum(nomor, pesan, "☕ Tanya Menu")
        return balas_menu()

    elif cek_kata(pesan, kata_harga):
        kirim_notif_umum(nomor, pesan, "🎯 Tanya Harga")
        return balas_harga(pesan)

    elif cek_kata(pesan, kata_jam):
        kirim_notif_umum(nomor, pesan, "⏰ Tanya Jam Buka")
        return balas_jam()

    elif cek_kata(pesan, kata_cek_meja):
        mode_manual[nomor] = True
        kirim_dashboard_meja(nomor, pesan)
        return balas_cek_meja()

    elif cek_kata(pesan, kata_reservasi):
        kirim_notif_umum(nomor, pesan, "📅 Minta Reservasi")
        return balas_reservasi()

    elif cek_kata(pesan, ["mau pesan","mau order","pesan makanan","pesan minuman",
                           "mau makan","mau minum","order","pesen"]):
        kirim_notif_umum(nomor, pesan, "🛎️ Mau Pesan")
        return balas_pesan_makan()

    # Cek sebut nama menu spesifik → alert admin
    else:
        ada_menu, nama_menu = cek_sebut_menu(pesan)
        if ada_menu:
            mode_manual[nomor] = True
            kirim_notif_menu(nomor, pesan, nama_menu)
            return (
                f"Wah Kakak tertarik dengan\n"
                f"{nama_menu.title()}! 😋\n\n"
                f"Sebentar ya Kak, kami sambungkan\n"
                f"ke staff kami untuk info lengkap\n"
                f"dan ketersediaannya! 😊🙏"
            )

        elif cek_ada_info_reservasi(pesan):
            kirim_notif_reservasi(nomor, pesan)
            return balas_konfirmasi_reservasi(pesan)

        else:
            kirim_notif_umum(nomor, pesan, "❓ Tidak Dikenali")
            return tidak_dikenali()

# ========================
# WEBHOOK FONNTE
# ========================

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.json
        print(f"\n📩 Data: {data}")

        if data.get("is_from_me") == True:
            return jsonify({"status": "ignored"}), 200
        if data.get("sender") == data.get("device"):
            return jsonify({"status": "ignored"}), 200
        if data.get("message_type") in ["notification","system"]:
            return jsonify({"status": "ignored"}), 200

        nomor  = data.get("sender", "")
        pesan  = data.get("message", "")

        if not nomor or not pesan:
            return jsonify({"status": "ignored"}), 200

        print(f"👤 {nomor}: {pesan}")

        global pelanggan_baru

        # Kalau pesan pertama — kirim sapaan halo dulu
        if nomor not in pelanggan_baru:
            pelanggan_baru[nomor] = True
            sapaan = (
                f"Halo Kak! Selamat datang di\n"
                f"{nama_bisnis}! ☕🎯\n\n"
                f"Wah senang banget ada yang\n"
                f"mampir nih! 😊✨\n\n"
                f"Ada yang bisa kami bantu\n"
                f"hari ini Kak?\n\n"
                f"💬 'menu' — lihat menu lengkap\n"
                f"🎯 'harga' — tarif billiard\n"
                f"📅 'booking' — reservasi meja\n"
                f"🔍 'meja kosong' — cek meja\n"
                f"⏰ 'jam buka' — jam operasional\n"
                f"🛎️ 'mau pesan' — order makan/minum"
            )
            kirim_wa(nomor, sapaan)

            # Kalau isi pesannya BUKAN sekedar halo
            # langsung proses juga isi pesannya!
            if not cek_kata(pesan, kata_halo):
                import time
                time.sleep(1)  # jeda 1 detik biar tidak overlap
                balasan = proses_pesan(pesan, nomor)
                if balasan:
                    kirim_wa(nomor, balasan)
            return jsonify({"status": "ok"}), 200

        balasan = proses_pesan(pesan, nomor)

        if balasan is None:
            return jsonify({"status": "manual_mode"}), 200

        kirim_wa(nomor, balasan)
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error"}), 500

# ========================
# WEBHOOK TELEGRAM CALLBACK
# ========================

@app.route("/telegram", methods=["POST"])
def telegram_update():
    try:
        data = request.json
        print(f"\n📱 Telegram update: {data}")

        # Handle callback query (tombol ditekan)
        if "callback_query" in data:
            callback = data["callback_query"]
            cb_data  = callback.get("data", "")
            cb_id    = callback.get("id", "")

            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery",
                data={"callback_query_id": cb_id}
            )

            if cb_data.startswith("pilih:"):
                parts          = cb_data.split(":")
                num            = int(parts[1])
                nomor_customer = parts[2]
                info           = daftar_meja[num]

                pesan_wa = (
                    f"Kabar gembira Kak! 🎉\n\n"
                    f"✅ {info['nama']} di Lantai {info['lantai']}\n"
                    f"saat ini masih KOSONG dan\n"
                    f"siap untuk Kakak gunakan! 🎯\n\n"
                    f"Mau langsung booking sekarang Kak?\n"
                    f"Bisa dibantu isi format berikut ya!\n\n"
                    f"👤 Nama      : [nama Kakak]\n"
                    f"⏰ Jam Main  : [jam mulai]\n"
                    f"🎯 Meja      : Meja {num}\n"
                    f"☕ Pre-order : [menu / kosongkan]\n\n"
                    f"📌 Harap hadir 10 menit lebih awal!\n\n"
                    f"Jika terlambat, 2 opsi:\n"
                    f"1️⃣ Main sesuai jam reservasi\n"
                    f"2️⃣ Reservasi hangus → ke customer\n"
                    f"   yang hadir lebih awal 🙏\n\n"
                    f"📲 Info: {nomor_bisnis}"
                )

                kirim_wa(nomor_customer, pesan_wa)
                mode_manual[nomor_customer] = False
                kirim_telegram(
                    f"✅ Info {info['nama']} terkirim ke {nomor_customer}!\n"
                    f"🤖 Chatbot aktif kembali!"
                )

            elif cb_data.startswith("penuh:"):
                nomor_customer = cb_data.split(":")[1]
                pesan_wa = (
                    f"Aduh maaf banget ya Kak 🙏\n\n"
                    f"😔 Saat ini semua meja sedang\n"
                    f"terisi penuh nih Kak!\n\n"
                    f"Tapi jangan khawatir! Kalau ada\n"
                    f"meja kosong kami langsung\n"
                    f"kabari Kakak ya! 😊\n\n"
                    f"Atau Kakak bisa coba datang\n"
                    f"langsung — biasanya ada yang\n"
                    f"selesai tidak lama lagi! 🎯\n\n"
                    f"📲 {nomor_bisnis}"
                )
                kirim_wa(nomor_customer, pesan_wa)
                mode_manual[nomor_customer] = False
                kirim_telegram(f"✅ Info penuh terkirim ke {nomor_customer}!")

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return jsonify({"status": "error"}), 500

@app.route("/", methods=["GET"])
def home():
    return "✅ Chatbot D'Ajiks ONLINE 24 JAM! ☕🎯", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
