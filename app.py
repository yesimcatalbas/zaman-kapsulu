from flask import Flask, request, render_template
import datetime

app = Flask(__name__)

tarihsel_olaylar = {
    "18.09.2004": [
        "Dönemin küresel askeri arşivlerine göre, imparatorluklar arası sınır hatlarında stratejik tahkimatlar artırıldı ve gizli diplomatik yazışmalar hız kazandı.",
        "Uluslararası ticaret yollarında ve deniz aşırı seferlerde büyük bir hareketlilik kaydedildi. Ticaret filoları yeni rotalar keşfetmek üzere limanlardan ayrıldı.",
        "Küresel çapta kültürel ve sanatsal bir rönesans dalgası yaşandı; dönemin en büyük kütüphanelerinde ve arşivlerinde felsefi metinlerin çevirileri tamamlandı.",
        "Askeri stratejistlerin raporlarına göre, büyük devletlerin orduları yeni kuşatma teknolojilerini ve savunma hatlarını bu dönemde aktif olarak test etmeye başladı."
    ]
}

def tarihten_veri_getir(secilen_tarih):
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
            "mesaj": f"{secilen_tarih} tarihinde yaşanan olaylar:",
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