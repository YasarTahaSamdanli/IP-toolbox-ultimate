# IP Toolbox Ultimate

🔍 Kapsamlı IP ve Ağ Analiz Aracı

---

## 📦 Uygulama Bilgileri

- **Versiyon:** 1.0  
- **Dil:** Python 3.8+  
- **Geliştirici:** Yasar Taha Samdanli  
- **Lisans:** MIT  

---

## 🌟 Öne Çıkan Özellikler

### 🔧 Entegre Araçlar

#### 🛡️ Nmap Scanner
- SYN / Connect / UDP / NULL Tarama  
- OS ve Servis Versiyon Tespiti  
- Vulnerability Tarama (`--script vuln`)  
- Gelişmiş Seçenekler:  
  - Zamanlama Şablonları: `-T0` ila `-T5`  
  - Decoy IP (`-D`)  
  - MAC Spoofing (`--spoof-mac`)  

#### 🌐 Network Utilities
- ✔ Ping Tool  
- ✔ DNS Lookup  
- ✔ Traceroute  
- ✔ WHOIS Sorgulama  

---

### 🖥️ Kullanıcı Arayüzü

- ✅ Gerçek Zamanlı Sistem Takibi (CPU / RAM / Ağ)  
- ❌ Koyu/Light Mod Desteği (Kaldırıldı ama eklenicek)  
- ✅ Çoklu Sekme Desteği (Nmap / Araçlar / Loglar)

---

## 🛠️ Teknik Detaylar

### 📦 Bağımlılıklar

| Kütüphane  | Versiyon  | Amaç                   |
|------------|-----------|------------------------|
| `psutil`   | 5.9.0+    | Sistem Kaynak İzleme   |
| `tkinter`  | Built-in  | GUI Oluşturma          |

> Diğer tüm modüller Python’un standart kütüphanelerindendir.

---

## ⚙️ Sistem Gereksinimleri

- Python **3.8** veya üzeri  
- **[install.sh](https://github.com/YasarTahaSamdanli/IP-toolbox-ultimate/blob/main/install.sh "install.sh")** kurulu olmalı ki nmap ve whois gibi toollar yüklensin :D  
- **Root yetkisi**, bazı taramalar için gerekli  
  - SYN Scan  
  - OS Detection

---

## 🚀 Kullanım Kılavuzu

### 🔎 Temel Tarama Adımları:

1. Hedef IP gir  
2. Port aralığı belirt *(örn: 80,443 veya 1-1000)*  
3. Tarama türünü seç *(SYN, UDP, vb.)*  
4. `Nmap Tara` butonuna bas

### 🧪 Örnek Nmap Çıktısı:

```text
Starting Nmap 7.92 ( https://nmap.org )
Nmap scan report for example.com (93.184.216.34)
PORT    STATE SERVICE
80/tcp  open  http
443/tcp open  https





## ⚠️ Yasal Uyarı ve Etik Kullanım

**Bu araç yalnızca:**
✅ Kendi sistemlerinizde  
✅ Yazılı izin alınmış hedeflerde  
✅ Etik hacking eğitimleri için  

**Kesinlikle yasak olanlar:**
❌ Yetkisiz sistem taramaları  
❌ Kötü niyetli aktiviteler  
❌ Yasal olmayan testler  

**Önemli Notlar:**
- Nmap ve benzeri tarama araçlarının izinsiz kullanımı **5237 sayılı TCK**'nın 243-245. maddelerine göre suçtur
- Ethical hacking için mutlaka **hedefin yazılı onayını** alın
- Sorumluluk **tamamen kullanıcıya** aittir
