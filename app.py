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

        # Wikipedia API
        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"

        headers = {
            'User-Agent': 'ZamanKapsuluUygulamasi/1.0'
        }

        yanit = requests.get(api_adresi, headers=headers).json()

        # TÜM olayları al
        olaylar = yanit.get("events", [])

        # Sadece girilen yıl ile aynı olan olayları filtrele
        ayni_yil_olaylari = [
            olay for olay in olaylar
            if olay.get("year") == yil
        ]

        # Eğer o yıla ait olay varsa
        if ayni_yil_olaylari:

            secilen_olay = ayni_yil_olaylari[0]

            metin = secilen_olay.get("text", "")
            olay_yili = secilen_olay.get("year", yil)

        else:
            metin = f"{yil} yılı için bu tarihte kayıtlı bir olay bulunamadı."
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