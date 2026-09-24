
import sys

from PySide6.QtWidgets import QApplication
from src.Interface.gerenciador_janelas import GerenciadorJanelas


def main():
    app = QApplication(sys.argv)

    gerenciador = GerenciadorJanelas()
    gerenciador.abrir("inicio")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()