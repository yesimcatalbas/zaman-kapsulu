
from flask import Flask, request, render_template
import datetime

app = Flask(__name__)

# Örnek tarihsel olay veritabanı (tarih formatı: "gun.ay.yil")
tarihsel_olaylar = {
    "18.09.2004": [
        {"baslik": "Mars Keşfi", "aciklama": "NASA'nın Mars Rover'ları yüzeyde yeni bulgular elde etti."},
        {"baslik": "Küresel Sanat Günü", "aciklama": "Dünya çapında 50'den fazla ülkede sokak sanatı festivali düzenlendi."},
        {"baslik": "Ticaret Devrimi", "aciklama": "Denizaşırı ticaret filolarında yeni rotalar açıldı."}
    ],
    "15.03.2012": [
        {"baslik": "Bilim İnsanı Ödülü", "aciklama": "CERN'de Higgs bozonu ile ilgili önemli bir adım atıldı."},
        {"baslik": "Siber Güvenlik Zirvesi", "aciklama": "Uluslararası 10 ülke siber saldırılara karşı iş birliği yaptı."}
    ],
    "01.01.2020": [
        {"baslik": "Yeni On Yıl Başlangıcı", "aciklama": "Dünya genelinde büyük kutlamalar yapıldı."},
        {"baslik": "Uzay Turizmi", "aciklama": "İlk ticari uzay aracı test uçuşunu tamamladı."}
    ]
}

def tarihten_veri_getir(secilen_tarih):
    """Seçilen tarihe ait olayları döndürür."""
    # Tarih formatını kontrol et (gg.aa.yyyy)
    try:
        datetime.datetime.strptime(secilen_tarih, "%d.%m.%Y")
    except ValueError:
        return {
            "durum": False,
            "tam_tarih": secilen_tarih,
            "mesaj": "Geçersiz tarih formatı. Lütfen 'gg.aa.yyyy' şeklinde giriniz.",
            "olaylar": []
        }

    if secilen_tarih in tarihsel_olaylar:
        return {
            "durum": True,
            "tam_tarih": secilen_tarih,
            "mesaj": f"{secilen_tarih} tarihinde yaşanan ilgi çekici olaylar:",
            "olaylar": tarihsel_olaylar[secilen_tarih]
        }
    else:
        return {
            "durum": False,
            "tam_tarih": secilen_tarih,
            "mesaj": "Bu tarihe ait kayıtlı bir olay bulunamadı.",
            "olaylar": []
        }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        kullanici_tarihi = request.form.get("tarih_girdisi")
        if kullanici_tarihi:
            sonuclar = tarihten_veri_getir(kullanici_tarihi.strip())
            return render_template("tasarim.html", veri=sonuclar)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)