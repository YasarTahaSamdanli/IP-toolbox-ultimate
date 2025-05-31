#!/bin/bash

echo ""
echo "[+] Python kütüphaneleri yükleniyor..."
pip install -r requirements.txt

echo ""
echo "[+] Sistem araçları (nmap, whois) yükleniyor..."
if command -v apt &> /dev/null
then
    sudo apt update
    sudo apt install -y nmap whois
elif command -v pacman &> /dev/null
then
    sudo pacman -Sy nmap whois
else
    echo "[!] Paket yöneticisi bulunamadı. Lütfen elle yükleyin: nmap, whois"
fi

echo ""
echo "[✓] Kurulum tamamlandı."
