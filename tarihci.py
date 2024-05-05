import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

class TarihciUygulamasi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarihçi - Tarihi Olaylar Veritabanı")
        self.setGeometry(100, 100, 500, 400)

        self.initUI()
        self.olaylar = {}

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        
        self.setStyleSheet("background-color: #f5f5dc; font-family: Arial;")

        
        self.label_baslik = QLabel("Tarihçi - Tarihi Olaylar Veritabanı")
        self.label_baslik.setAlignment(Qt.AlignCenter)
        self.label_baslik.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(self.label_baslik)

        
        self.label_olay_ad = QLabel("Olay Adı:")
        self.edit_olay_ad = QLineEdit()
        self.layout.addWidget(self.label_olay_ad)
        self.layout.addWidget(self.edit_olay_ad)

        self.label_olay_tarih = QLabel("Olay Tarihi:")
        self.edit_olay_tarih = QLineEdit()
        self.layout.addWidget(self.label_olay_tarih)
        self.layout.addWidget(self.edit_olay_tarih)

        self.label_olay_aciklama = QLabel("Olay Açıklaması:")
        self.edit_olay_aciklama = QLineEdit()
        self.layout.addWidget(self.label_olay_aciklama)
        self.layout.addWidget(self.edit_olay_aciklama)

        self.btn_olay_ekle = QPushButton("Olay Ekle")
        self.btn_olay_ekle.setStyleSheet("background-color: #8b4513; color: white; border-radius: 5px;")
        self.btn_olay_ekle.clicked.connect(self.ekleOlay)
        self.layout.addWidget(self.btn_olay_ekle)

        
        self.label_icerikler = QLabel("Eklenen Olaylar")
        self.label_icerikler.setFont(QFont("Arial", 12, QFont.Bold))
        self.layout.addWidget(self.label_icerikler)

        self.list_icerikler = QListWidget()
        self.list_icerikler.setStyleSheet("background-color: #d2b48c; border-radius: 5px;")
        self.layout.addWidget(self.list_icerikler)

        
        self.label_sorgula_olay = QLabel("Olay Sorgula:")
        self.layout.addWidget(self.label_sorgula_olay)

        self.edit_sorgula_olay = QLineEdit()
        self.layout.addWidget(self.edit_sorgula_olay)

        self.btn_sorgula_olay = QPushButton("Olayı Sorgula")
        self.btn_sorgula_olay.setStyleSheet("background-color: #8b4513; color: white; border-radius: 5px;")
        self.btn_sorgula_olay.clicked.connect(self.sorgulaOlay)
        self.layout.addWidget(self.btn_sorgula_olay)

        
        self.label_sorgula_tarih = QLabel("Tarih Sorgula:")
        self.layout.addWidget(self.label_sorgula_tarih)

        self.edit_sorgula_tarih = QLineEdit()
        self.layout.addWidget(self.edit_sorgula_tarih)

        self.btn_sorgula_tarih = QPushButton("Tarihi Sorgula")
        self.btn_sorgula_tarih.setStyleSheet("background-color: #8b4513; color: white; border-radius: 5px;")
        self.btn_sorgula_tarih.clicked.connect(self.sorgulaTarih)
        self.layout.addWidget(self.btn_sorgula_tarih)

    def ekleOlay(self):
        olay_ad = self.edit_olay_ad.text()
        olay_tarih = self.edit_olay_tarih.text()
        olay_aciklama = self.edit_olay_aciklama.text()

        if olay_ad in self.olaylar:
            QMessageBox.warning(self, "Uyarı", "Bu olay zaten eklenmiş.")
            return

        sahsiyet_ad, ok = QInputDialog.getText(self, "Şahsiyet Ekle", "Olaya bağlı şahsiyetin adını girin:")
        if not ok:
            return

        if olay_ad not in self.olaylar:
            self.olaylar[olay_ad] = {"Tarih": olay_tarih, "Açıklama": olay_aciklama, "Şahsiyetler": []}
            self.list_icerikler.addItem(f"Olay: {olay_ad} - {olay_tarih} - {olay_aciklama}")

        self.olaylar[olay_ad]["Şahsiyetler"].append(sahsiyet_ad)

        self.list_icerikler.clear()
        for olay, bilgi in self.olaylar.items():
            self.list_icerikler.addItem(f"Olay: {olay} - {bilgi['Tarih']} - {bilgi['Açıklama']}")
            for sahsiyet in bilgi["Şahsiyetler"]:
                self.list_icerikler.addItem(f"    Şahsiyet: {sahsiyet}")

    def sorgulaOlay(self):
        olay_ad = self.edit_sorgula_olay.text()
        if olay_ad in self.olaylar:
            bilgi = self.olaylar[olay_ad]
            sahsiyetler = ", ".join(bilgi["Şahsiyetler"])
            QMessageBox.information(self, "Olay Bilgisi", f"Olay Tarihi: {bilgi['Tarih']}\nOlay Açıklaması: {bilgi['Açıklama']}\nŞahsiyetler: {sahsiyetler}")
        else:
            QMessageBox.warning(self, "Uyarı", "Bu olay veritabanında bulunamadı.")

    def sorgulaTarih(self):
        tarih = self.edit_sorgula_tarih.text()
        bulunan_olaylar = []
        for olay, bilgi in self.olaylar.items():
            if bilgi["Tarih"] == tarih:
                bulunan_olaylar.append((olay, bilgi))

        if bulunan_olaylar:
            mesaj = ""
            for olay, bilgi in bulunan_olaylar:
                sahsiyetler = ", ".join(bilgi["Şahsiyetler"])
                mesaj += f"Olay Adı: {olay}\nTarih: {bilgi['Tarih']}\nAçıklama: {bilgi['Açıklama']}\nŞahsiyetler: {sahsiyetler}\n\n"
            QMessageBox.information(self, "Tarih Bilgisi", mesaj)
        else:
            QMessageBox.warning(self, "Uyarı", "Belirtilen tarihte olay bulunamadı.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TarihciUygulamasi()
    window.show()
    sys.exit(app.exec_())
