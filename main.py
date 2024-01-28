# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sys
import os
import importlib
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from dialogs import WarnDialog
import galois
from galois import *
import affine


class ProgramWindow(QMainWindow):
    """! Главное окно программы
    """
    def __init__(self):
        """! Инициализация окна
        """
        super().__init__()
        uic.loadUi('forms/main.ui', self)

        self.random_button.clicked.connect(self.generate_irr)
        self.build_button.clicked.connect(self.set_irr)
        self.button_abc.clicked.connect(self.set_affine_abc)
        self.button_bin.clicked.connect(self.set_affine_bin)
        self.button_add.clicked.connect(self.show_add)
        self.button_mul.clicked.connect(self.show_mul)
        self.button_encrypt.clicked.connect(self.run_encrypt)
        self.button_decrypt.clicked.connect(self.run_decrypt)
        self.combo_elem.currentTextChanged.connect(self.show_powers)

        # maths
        self.field = None

    def update_info(self):
        # главное поле
        self.text_p.setText(str(self.field.p))
        self.text_n.setText(str(self.field.n))
        irreducible = galois.GaloisFieldElement(self.field.irreducible, self.field.p, [])
        self.text_irreducible.setText("   " + irreducible.fancy())

        # ЭЛЕМЕНТЫ
        # сначала очищаем таблицу
        while self.element_table.rowCount():
            self.element_table.removeRow(0)

        self.element_table.setRowCount(len(self.field.elements) + 1)

        # добавить 0 элемент
        item_poly0 = QTableWidgetItem("0")
        item_poly0.setFlags(Qt.ItemIsEditable)
        item_pow0 = QTableWidgetItem("-1")
        item_pow0.setFlags(Qt.ItemIsEditable)
        self.element_table.setItem(0, 1, item_poly0)
        self.element_table.setItem(0, 0, item_pow0)

        # записать все элементы
        for i, element in enumerate(self.field.elements):
            item_poly = QTableWidgetItem(element.fancy())
            item_poly.setFlags(Qt.ItemIsEditable)  # выключаем возможность редактировать элемент

            item_pow = QTableWidgetItem(str(i))  # порядок
            item_pow.setFlags(Qt.ItemIsEditable)  # выключаем возможность редактировать элемент

            self.element_table.setItem(i + 1, 1, item_poly)
            self.element_table.setItem(i + 1, 0, item_pow)

        self.element_table.setColumnWidth(0, 50)
        self.element_table.setColumnWidth(1, 500)

        self.element_table.setStyleSheet("color: rgb(0, 0, 0)")

        # ГРУППЫ
        while self.group_table.rowCount():
            self.group_table.removeRow(0)

        groups = self.field.find_groups()
        self.group_table.setRowCount(len(groups))
        for i, group in enumerate(groups.values()):
            item_pow = QTableWidgetItem(str(group.power))  # порядок
            item_pow.setFlags(Qt.ItemIsEditable)

            item_root = QTableWidgetItem(" = ".join(map(lambda s: f"<{s.fancy()}>", group.roots)))  # образующие
            item_root.setFlags(Qt.ItemIsEditable)

            item_elem = QTableWidgetItem("; ".join(map(GaloisFieldElement.fancy, group.elements)))  # элементы
            item_elem.setFlags(Qt.ItemIsEditable)

            self.group_table.setItem(i, 0, item_pow)
            self.group_table.setItem(i, 1, item_root)
            self.group_table.setItem(i, 2, item_elem)

        self.group_table.setStyleSheet("color: rgb(0, 0, 0)")

        self.combo_elem.clear()
        self.combo_elem.addItems(map(GaloisFieldElement.fancy, self.field.elements[1:]))

        # ТАБЛИЦА УМНОЖЕНИЯ

        self.mult_table.setRowCount(len(self.field.elements))
        self.mult_table.setColumnCount(len(self.field.elements))

        self.add_table.setRowCount(len(self.field.elements))
        self.add_table.setColumnCount(len(self.field.elements))

        for i, element in enumerate(self.field.elements):
            self.mult_table.setHorizontalHeaderItem(i, QTableWidgetItem(element.fancy()))
            self.mult_table.setVerticalHeaderItem(i, QTableWidgetItem(element.fancy()))

            self.add_table.setHorizontalHeaderItem(i, QTableWidgetItem(element.fancy()))
            self.add_table.setVerticalHeaderItem(i, QTableWidgetItem(element.fancy()))

        for i in range(len(self.field.elements)):
            for j in range(i + 1):
                element = self.field.get_mult(i, j)
                item_poly = QTableWidgetItem(element.fancy())

                self.mult_table.setItem(i, j, item_poly)
                self.add_table.setItem(i, j, QTableWidgetItem((self.field.elements[i] + self.field.elements[j]).fancy()))

        # АФФИННЫЙ

        # разрешить двоичный режим
        self.button_bin.setEnabled(self.field.p == 2)
        if self.field.p != 2:
            self.button_abc.click()

    def show_powers(self):
        def add_elem_table(column_title, data):
            column_count = self.power_table.columnCount()
            self.power_table.setColumnCount(column_count + 1)

            # Установка названия столбца
            self.power_table.setHorizontalHeaderItem(column_count, QTableWidgetItem(column_title))

            self.power_table.setItem(0, column_count, QTableWidgetItem(data))

        data_string = self.combo_elem.currentText()

        if not data_string:
            return

        self.power_table.setRowCount(1)
        self.power_table.setColumnCount(0)
        self.power_table.setVerticalHeaderItem(0, QTableWidgetItem("aⁿ"))
        for e in self.field.elements:
            if e.fancy() == data_string:
                poly = e

                counter = 1
                while poly.coefficients != [1, ]:
                    add_elem_table(str(counter), poly.fancy())
                    counter += 1
                    poly = poly * e
                add_elem_table(str(counter), poly.fancy())
                break

    def set_affine_abc(self):
        self.label_abc.show()
        self.line_abc.show()

    def set_affine_bin(self):
        self.label_abc.hide()
        self.line_abc.hide()

    def check_poly(self, data) -> GaloisFieldElement:
        if not self.field.ready:
            d = WarnDialog("Ошибка", "Поле не определено")
            d.exec_()
            return

        try:
            c = list(map(int, data.split()))

            # проверить, что коэффициенты в норме
            for c0 in c:
                if c0 >= self.field.p:
                    d = WarnDialog("Ошибка", "Неверные коэффициенты многочлена!")
                    d.exec_()
                    return

        except ValueError:
            d = WarnDialog("Ошибка", "Неверный ввод!")
            d.exec_()
            return

        try:
            return self.field.get(self.field.get_element(c))
        except KeyError:
            d = WarnDialog("Ошибка", "Такого элемента нету в данном поле Галуа.")
            d.exec_()
            return

    def generate_irr(self):
        # проверить, просто ли число
        p, n = int(self.box_p.text()[2:]), int(self.box_n.text()[2:])

        if not galois.is_prime(p):
            d = WarnDialog("Ошибка", "Число p не простое!")
            d.exec_()
            return

        self.field = galois.GaloisField(p, n, galois.generate_irreducible2(p, n))
        self.poly_edit.setText(' '.join(map(str, self.field.irreducible)))
        self.update_info()

    def set_irr(self):
        # проверить, просто ли число
        p, n = int(self.box_p.text()[2:]), int(self.box_n.text()[2:])

        if not galois.is_prime(p):
            d = WarnDialog("Ошибка", "Число p не простое!")
            d.exec_()
            return

        input_text = self.poly_edit.text()

        try:
            c = list(map(int, input_text.split()))

            # проверить, что коэффициенты в норме
            for c0 in c:
                if c0 >= p:
                    d = WarnDialog("Ошибка", "Неверные коэффициенты многочлена!")
                    d.exec_()
                    return
        except ValueError:
            d = WarnDialog("Ошибка", "Неверный ввод!")
            d.exec_()
            return

        self.field = GaloisField(p, n)
        try:
            self.field.set_irreducible(c)
        except ArithmeticError as e:
            d = WarnDialog("Ошибка", str(e))
            d.exec_()
            return

        self.update_info()

    def show_add(self):
        a = self.check_poly(self.line_add_a.text())
        b = self.check_poly(self.line_add_b.text())
        if a is not None and b is not None:
            result = a + b
            self.line_add_res.setText(result.fancy())

    def show_mul(self):
        a = self.check_poly(self.line_mul_a.text())
        b = self.check_poly(self.line_mul_b.text())
        if a is not None and b is not None:
            result = a * b
            self.line_mul_res.setText(result.fancy())

    def run_encrypt(self):
        if not self.field.ready:
            d = WarnDialog("Ошибка", "Поле не определено")
            d.exec_()
            return
        if self.button_abc.isChecked():
            self.encryptA()
        else:
            self.encryptB()

    def run_decrypt(self):
        if not self.field.ready:
            d = WarnDialog("Ошибка", "Поле не определено")
            d.exec_()
            return
        if self.button_abc.isChecked():
            self.decryptA()
        else:
            self.decryptB()

    def encryptA(self):
        # получить алфавит
        abc = self.line_abc.text()
        if len(abc) != (1 + len(self.field.elements)):
            d = WarnDialog("Ошибка", f"Модуль алфавита должен быть равен {self.field.p * self.field.n}")
            d.exec_()
            return

        # получить ключи
        a = self.check_poly(self.key_a.text())
        b = self.check_poly(self.key_b.text())
        if a is None or b is None:
            return

        input_text = self.text_open.toPlainText()
        try:
            encrypted = affine.encryptA(self.field, abc, input_text, a, b)
        except ValueError:
            d = WarnDialog("Ошибка", f"В открытом тексте есть символ, отсутствующий в заданном алфавите.")
            d.exec_()
            return

        self.text_cipher.setPlainText(encrypted)

    def encryptB(self):
        pass

    def decryptA(self):
        # получить алфавит
        abc = self.line_abc.text()
        if len(abc) != (1 + len(self.field.elements)):
            d = WarnDialog("Ошибка", f"Модуль алфавита должен быть равен {self.field.p * self.field.n}")
            d.exec_()
            return

        # получить ключи
        a = self.check_poly(self.key_a.text())
        b = self.check_poly(self.key_b.text())
        if a is None or b is None:
            return

        input_text = self.text_cipher.toPlainText()
        try:
            decrypted = affine.decryptA(self.field, abc, input_text, a, b)
        except ValueError:
            d = WarnDialog("Ошибка", f"В открытом тексте есть символ, отсутствующий в заданном алфавите.")
            d.exec_()
            return

        self.text_open.setPlainText(decrypted)

    def decryptB(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont("forms/Hack-Regular.ttf")  # load font
    win = ProgramWindow()
    win.show()
    sys.exit(app.exec_())
