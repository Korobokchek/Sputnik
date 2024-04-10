import time, os, sys, serial
import folium
import numpy as np
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QHBoxLayout, QLineEdit
from PyQt5.QtCore import QTimer, QDateTime, Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap


def com_read(timeout=1):
    # 55.9297334, 37.6173
    '''Время по RTC; Время со старта; Высота по GPS(1000); высота по барометру(6000);
    Широта(55.9297334); Долгота(37.6173); давление; температура; Ускорение Z; Давление внутри шара(1000);
    Температура АКБ; Напряжение АКБ(i++); Ток АКБ(0); Ускорение по X; Ускорение по Y; Состояние клапана Н(1); С(0); Нагрев
    '''

    global port, baudrate, prev_values
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        if ser.isOpen():
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time > 1:
                    prev_values[-1] = 0
                    return prev_values

                data = ser.readline().decode(encoding='utf-8').strip()
                if data:
                    tr = data.split(';')
                    prev_values[-1] = 1
                    return list(map(float, tr))
                    # return [float(tr[0]), float(tr[1]), float(tr[2]), float(tr[3]), float(tr[4]),
                    #         float(tr[5]), float(tr[6]), float(tr[7]), float(tr[8]), float(tr[9]),
                    #         float(tr[10]), float(tr[11]), float(tr[12]), float(tr[13]), float(tr[14]),
                    #         float(tr[15]), float(tr[16]), 1]

    except BaseException as e:
        print("Произошла ошибка при открытии порта:", e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.datetimeLabel = QLabel()
        self.textEdit = QTextEdit()
        self.lineEdit = QLineEdit()
        self.browser = QWebEngineView()
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(QPixmap("4.png"))
        self.imageLabel.setScaledContents(True)

        self.graph_battary_temperature = PlotWidget()
        self.graph_temperature = PlotWidget()
        self.graph_battary_voltage = PlotWidget()
        self.graph_battary_current = PlotWidget()
        self.graph_accX = PlotWidget()
        self.graph_mono_pressure = PlotWidget()

        main_layout = QHBoxLayout()

        self.graphLayout = QVBoxLayout()
        self.graphLayout.addWidget(self.graph_battary_temperature)
        self.graphLayout.addWidget(self.graph_temperature)
        self.graphLayout.addWidget(self.graph_battary_voltage)
        self.graphLayout.addWidget(self.graph_battary_current)
        self.graphLayout.addWidget(self.graph_accX)
        self.graphLayout.addWidget(self.graph_mono_pressure)
        main_layout.addLayout(self.graphLayout)

        not_graph_layout = QVBoxLayout()
        not_graph_layout.addWidget(self.datetimeLabel)
        not_graph_layout.addWidget(self.textEdit)
        not_graph_layout.addWidget(self.lineEdit)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.browser)

        right_bottom_layout = QHBoxLayout()
        right_bottom_layout.addWidget(self.imageLabel)
        bottom_layout.addLayout(right_bottom_layout)

        not_graph_layout.addLayout(bottom_layout)
        main_layout.addLayout(not_graph_layout)


        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("Телеметрия")
        self.setGeometry(100, 200, 1000, 600)

        self.graph_battary_temperature.setTitle("Температура АКБ")
        self.graph_battary_temperature.setXRange(0, 11)
        self.graph_battary_temperature.setYRange(0, 11)

        self.graph_temperature.setTitle("Внешняя температура")
        self.graph_temperature.setXRange(0, 11)
        self.graph_temperature.setYRange(0, 11)

        self.graph_battary_voltage.setTitle("Напряжение АКБ")
        self.graph_battary_voltage.setXRange(0, 11)
        self.graph_battary_voltage.setYRange(0, 11)

        self.graph_battary_current.setTitle("Ток АКБ")
        self.graph_battary_current.setXRange(0, 11)
        self.graph_battary_current.setYRange(0, 11)

        self.graph_accX.setTitle("Ускорение")
        self.graph_accX.setXRange(0, 11)
        self.graph_accX.setYRange(0, 11)
        self.lineEdit.returnPressed.connect(self.update_text)

        self.graph_mono_pressure.setTitle("Давление в шаре")
        self.graph_mono_pressure.setXRange(0, 11)
        self.graph_mono_pressure.setYRange(0, 11)
        self.lineEdit.returnPressed.connect(self.update_text)

        self.timer = QTimer()
        self.timer.setInterval(800)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.load_html_content(m.get_root().render(), QUrl.fromLocalFile(os.path.abspath('')))
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.update_map)
        self.timer2.start(2000)

        self.data_battary_voltage = np.zeros(100)
        self.data_battary_current = np.zeros(100)
        self.data_battary_temerature = np.zeros(100)
        self.data_temperature = np.zeros(100)
        self.data_accX = np.zeros(100)
        self.data_mono_pressure = np.zeros(100)
        self.x = np.linspace(0, 10, 100)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b; /* Цвет фона */
            }

            QLabel#datetimeLabel {
                font-size: 22px;
                color: #f0f0f0; /* Цвет текста */
                font-weight: bold;
            }

            QTextEdit {
                background-color: #1e1e1e; /* Цвет фона текстового поля */
                border: 5px solid #000;
                color: #f0f0f0; /* Цвет текста */
                font-size: 14px;
            }

            QLineEdit {
                background-color: #1e1e1e; /* Цвет фона поля ввода */
                color: #f0f0f0; /* Цвет текста */
                font-size: 14px;
                border: 5px solid #555;
                border-radius: 5px;
            }

            PlotWidget {
                background-color: #1e1e1e; /* Цвет фона графиков */
                border: 5px solid #555;
                border-radius: 100px;

            }

            /* Заголовки графиков */
            PlotWidget > QLabel {
                color: #f0f0f0; /* Цвет текста */
            }

            /* Цвет линий графиков */
            PlotWidget > QFrame {
                background-color: #2b2b2b; /* Цвет фона */
            }
        """)

    def update_plot(self):
        global prev_values
        values = com_read()

        print(values)

        RTCtime = values[0]
        if RTCtime:
            pass
        else:
            RTCtime = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss")

        mission_time = values[1]
        GPS_h = values[2]
        baro_h = values[3]
        shirota = values[4]
        dolgota = values[5]
        pressure = values[6]
        temperature = values[7]
        accZ = values[8]
        mono_pressure = values[9]
        battary_temperature = values[10]
        battary_voltage = values[11]
        battary_current = values[12]
        accX = values[13]
        accY = values[14]
        clapanN = values[15]
        clabsnS = values[16]
        nagrev = values[17]

        self.data_battary_voltage = np.append(self.data_battary_voltage[1:], battary_voltage)
        self.data_battary_current = np.append(self.data_battary_current[1:], battary_current)
        self.data_battary_temerature = np.append(self.data_battary_temerature[1:], battary_temperature)
        self.data_temperature = np.append(self.data_temperature[1:], temperature)
        self.data_mono_pressure = np.append(self.data_mono_pressure[1:], mono_pressure)
        self.data_accX = np.append(self.data_accX[1:], accX)
        prev_values = values
        self.x += 0.1

        self.graph_battary_temperature.plot(self.x, self.data_battary_temerature, clear=True, pen={'color': 'b', 'width': 4})
        self.graph_temperature.plot(self.x, self.data_temperature, clear=True, pen={'color': 'r', 'width': 4})
        self.graph_battary_voltage.plot(self.x, self.data_battary_voltage, clear=True, pen={'color': 'g', 'width': 4})
        self.graph_battary_current.plot(self.x, self.data_battary_current, clear=True, pen={'color': 'm', 'width': 4})
        self.graph_accX.plot(self.x, self.data_accX, clear=True, pen={'color': 'c', 'width': 4})
        self.graph_mono_pressure.plot(self.x, self.data_mono_pressure, clear=True, pen={'color': 'w', 'width': 4})

        self.datetimeLabel.setText(f"{RTCtime}\t{shirota}° {dolgota}° {GPS_h}м")
        self.datetimeLabel.setStyleSheet("font-size: 22px; color: white; font-weight: bold;")

        if clapanN:
            state = "надув"
        elif clabsnS:
            state = "стравливание"
        else:
            state = "клапаны закрты"
        if clapanN and clabsnS:
            state = "ОШИБКА (оба клапана открыты)"

        if nagrev:
            nagrev_state = "батарея нагревается"
        else:
            nagrev_state = ''

        if prev_values[-1]:
            self.textEdit.append(f"{RTCtime}\tвремя миссии: {mission_time}c\t{temperature}°C\tускорение х, y, z: {accX, accY, accZ}м/с\tАКБ: {battary_temperature}°C\t{battary_voltage}B\t{battary_current}А\nкоординаты: {shirota}°\t{dolgota}°\t{GPS_h}м\t{pressure}Па\t{baro_h}м (по давлению)\t\t{mono_pressure}Па(в шаре)\t\t{state}\t{nagrev_state}\n\n\n\n")
            # self.textEdit.append(f"{RTCtime}\t{mission_time}c\t{temperature}°C\t{accX, accY, accZ}м/с\tАКБ: {battary_temperature}°C\t{battary_voltage}B\t{battary_current}А\t{shirota}°\t{dolgota}°\t{GPS_h}м\t{pressure}Па\t{baro_h}м\t{mono_pressure}Па(в шаре)\n\n\n\n")
        else:
            self.textEdit.append(f"! {RTCtime}\tвремя миссии: {mission_time}c\t{temperature}°C\tускорение х, y, z: {accX, accY, accZ}м/с\tАКБ: {battary_temperature}°C\t{battary_voltage}B\t{battary_current}А\nкоординаты: {shirota}°\t{dolgota}°\t{GPS_h}м\t{pressure}Па\t{baro_h}м (по давлению)\t\t{mono_pressure}Па(в шаре)\t\t{state}\t{nagrev_state}\n\n\n\n")
            # self.textEdit.append(f"! {RTCtime}\t{mission_time}c\t{temperature}°C\t{accX, accY, accZ}м/с\tАКБ: {battary_temperature}°C\t{battary_voltage}B\t{battary_current}А\t{shirota}°\t{dolgota}°\t{GPS_h}м\t{pressure}Па\t{baro_h}м\t{mono_pressure}Па(в шаре)\n\n\n\n")


    def update_text(self, tx=''):
        global port, ser
        # file = open("logs.txt", 'w', encoding='utf-8')
        text = self.lineEdit.text().strip()
        match text:
            case "зыз":
                self.textEdit.append("зыыыыыыыыыыыыыыыыыыыыыыыыыыыыз")
            case "open":
                self.textEdit.append("Система сдува запущена")
                # file.write("Система сдува запущена\n")
                self.lineEdit.clear()
                # ser.write(b"1103_on\n")
            case "close":
                self.textEdit.append("Система надува запущена")
                # file.write("Система надува запущена\n")
                self.lineEdit.clear()
                # ser.write(b"1103_off\n")
            case "clear":
                self.textEdit.clear()
            case _:
                self.textEdit.append(text)
                # file.write(text)
                # print(text)

        self.lineEdit.clear()

    def load_html_content(self, content, base_url):
        self.browser.setHtml(content, baseUrl=base_url)

    def update_map(self):
        global m
        global marker
        global prev_values

        marker.location = [prev_values[5], prev_values[6]]

        # Устанавливаем новые координаты центра карты
        m.location = [marker.location[0], marker.location[1]]

        # Получаем HTML-контент карты и загружаем его в WebView
        html_content = m.get_root().render()
        self.load_html_content(html_content, QUrl.fromLocalFile(os.path.abspath('')))



if __name__ == '__main__':
    port = 'COM11'
    baudrate = 115200
    prev_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
    ser = serial.Serial(port, 115200)

    m = folium.Map(location=[55.9297334, 37.6173], zoom_start=10)
    marker = folium.Marker(location=[55.9297334, 37.6173], popup='Мое местоположение')
    marker.add_to(m)
    m.save('index.html')

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

