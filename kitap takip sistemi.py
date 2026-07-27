"""
Kitap Takip Sistemi
Okunan kitapları, okunmayan kitapları ve kitap puanlarını takip etmek için basit bir Python programı.
Bu program, kullanıcıların kitap eklemesine, silmesine, durumunu değiştirmesine ve  puan vermesine olanak tanır.

(python3 kitap.py) Terminale bu kodu yazarak çalıştırılabilir. (eğer çalışmıyorasa projenin dosya yolunu kontrol edin.)

İşlevler:
1. Kitapları Listele
2. Yeni Kitap Ekle (boş başlık/yazar kabul etmez)
3. Okundu/Okunmadı İşaretle
4. Kitap Sil
5. Kitap Puanla (1-5 arası puan verilebilir)
6. Çıkış

"""

import json
import os
PROGRAM_KLASORU = os.path.dirname(os.path.abspath(__file__))
DOSYA_YOLU = os.path.join(PROGRAM_KLASORU, "kitaplar.json")
def menü_göster():
    print("\n ***Kitap Takip Sistemi*** ")
    print("\n1. Kitapları Listele")
    print("2. Yeni Bir Kitap Ekle")
    print("3. Kitap Sil")
    print("4. Okundu/Okunmadı Durumunu Değiştir")
    print("5. Kitap Puanla")
    print("6. Çıkış")

def secim_al():
    return input("\n Lütfen bir seçenek giriniz (1-6): ")


def veri_kaydet(kitaplar):
    """Her değişiklikten sonra kitapları json dosyasına kaydeder."""
    try:
        with open(DOSYA_YOLU, "w", encoding="utf-8") as dosya:
            # ensure_ascii=False #Türkçe karakterlerin bozulmasını engeller, kod da hata oluşumunun önüne geçer
            json.dump(kitaplar, dosya, ensure_ascii=False, indent=4)
    except IOError:
        print("\nHata: Dosya yazılırken bir disk hatası oluştu! Veriler kaydedilemedi.")

def veri_yukle():

    try:
        with open(DOSYA_YOLU, "r", encoding="utf-8") as dosya:
            return json.load(dosya)
    except FileNotFoundError:
         #Dosya yoksa eğer boş listeyle başlıyacaktır!!
        return []
    except (json.JSONDecodeError, IOError):
        
        print("\nUyarı: Kayıt dosyası bozuk veya okunamadı! Boş kütüphane ile başlatılıyor.")
        return []



def kitapları_listele(kitaplar):
    if len(kitaplar) == 0:
        print("\nHenüz kitap eklenmedi.")
        return
    
    print("\n---Kitap Listesi---")
    for sıra, kitap in enumerate(kitaplar):
        # Eğer kitaba puan verilmişse ekrana yazdır, verilmemişse boş bırakır
        puan_yazısı = f" -- [Puan: {kitap['puan']}/5]" if kitap['puan'] else ""
        print(f"{sıra+1}. {kitap['ad']} -- {kitap['yazar']} -- [{kitap['durum']}]{puan_yazısı}")


def kitap_ekle(kitaplar):
    kitap_adı = input("\n Kitap Adı Giriniz: ").strip()
    yazar_adı = input("\n Yazar Adı Giriniz: ").strip()
    
    if kitap_adı == "" or yazar_adı == "":
        print("\n Hata: Kitap Adı veya Yazar Adı Boş Bırakılamaz!")
    else:
        yeni_kitap = {
            "ad": kitap_adı,
            "yazar": yazar_adı,
            "durum": "Okunmadı",
            "puan": None  
        }
        kitaplar.append(yeni_kitap)
        veri_kaydet(kitaplar)  
        print(f"\n {kitap_adı} -- {yazar_adı} Başarıyla listeye eklendi!")


def kitap_sil(kitaplar):
    kitapları_listele(kitaplar)
    kitap_no = input("\n Silmek istediğiniz kitabın numarasını giriniz: ").strip()
    try:
        kitap_no = int(kitap_no) - 1
        if kitap_no < 0 or kitap_no >= len(kitaplar):
            print("\nGeçersiz numara!")
            return
            
        silinen_kitap = kitaplar.pop(kitap_no)
        veri_kaydet(kitaplar)  
        print(f"\n '{silinen_kitap['ad']}' Adlı Kitap Başarıyla Silindi!")
    except ValueError:
        print("\nHata: Lütfen geçerli bir sıra numarası girin!")


def kitap_durum(kitaplar):
    kitapları_listele(kitaplar)
    kitap_no = input("\n Durumunu değiştirmek istediğiniz kitabın numarasını giriniz: ").strip()
    try:
        kitap_no = int(kitap_no) - 1
        if kitap_no < 0 or kitap_no >= len(kitaplar):
            print("\nGeçersiz numara!")
            return
            
        # JSON ile değer değiştir!
        if kitaplar[kitap_no]["durum"] == "Okunmadı":
            kitaplar[kitap_no]["durum"] = "Okundu"
        else:
            kitaplar[kitap_no]["durum"] = "Okunmadı"
            
        veri_kaydet(kitaplar)  
        print(f"\n Kitap durumu '{kitaplar[kitap_no]['durum']}' olarak güncellendi!")
    except ValueError:
        print("\nHata: Lütfen geçerli bir sıra numarası girin!")


def kitap_puan(kitaplar):
    kitapları_listele(kitaplar)
    kitap_no = input("\n Hangi Kitap'a Puan Vermek İstiyorsunuz? ").strip()
    try:
        kitap_no = int(kitap_no) - 1
        if kitap_no < 0 or kitap_no >= len(kitaplar):
            print("\nGeçersiz numara!")
            return

        puan = input("\n Kitaba kaç puan vermek istiyorsunuz? (1-5): ").strip()
        if puan not in ["1", "2", "3", "4", "5"]:
            print("\nHata: Lütfen sadece 1 ile 5 arasında bir sayı girin!")
            return

        
        kitaplar[kitap_no]["puan"] = int(puan)
        veri_kaydet(kitaplar)  # Yönerge: Her değişiklikte kaydet
        print(f"\n Kitap'a başarıyla {puan}/5 puanı verildi!")
    except ValueError:
        print("\nHata: Lütfen geçerli bir sıra numarası girin!")



kitaplar = veri_yukle()

while True:
    menü_göster()
    secim = secim_al()
    
    if secim == "1":
        kitapları_listele(kitaplar)
    elif secim == "2":
        kitap_ekle(kitaplar) 
    elif secim == "3":
        kitap_sil(kitaplar)       
    elif secim == "4":
        kitap_durum(kitaplar)
    elif secim == "5":
        kitap_puan(kitaplar)
    elif secim == "6":
        print("\n Program Sonlandırılıyor... İyi okumalar!")
        exit()
    else:
        print("\n Geçersiz seçenek! Lütfen 1-6 arasında bir sayı giriniz.")