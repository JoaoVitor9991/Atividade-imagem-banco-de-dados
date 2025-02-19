import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap


DB_CONFIG = {
    "host": "localhost",
    "user": "root",      
    "password": "",    
    "database": "imagens_db"
}


def salvar_imagem_no_banco(caminho):
    with open(caminho, "rb") as file:
        dados_imagem = file.read()
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO imagens (nome, dados) VALUES (%s, %s)", (caminho.split("/")[-1], dados_imagem))
        conn.commit()
        conn.close()
        print("Imagem salva no banco de dados!")
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")


def carregar_imagem_do_banco():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT dados FROM imagens ORDER BY id DESC LIMIT 1")
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            with open("temp_imagem.png", "wb") as file:
                file.write(resultado[0])
            return "temp_imagem.png"
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
    return None


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Selecionar e Salvar Imagem (MySQL)")
        self.setGeometry(100, 100, 400, 400)

       
        self.botao = QPushButton("Selecionar Imagem", self)
        self.botao.clicked.connect(self.abrir_selecionador)

        
        self.label_imagem = QLabel(self)
        self.label_imagem.setFixedSize(300, 300)

        
        layout = QVBoxLayout()
        layout.addWidget(self.botao)
        layout.addWidget(self.label_imagem)
        self.setLayout(layout)

    def abrir_selecionador(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg *.bmp)")

        if caminho:
            salvar_imagem_no_banco(caminho)
            self.exibir_imagem()

    def exibir_imagem(self):
        caminho = carregar_imagem_do_banco()
        if caminho:
            pixmap = QPixmap(caminho)
            self.label_imagem.setPixmap(pixmap.scaled(300, 300))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = App()
    janela.show()
    sys.exit(app.exec_())
