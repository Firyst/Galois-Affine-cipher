from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog


class WarnDialog(QDialog):
    """! Предупреждающее/информационное диалоговое окно.
    """
    def __init__(self, title: str, text: str):
        """! Инициализация окна
        @param title: название окна
        @param text: текст сообщения
        """
        super().__init__()
        uic.loadUi('forms/warning.ui', self)  # загрузка UI файла
        self.setWindowFlags(Qt.WindowContextHelpButtonHint ^ self.windowFlags())  # отключить подсказки

        self.setWindowTitle(title)
        self.mainLabel.setText(text)
        self.buttonConfirm.clicked.connect(self.close_dialog)

    def close_dialog(self):
        """! Закрытие диалогового окна. Вызывается при нажатии на кнопку.
        """
        self.close()