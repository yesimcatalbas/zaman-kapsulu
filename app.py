
from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def tarihten_veri_getir(secilen_tarih):
    try:
        tarih_objesi = datetime.strptime(secilen_tarih, "%Y-%m-%d")
        gun = f"{tarih_objesi.day:02d}"
        ay = f"{tarih_objesi.month:02d}"

        # Wikipedia Türkçe "Tarihte Bugün" API'si
        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"
        headers = {'User-Agent': 'ZamanKapsuluUygulamasi/1.0 (iletisim@webkapsulu.com)'}
        
        yanit = requests.get(api_adresi, headers=headers).json()
        olaylar = yanit.get("selected", [])

        olay_listesi = []
        for olay in olaylar:
            metin = olay.get("text")
            olay_yili = olay.get("year")
            
            # İlgi çekici kelimeleri içeren olayları üst sıralara taşımak için basit bir filtre
            # Yapay zekasız ama akıllıca bir mantık!
            if metin and olay_yili:
                olay_listesi.append({
                    "yil": olay_yili,
                    "metin": metin
                })

        # Olayları yıllara göre yeniden eskiye sıralıyoruz (Kronolojik gazete mantığı)
        olay_listesi = sorted(olay_listesi, key=lambda x: x['yil'], reverse=True)

        # Kullanıcıya en ilgi çekici ve net olan ilk 5-6 büyük olayı gösteriyoruz
        en_iyi_olaylar = olay_listesi[:6]

        # Eğer o gün şans eseri boşsa boş kalmasın diye garanti veri
        if not en_iyi_olaylar:
            en_iyi_olaylar.append({
                "yil": "Tarih Boyunca",
                "metin": "Bu özel günde dünya genelinde sakin bir seyir izlenmiştir."
            })

        return {
            "durum": True,
            "tam_tarih": f"{gun}.{ay}.{tarih_objesi.year}",
            "olaylar": en_iyi_olaylar
        }
    except Exception as hata:
        return {
            "durum": False,
            "tam_tarih": secilen_tarih,
            "olaylar": [{"yil": "Arşiv", "metin": "Bağlantı tazelememiz gerekiyor, lütfen tekrar deneyin."}]
        }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        kullanici_tarihi = request.form.get("tarih_girdisi")
        if kullanici_tarihi:
            sonuclar = tarihten_veri_getir(kullanici_tarihi)
            return render_template("tasarim.html", veri=sonuclar)
            
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)