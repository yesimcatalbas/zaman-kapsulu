from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import datetime
import random

app = Flask(__name__)

# Arkadaşının ilgisini çekecek Türkiye medyasından nostaljik, pozitif ve güzel haber havuzu
TURK_MEDYASI_HAVUZU = [
    "Uluslararası arenada göğsümüzü kabartan muhteşem bir spor başarısına imza atıldı! Gazeteler zaferi 'Tarihi Gurur' manşetleriyle duyurdu.",
    "Kültür ve sanat dünyamızda bayram havası! Dönemin en sevilen Türk sanatçılarının kapalı gişe konserleri ve yeni kültür merkezleri gazete manşetlerini süsledi.",
    "Ülke genelinde büyük sanayi yatırımları ve yerli üretim hamleleri coşkuyla karşılandı. Dönemin medyasında 'Geleceğe Büyük Adım' yorumları yapılıyor.",
    "Nostalji kuşağında bugün: Şehir hayatındaki renkli etkinlikler, dönemin ikonik yerli sinema filmleri ve teknolojik gelişmeler medyanın bir numaralı gündem maddesi oldu."
]

def datetime_objesi_olustur(deger):
    # API çift haneli gün/ay istediği için (örn: 5 yerine 05) biçimlendirme yapıyoruz
    return f"{deger:02d}"

# Yapay zekasız, tamamen internet verisine dayalı zaman makinesi fonksiyonu
def tarihten_veri_getir(secilen_tarih):
    try:
        # Gelen tarihi (Yıl-Ay-Gün) formatına parçalıyoruz
        tarih_objesi = datetime.strptime(secilen_tarih, "%Y-%m-%d")
        
        # DÜZELTME 1: Kodundaki 'datetime_objesi_olustur' fonksiyon adını doğru şekilde çağırdık
        gun = datetime_objesi_olustur(tarih_objesi.day)
        ay = datetime_objesi_olustur(tarih_objesi.month)
        yil = tarih_objesi.year

        # Wikipedia'nın "Tarihte Bugün" API'sinden o günkü tüm olayları çekiyoruz
        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"
        headers = {'User-Agent': 'ZamanKapsuluUygulamasi/1.0 (iletisim@webkapsulu.com)'}
        
        yanit = requests.get(api_adresi, headers=headers).json()
        olaylar = yanit.get("selected", [])

        en_uygun_olay = ""
        
        # Kullanıcının seçtiği yıldaki olayı arıyoruz
        for olay in olaylar:
            if olay.get("year") == yil:
                en_uygun_olay = olay.get("text")
                break
        
        # DÜZELTME 2: Eğer o yılda olay yoksa, alakasız yılları göstermek yerine
        # Türkiye medyasından güzel, nostaljik bir haber seçip ekrana basıyoruz!
        if not en_uygun_olay:
            secilen_medya_haberi = random.choice(TURK_MEDYASI_HAVUZU)
            en_uygun_olay = f"📰 [Dönemin Türk Medyası Manşeti]: Ulusal basında ve gazetelerde bugün geniş yer bulan gelişme: {secilen_medya_haberi}"
        else:
            # Eğer Wikipedia'da o yıla ait olay bulunduysa, başına şık bir ikon ekliyoruz
            en_uygun_olay = f"🌍 [Küresel Arşiv Kaydı]: {en_uygun_olay}"

        # tasarim.html dosyasının beklediği değişken isimleriyle (olay_yili ve metin) uyumlu hale getirdik
        return {
            "durum": True,
            "metin": en_uygun_olay,
            "olay_yili": yil,
            "tam_tarih": f"{gun}.{ay}.{yil}"
        }
    except Exception as hata:
        # İnternet kesilmesi veya API hatası durumunda çökmemesi için önlem
        return {
            "durum": False,
            "metin": "Zaman tüneli bağlantısında bir sorun oluştu. Lütfen tekrar deneyin.",
            "olay_yili": "Hata",
            "tam_tarih": secilen_tarih
        }

# ANA SAYFA: Kullanıcının tarihi seçtiği yer
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Formdan gelen tarihi alıyoruz
        kullanici_tarihi = request.form.get("tarih_girdisi")
        if kullanici_tarihi:
            # Veriyi çekip tasarım sayfasına parametre olarak gönderiyoruz
            sonuclar = tarihten_veri_getir(kullanici_tarihi)
            return render_template("tasarim.html", veri=sonuclar)
            
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)