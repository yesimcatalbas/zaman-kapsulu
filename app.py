from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def tarihten_veri_getir(secilen_tarih):
    try:
        tarih_objesi = datetime.strptime(secilen_tarih, "%Y-%m-%d")
        gun = f"{tarih_objesi.day:02d}"
        ay = f"{tarih_objesi.month:02d}"
        yil = tarih_objesi.year

        # Wikipedia Türkçe Tarihte Bugün API'si
        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"
        headers = {'User-Agent': 'ZamanKapsuluUygulamasi/1.0 (iletisim@zaman-kapsulu.com)'}
        
        yanit = requests.get(api_adresi, headers=headers).json()
        olaylar = yanit.get("selected", [])

        if olaylar:
            # En son gerçekleşen tek bir olayı seçiyoruz
            en_son_olay = olaylar[-1]
            metin = en_son_olay.get("text", "")
            olay_yili = en_son_olay.get("year", yil)
        else:
            metin = "Bu tarihe ait özel bir arşiv kaydı bulunamadı."
            olay_yili = yil

        return {
            "durum": True,
            "tam_tarih": f"{gun}.{ay}.{yil}",
            "olay_yili": olay_yili,
            "metin": metin
        }
    except Exception as hata:
        return {
            "durum": False,
            "tam_tarih": secilen_tarih,
            "olay_yili": "Hata",
            "metin": "Arşiv bağlantısında bir sorun oluştu."
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