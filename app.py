
from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime
import random # Rastgele şablonlar seçebilmek için ekledik

app = Flask(__name__)

# Gazete giriş şablonları havuzu
GIRIS_SABLONLARI = [
    "Dönemin ulusal basınında geniş yankı uyandıran gelişmelere göre; {olay}",
    "Günün öne çıkan ve tarih sayfalarında derin izler bırakan o gelişme: {olay}",
    "Tarihin tozlu yapraklarından günümüze ulaşan resmi kayıtlara göre; {olay}",
    "Ajanslarımıza ulaşan son dakika bilgisine göre; dünya genelinde dikkat çeken tarihi olay kayıtlara geçmiştir: {olay}",
    "O dönem basılan gazetelerin manşetlerini süsleyen o tarihi gelişmenin özeti şu şekildedir: {olay}",
    "Yıllar öncesinin bugününde, dünya kamuoyunun gündemine oturan ana gelişme: {olay}"
]

# Rastgele muhabir isimleri havuzu (Nostalji havası için)
MUHABIRLER = ["Ahmet Şen / Ankara", "Selin Yılmaz / Ajanslar", "M. Ali Kaya / Dış Haberler", "Zeynep Demir / Kültür Arşivi"]

def tarihten_veri_getir(secilen_tarih):
    try:
        tarih_objesi = datetime.strptime(secilen_tarih, "%Y-%m-%d")
        gun = f"{tarih_objesi.day:02d}"
        ay = f"{tarih_objesi.month:02d}"
        yil = tarih_objesi.year

        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"
        headers = {'User-Agent': 'ZamanKapsuluUygulamasi/1.0 (iletisim@webkapsulu.com)'}
        
        yanit = requests.get(api_adresi, headers=headers).json()
        olaylar = yanit.get("selected", [])

        en_uygun_olay = "O tarihte dünya genelinde kayda değer büyük bir olay bulunamadı veya arşivlerde yok."
        
        for olay in olaylar:
            if olay.get("year") == yil:
                en_uygun_olay = olay.get("text")
                break
            elif olaylar:
                en_uygun_olay = olaylar[0].get("text")

        # 1. Havuzdan rastgele bir giriş cümlesi seçip içine olayı gömüyoruz
        secilen_sablon = random.choice(GIRIS_SABLONLARI)
        dinamik_alinti = secilen_sablon.format(olay=en_uygun_olay)

        # 2. Rastgele bir muhabir imzası ve rastgele bir arşiv sayı kodu üretiyoruz
        muhabir = random.choice(MUHABIRLER)
        arsiv_kodu = f"Ref-No: {random.randint(1000, 9999)}/{gun}"

        return {
            "durum": True,
            "alinti_metni": dinamik_alinti,
            "muhabir": muhabir,
            "kod": arsiv_kodu,
            "yil": yil,
            "tam_tarih": f"{gun}.{ay}.{yil}"
        }
    except Exception as hata:
        return {
            "durum": False,
            "alinti_metni": "Arşiv bağlantısında bir hata oluştu.",
            "muhabir": "Bilinmiyor",
            "kod": "0000",
            "yil": "Bilinmiyor",
            "tam_tarih": secilen_tarih
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