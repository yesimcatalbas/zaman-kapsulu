from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime

app = Flask(__name__)

def tarihten_veri_getir(secilen_tarih):
    try:
        tarih_objesi = datetime.strptime(secilen_tarih, "%Y-%m-%d")
        gun = f"{tarih_objesi.day:02d}"
        ay = f"{tarih_objesi.month:02d}"
        yil = tarih_objesi.year

        # Wikipedia Türkçe "Tarihte Bugün" API'si
        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"
        headers = {'User-Agent': 'ZamanKapsuluUygulamasi/1.0 (iletisim@webkapsulu.com)'}
        
        yanit = requests.get(api_adresi, headers=headers).json()
        olaylar = yanit.get("selected", [])

        # O güne ait tüm olayları temiz bir liste haline getiriyoruz
        olay_listesi = []
        for olay in olaylar:
            metin = olay.get("text")
            olay_yili = olay.get("year")
            if metin and olay_yili:
                olay_listesi.append({
                    "yil": olay_yili,
                    "metin": metin
                })

        # Eğer o güne ait hiçbir olay dönmezse boş kalmasın diye önlem
        if not olay_listesi:
            olay_listesi.append({
                "yil": yil,
                "metin": "Bu tarihe ait arşiv kaydı bulunamadı."
            })

        return {
            "durum": True,
            "tam_tarih": f"{gun}.{ay}.{yil}",
            "olaylar": olay_listesi
        }
    except Exception as hata:
        return {
            "durum": False,
            "tam_tarih": secilen_tarih,
            "olaylar": [{"yil": "Hata", "metin": "Arşiv bağlantısında bir sorun oluştu."}]
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