from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def tarihten_veri_getir(secilen_tarih):
    try:
        tarih_objesi = datetime.strptime(secilen_tarih, "%Y-%m-%d")
        gun = f"{tarih_objesi.day:02d}"
        ay = f"{tarih_objesi.month:02d}"
        yil = int(tarih_objesi.year)

        # Wikipedia Türkçe API adresi
        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"
        headers = {
            "User-Agent": "ZamanKapsulu/1.0 (iletisim@zaman-kapsulu.com)"
        }

        yanit = requests.get(api_adresi, headers=headers)
        veri = yanit.json()

        # DÜZELTME 1: Wikipedia API'sinde olaylar anahtarı "events" değil, "selected" olarak döner.
        olaylar = veri.get("selected", [])

        ayni_yil_olaylari = []
        for olay in olaylar:
            olay_yili = olay.get("year")
            
            # DÜZELTME 2: Gelen yıl bilgisi bazen None veya boş olabiliyor, güvenli kontrol ekledik.
            if olay_yili is not None and int(olay_yili) == yil:
                ayni_yil_olaylari.append(olay)

        if ayni_yil_olaylari:
            secilen_olay = ayni_yil_olaylari[0]
            metin = secilen_olay.get("text", "")
            return {
                "durum": True,
                "tam_tarih": f"{gun}.{ay}.{yil}",
                "olay_yili": yil,
                "metin": metin
            }
        else:
            return {
                "durum": False,
                "tam_tarih": f"{gun}.{ay}.{yil}",
                "olay_yili": yil,
                "metin": f"{gun}.{ay}.{yil} tarihinde dünya genelinde resmi olarak kayda geçmiş büyük bir tarihi olay bulunamadı."
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
            sonuc = tarihten_veri_getir(kullanici_tarihi)
            return render_template("tasarim.html", veri=sonuc)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)