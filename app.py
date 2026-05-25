from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)

# Yapay zekasız, tamamen internet verisine dayalı zaman makinesi fonksiyonu
def tarihten_veri_getir(secilen_tarih):
    try:
        # Gelen tarihi (Yıl-Ay-Gün) formatına parçalıyoruz
        tarih_objesi = datetime.strptime(secilen_tarih, "%Y-%m-%d")
        gun = datetime_objesi_olustur(tarih_objesi.day)
        ay = datetime_objesi_olustur(tarih_objesi.month)
        yil = tarih_objesi.year

        # Wikipedia'nın "Tarihte Bugün" API'sinden o günkü tüm olayları çekiyoruz
        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"
        headers = {'User-Agent': 'ZamanKapsuluUygulamasi/1.0 (iletisim@webkapsulu.com)'}
        
        yanit = requests.get(api_adresi, headers=headers).json()
        olaylar = yanit.get("selected", [])

        # Kullanıcının seçtiği yıla en yakın veya o yıldaki olayı buluyoruz
        en_uygun_olay = "O tarihte dünya genelinde kayda değer büyük bir olay bulunamadı veya arşivlerde yok."
        
        for olay in olaylar:
            if olay.get("year") == yil:
                en_uygun_olay = olay.get("text")
                break
            # Eğer tam o yıl yoksa, o güne ait popüler ilk olayı seçelim
            elif olaylar:
                en_uygun_olay = olaylar[0].get("text")

        return {
            "durum": True,
            "olay": en_uygun_olay,
            "yil": yil,
            "tam_tarih": f"{gun}.{ay}.{yil}"
        }
    except Exception as hata:
        # İnternet kesilmesi veya API hatası durumunda çökmemesi için önlem
        return {
            "durum": False,
            "olay": "Veriler çekilirken bir hata oluştu. Lütfen tekrar deneyin.",
            "yil": "Bilinmiyor",
            "tam_tarih": secilen_tarih
        }

def datetime_objesi_olustur(deger):
    # API çift haneli gün/ay istediği için (örn: 5 yerine 05) biçimlendirme yapıyoruz
    return f"{deger:02d}"

# ANA SAYFA: Kullanıcının tarihi seçtiği yer
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Formdan gelen tarihi alıyoruz
        kullanici_tarihi = request.form.get("tarih_girdisi")
        if kullanici_tarihi:
            # Veriyi çekip tasarım sayfasına parametre olarak gönderiyoruz
            sonuclar = tarihten_veri_getir(kullanici_tarihi)
            return render_template("tasarim.html", veri=sonuclar)
            
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)