import socket
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class DropArea(QLabel): # Класс для отправителя
    def __init__(self):
        super().__init__("Перетащите файл сюда/нажмите для проводника")
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

class ReceiveWidget(QLabel): # класс получателя
  accepted = pyqtSignal()
  rejected = pyqtSignal()

  def __init__(self):
    super().__init__("Ожидание входящих файлов...")
    self.setAlignment(Qt.AlignCenter)
    self.setMinimumHeight(200)

    self.setStyleSheet(
        "QLabel { border: 2px dashed #888; border-radius: 8px; "
        "font-size: 14px; color: #555; }"
    ) 


class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Файлообменник")
    self.resize(600, 450)

    # --- 1. ВЕРХНЯЯ ПАНЕЛЬ ---
    self.ip_label = QLabel(f"Ваш IP: {self.get_local_ip()}")

    # Переключатель режимов
    self.btn_mode_send = QPushButton("Отправка") 
    self.btn_mode_receive = QPushButton("Приём")
    self.btn_mode_send.setCheckable(True)
    self.btn_mode_receive.setCheckable(True)
    self.btn_mode_send.setChecked(True)  # По умолчанию отправка

    self.btn_mode_send.clicked.connect(lambda: self.switch_mode(0))
    self.btn_mode_receive.clicked.connect(lambda: self.switch_mode(1))

    top_layout = QHBoxLayout()
    top_layout.addWidget(self.ip_label)
    top_layout.addStretch()
    top_layout.addWidget(self.btn_mode_send)
    top_layout.addWidget(self.btn_mode_receive)

    # прогресс бар
    self.progress_bar = QProgressBar()
    self.progress_bar.setRange(0, 100)
    self.progress_bar.setValue(0)
    self.progress_bar.setTextVisible(False)
    self.progress_bar.setFixedHeight(6)
    self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #e0e0e0;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #3c8dbc;
                border-radius: 3px;
            }
        """)

    # стакаем
    self.stack = QStackedWidget()

    # отправитель
    sender_page = QWidget()
    sender_layout = QVBoxLayout(sender_page)

    target_layout = QHBoxLayout()
    target_layout.addWidget(QLabel("IP получателя:"))
    self.device_chose = QLineEdit()
    self.device_chose.setPlaceholderText("В формате 192.168.1.15")
    target_layout.addWidget(self.device_chose)

    self.drop_area = DropArea()

    self.confirm_button = QPushButton("Отправить файл")
    self.confirm_button.clicked.connect(self.on_confirm)

    sender_layout.addLayout(target_layout)
    sender_layout.addWidget(self.drop_area, stretch=1)
    sender_layout.addWidget(self.confirm_button)

    # получатель
    self.receive_page = ReceiveWidget()

    self.stack.addWidget(sender_page)  # ind0
    self.stack.addWidget(self.receive_page)  # ind1

    # final rasp
    main_layout = QVBoxLayout()
    main_layout.addLayout(top_layout)
    main_layout.addWidget(self.progress_bar)
    main_layout.addSpacing(10) # отдел прогрс
    main_layout.addWidget(self.stack, stretch=1)

    container = QWidget()
    container.setLayout(main_layout)
    self.setCentralWidget(container)

  def switch_mode(self, index: int):
    self.stack.setCurrentIndex(index)
    self.btn_mode_send.setChecked(index == 0)
    self.btn_mode_receive.setChecked(index == 1)

  def set_progress(self, value: int): 
    self.progress_bar.setValue(max(0, min(100, value)))

  def on_confirm(self):
    file_path = self.drop_area.selected_file
    device = self.device_chose.text().strip() 
    if not file_path or not device:
      QMessageBox.warning(self, "Ошибка", "Выберите файл и укажите IP устройства.")
      return
    print(f"Отправка файла: {file_path} -> {device}")

  @staticmethod
  def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
      s.connect(("8.8.8.8", 80))
      return s.getsockname()[0]
    except Exception:
      return "не определён"
    finally:
      s.close()


if __name__ == "__main__": # выполняем, только если файл запущен напрямую
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()