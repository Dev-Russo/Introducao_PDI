# main.py
import sys
from PyQt5.QtWidgets import QApplication
# Importa a classe principal da nossa interface
from interface import App

if __name__ == '__main__':
    """
    Função principal que executa a aplicação.
    """
    app = QApplication(sys.argv)
    janela = App()
    janela.show()
    sys.exit(app.exec_())