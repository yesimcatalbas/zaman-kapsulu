
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

        # Wikipedia'dan o günün ait olduğu ayın tüm olaylarını çekiyoruz
        api_adresi = f"https://api.wikimedia.org/feed/v1/wikipedia/tr/onthisday/all/{ay}/{gun}"
        headers = {'User-Agent': 'ZamanKapsuluUygulamasi/1.0 (iletisim@webkapsulu.com)'}
        
        yanit = requests.get(api_adresi, headers=headers).json()
        olaylar = yanit.get("selected", [])

        olay_listesi = []
        for olay in olaylar:
            olay_yili = olay.get("year")
            metin = olay.get("text")
            
            # KESİN FİLTRE: Sadece kullanıcının seçtiği YILDA olan olayları getir
            if olay_yili == yil and metin:
                olay_listesi.append({
                    "yil": olay_yili,
                    "metin": metin
                })

        # EĞER TAM O YILDA VE GÜNDE BAŞKA OLAY YOKSA:
        # Boş kalmasın diye o yılın o ayında gerçekleşen diğer önemli olayları havuzdan çekip listeliyoruz
        if not olay_listesi:
            for olay in olaylar:
                olay_yili = olay.get("year")
                metin = olay.get("text")
                # Kullanıcının seçtiği yılın yakınlarında o ayda olan olayları topluyoruz
                if olay_yili and (yil - 3 <= olay_yili <= yil + 3) and metin:
                    olay_listesi.append({
                        "yil": olay_yili,
                        "metin": metin
                    })

        return {
            "durum": True,
            "tam_tarih": f"{gun}.{ay}.{yil}",
            "olaylar": olay_listesi[:5] # En fazla 5 tane net olay listelesin
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