import sys
import socket

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QLineEdit
)


class DropArea(QLabel):
    def __init__(self):
        super().__init__("Перетащите файл сюда")
        self.setAlignment(Qt.AlignCenter)   # Центрируем текст
        self.setAcceptDrops(True)           # разрешаем приём drop-событий
        self.setMinimumHeight(200)          # Минимальная высота
        self.setStyleSheet(
            "QLabel { border: 2px dashed #888; border-radius: 8px; "
            "font-size: 14px; color: #555; }"
        )
        self.selected_file = None
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls() # получаем список путей
        if urls: # список не пустой
            path = urls[0].toLocalFile() # берём один элемент и превращаем в локальный путь
            self.set_file(path) 
            event.acceptProposedAction() # Убедиться, что всё выполнено
    # пока сделал только для одного объекта        

    # Проводник
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.open_file_dialog()

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите ф", "", "Все файлы (*)"
        )
        if path:
            self.set_file(path)

    def set_file(self, path):
        self.selected_file = path
        self.setText(f"Выбран файл:\n{path}")
        self.setStyleSheet(
            "QLabel { border: 2px solid #3c8dbc; border-radius: 8px; "
            "font-size: 14px; color: #222; background: #eaf4fb; }"
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мой PyQt5 App")
        self.resize(600, 450)

        # верх панель
        self.ip_label = QLabel(f"Ваш IP: {self.get_local_ip()}")

                

        #self.device_chose = QComboBox() # Создаём выпадающий список список device_chose
        # self.device_chose.addItems([ #Заполняем список
        #     "192.168.1.1",
        #     "192.168.1.2",
        #     "192.168.1.3",
        #     "192.168.1.4",
        # ])

        self.device_chose = QLineEdit()

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.ip_label)
        top_layout.addStretch()               # раздвигаем по краям
        top_layout.addWidget(QLabel("Устройство:"))
        top_layout.addWidget(self.device_chose)
       

        # дроп зона
        self.drop_area = DropArea()

        # низ
        self.confirm_button = QPushButton("Подтвердить")
        self.confirm_button.clicked.connect(self.on_confirm)

        # собираем по порядку
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.drop_area, stretch=1)
        main_layout.addWidget(self.confirm_button)

        container = QWidget() # пустой виджет, через него обработка
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def on_confirm(self):
        file_path = self.drop_area.selected_file
        device = self.device_chose.currentText() # забрать выбраный ip 
        print(f"Файл: {file_path}, устройство: {device}") # заглушка

    @staticmethod # можем без self писать
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0] # 0 - ip
        except Exception:
            return "не определён"
        finally:
            s.close()


if __name__ == "__main__": # выполняем, только если файл запущен напрямую
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()