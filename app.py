
from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

def tarihten_veri_getir(secilen_tarih):
    try:
        tarih_objesi = datetime.strptime(secilen_tarih, "%Y-%m-%d")
        gun = f"{tarih_objesi.day:02d}"
        ay = f"{tarih_objesi.month:02d}"
        yil = tarih_objesi.year # Kullanıcının seçtiği net yıl (Örn: 1122)

        # API'den o gün ve aya ait tarih boyu olmuş tüm olayları çekiyoruz
        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"
        headers = {'User-Agent': 'ZamanKapsuluUygulamasi/1.0 (iletisim@webkapsulu.com)'}
        
        yanit = requests.get(api_adresi, headers=headers).json()
        olaylar = yanit.get("selected", [])

        olay_listesi = []
        for olay in olaylar:
            olay_yili = olay.get("year")
            metin = olay.get("text")
            
            # KATI KURAL: Yıl, kullanıcının seçtiği yıla BİREBİR eşit olmak zorunda!
            if olay_yili == yil and metin:
                olay_listesi.append({
                    "yil": olay_yili,
                    "metin": metin
                })

        # Eğer o gün ve o yılda hiçbir olay bulunamadıysa (Alakasız yılları asla gösterme!)
        if not olay_listesi:
            olay_listesi.append({
                "yil": yil,
                "metin": f"Arşiv kayıtlarına göre {gun}.{ay}.{yil} tarihinde dünya genelinde resmi olarak kayda geçmiş büyük bir diplomatik, askeri veya tarihi olay bulunmamaktadır."
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