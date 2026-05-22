# 📥 Google Drive Relay Downloader

Herhangi bir dosyayı (herhangi bir genel URL'den) indirebilen ve doğrudan **Google Drive**'ınıza kaydedebilen bir masaüstü GUI aracı – bir Google Apps Script'i röle olarak kullanarak.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Apps Script](https://img.shields.io/badge/Google-AppsScript-yellow)

## 📚 Diğer Diller

* [English 🇺🇸](README.md)
* [فارسی 🇮🇷](README_FA.md)
* [Türkçe 🇹🇷](README_TR.md)

---

## ✨ Özellikler

* **Yerel Depolama Bypası:** Dosya doğrudan kaynak URL'den Google Drive'ınıza gider. Hiçbir zaman yerel sabit sürücünüze indirilmez.
* **Basit GUI:** Tkinter ile oluşturulmuş kullanımı kolay bir masaüstü arayüzü.
* **Otomatik Çıkarma:** Özel bir ad sağlanmazsa URL'den dosya adını otomatik olarak çıkarır.
* **Özel Klasörler:** Doğrudan GUI'de farklı Google Drive klasör kimliklerini belirterek indirmelerinizi anında sıralayın.
* **Sessiz Başlatma:** Windows kullanıcıları için uygulamayı yapışkan bir komut istemi penceresi olmadan başlatmak üzere bir VBScript sarmalayıcısı içerir.

---

## 🚀 Nasıl Çalışır

1.  Bir **dosya URL'si** sağlarsınız (örneğin, `https://example.com/file.pdf`).
2.  Python GUI, URL + istenen dosya adını **Google Apps Script web uygulamasına** gönderir.
3.  Apps Script girdileri doğrular, uzak dosyayı getirir ve **Google Drive klasörünüze** kaydeder.
4.  Betik bir başarı yanıtı döndürür ve GUI yeni Drive dosyası URL'sini görüntüler.

---

## 🛠️ Kurulum Talimatları

### 1. Google Apps Script'i Dağıtın

* [script.google.com](https://script.google.com) açın ve yeni bir proje oluşturun.
* Varsayılan kodu [`ScriptToDeploy.gs`](ScriptToDeploy.gs) içeriğiyle değiştirin.
* **Klasör kimliğini** betik içinde değiştirin:  
    `const folderId = 'YOUR_DRIVE_FOLDER_ID';`  
    *(Klasör kimliğinizi Drive URL'sinde bulun: `https://drive.google.com/drive/folders/THIS_IS_THE_ID`)*
* **Web Uygulaması** olarak dağıtın:
    * Şu şekilde yürütün: **Ben**
    * Kimlerin erişimi var: **Herkes** (veya "Bağlantısı olan herkes" – aracın buna erişebilmesi gerekir).
    * **Dağıt** → **Yeni dağıtım** → **Web uygulaması** öğesine tıklayın.  
    * **Dağıtım URL'sini** kopyalayın (`https://script.google.com/macros/s/.../exec` gibi görünür).

### 2. Python Ortamını Yapılandırın

* **Python 3.7+** yüklü olduğundan emin olun.
* Gerekli `requests` kitaplığını yükleyin:  
    ```bash
    pip install requests
    ```
* `relay_config.json` dosyasını düzenleyin ve Apps Script URL'nizi yapıştırın:  
    ```json
    {
      "script_url": "https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec",
      "folder_id": ""
    }
    ```
    *(Alternatif olarak, URL'yi doğrudan GUI'ye girebilir ve "Ayarları Kaydet"e tıklayabilirsiniz).*

---

## 💻 Kullanım

### Uygulamayı Çalıştırma

Uygulamayı başlatmanın iki yolu vardır:
1.  **Standart Başlatma:** Python betiğini doğrudan terminalinizden veya komut isteminden çalıştırın:
    ```bash
    python drive_relay_gui.py
    ```
2.  **Sessiz Başlatma (Yalnızca Windows):** [`launch_gui.vbs`](launch_gui.vbs) dosyasına çift tıklayın. Bu betik, grafik arayüzü bir komut istemi penceresi açmadan arka planda sessizce çalıştırmak için `pythonw` kullanır.

### Arayüzü Kullanma

* **Apps Script URL:** 1. Adımda oluşturduğunuz web uygulaması URL'sini yapıştırın.
* **Drive Klasör Kimliği (İsteğe Bağlı):** Belirli bir dosyayı Apps Script'inizde kodlanmış varsayılan klasörden farklı bir klasöre kaydetmek istiyorsanız, yeni klasör kimliğini buraya yapıştırın.
* **Dosya URL'si:** Dosyaya doğrudan indirme bağlantısı.
* **Farklı Kaydet (İsteğe Bağlı):** Özel bir ad sağlayın (örneğin, `report_2026.pdf`). Boş bırakılırsa, uygulama adı URL'den otomatik olarak algılar.
* **"📥 Drive'a İndir"** öğesine tıklayın.

<img width="933" height="759" alt="image" src="https://github.com/user-attachments/assets/7d1c6ade-18dd-4566-97a0-2860379c2561" />

---

## ⚠️ Sınırlamalar ve Notlar

* **50 MB Dosya Sınırı:** Google Apps Script, blobları getirmek ve işlemek için katı bir bellek sınırı vardır (`UrlFetchApp`). Python GUI, 50 MB'dan büyük bir dosya algılarsa sizi uyarır, çünkü Apps Script büyük olasılıkla bellekten çıkacaktır.
* **Zaman Aşımı:** Apps Script yürütme sınırı 6 dakikadır. Aşırı yavaş kaynak sunucuları, dosya aktarımı tamamlanmadan önce betiğin zaman aşımına uğramasına neden olabilir.
* **Yalnızca Doğrudan Bağlantılar:** Sağlanan URL, doğrudan bir dosya bağlantısı olmalıdır (tarayıcıya yapıştırıldığında hemen indirmedir ve genel olarak erişilebilir olmalıdır. Giriş veya tıklama gerektiren sayfalar desteklenmez.
