from flask import Flask, request, render_template
import datetime

app = Flask(__name__)

# Gerçekçi ve ilgi çekici tarihsel olay veritabanı
tarihsel_olaylar = {
    "18.09.2004": [
        "NASA'nın Genesis uzay aracı Dünya'ya dönerken paraşütü açılmadı, ancak önemli güneş rüzgarı örnekleri kurtarıldı.",
        "Irak'ta Felluce şehrinde yoğun çatışmalar yaşandı, ABD güçleri şehri kuşattı.",
        "Rusya'da Beslan rehine krizi sonrası güvenlik önlemleri ülke genelinde artırıldı.",
        "İsviçre'de CERN laboratuvarında LHC'nin soğutma testleri başarıyla tamamlandı."
    ],
    "20.07.1969": [
        "Apollo 11 göreviyle Neil Armstrong ve Buzz Aldrin Ay'a ayak bastı.",
        "'İnsanlık için küçük bir adım, insanlık için büyük bir sıçrama' sözü tarihe geçti.",
        "Ay yürüyüşü dünya genelinde 600 milyon kişi tarafından canlı izlendi."
    ],
    "09.11.1989": [
        "Berlin Duvarı yıkıldı, Doğu ve Batı Almanya birleşme sürecine girdi.",
        "Yıkım anında binlerce insan sınır kapılarına akın etti.",
        "Soğuk Savaş'ın simgesel sonu olarak kabul edildi."
    ],
    "11.09.2001": [
        "El-Kaide terör örgütü New York'taki İkiz Kuleler'e saldırı düzenledi.",
        "Pentagon'a da bir uçak çarptı, toplamda yaklaşık 3.000 kişi hayatını kaybetti.",
        "Saldırılar sonrası küresel terörle mücadele konsepti tamamen değişti."
    ],
    "28.06.1914": [
        "Avusturya-Macaristan veliahtı Franz Ferdinand Saraybosna'da suikaste uğradı.",
        "Bu suikast I. Dünya Savaşı'nın tetikleyicisi oldu.",
        "Avrupa'daki ittifak sistemleri bir ay içinde savaşı kaçınılmaz hale getirdi."
    ]
}

def tarihten_veri_getir(secilen_tarih):
    # Tarih formatını kontrol et (gg.aa.yyyy)
    try:
        datetime.datetime.strptime(secilen_tarih, "%d.%m.%Y")
    except ValueError:
        return {
            "durum": False,
            "tam_tarih": secilen_tarih,
            "mesaj": "Geçersiz tarih formatı. Lütfen 'gg.aa.yyyy' şeklinde giriniz. Örnek: 18.09.2004",
            "olaylar": []
        }

    if secilen_tarih in tarihsel_olaylar:
        return {
            "durum": True,
            "tam_tarih": secilen_tarih,
            "mesaj": f"📅 {secilen_tarih} tarihinde yaşanan ilgi çekici olaylar:",
            "olaylar": tarihsel_olaylar[secilen_tarih]
        }
    else:
        return {
            "durum": False,
            "tam_tarih": secilen_tarih,
            "mesaj": f"❌ {secilen_tarih} tarihine ait kayıtlı bir olay bulunamadı. Lütfen başka bir tarih deneyin.",
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