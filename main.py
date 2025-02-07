from tkinter import *
from yt_dlp import YoutubeDL
from tkinter import messagebox
import subprocess
import os

# requests modülünü yüklemeye çalışıyoruz
try:
    import requests
except ImportError:
    try:
        # Chocolatey'i yüklemek için PowerShell komutu
        os.system("Set-ExecutionPolicy Bypass -Scope Process -Force; "
                  "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; "
                  "iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))")
        subprocess.run('choco install ffmpeg -y', check=True, shell=True)
    except Exception as e:
        # Yükleme hatası durumunda kullanıcıya mesaj verir
        messagebox.showerror("Error", f"An error occurred: {e}")

# Kodun geri kalanı buraya gelir

# Pencere oluştur
pencere = Tk()
pencere.title("YouTube Video İndirici")
pencere.geometry("600x400")
pencere.config(bg="black")

# Başlık etiketi
selam_label = Label(
    pencere, 
    text="Sisteme hoşgeldiniz!", 
    font=("Comic Sans MS", 18), 
    fg="white",
    bg="black"
)
selam_label.pack()

# Video indirme fonksiyonu
def video_indir():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Hata", "Lütfen bir YouTube bağlantısı girin!")
        return

    try:
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",  # En iyi video ve ses formatlarını seç
            "merge_output_format": "mp4",  # Video ve sesi birleştirip MP4 olarak kaydet
            "outtmpl": "%(title)s.%(ext)s",  # Dosya adı: Video başlığı
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",  # FFmpeg ile MP4 formatına dönüştür
            }],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        label_durum.config(text="✅ Video indirildi!", fg="green")
    except Exception as e:
        label_durum.config(text="❌ Video indirilemedi!", fg="red")
        messagebox.showerror("Hata", f"Download Failed!: {e}")

# URL giriş etiketi
url_label = Label(
    pencere, 
    text="YouTube video URL'sini girin:", 
    font=("Arial", 18), 
    fg="white",
    bg="black"
)
url_label.pack()

# URL giriş alanı
url_entry = Entry(pencere, font=("Comic Sans MS", 18), width=34)
url_entry.pack()

# Durum etiketi
label_durum = Label(pencere, font=("Arial", 14), bg="black", fg="white")
label_durum.pack()

# İndirme butonu
indir_buton = Button(
    pencere, 
    text="Video indir", 
    font=("Arial", 18), 
    width=15,
    command=video_indir,
    fg="white",
    bg="red"  # Buton arka plan rengi, yazı rengi
)
indir_buton.pack(pady=50)

pencere.mainloop()