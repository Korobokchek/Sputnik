import os, sys, serial
import folium
import numpy as np
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QHBoxLayout, QLineEdit
from PyQt5.QtCore import QTimer, QDateTime, Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap
import serial_read


class TelemetriaWindow(QMainWindow):
    def __init__(self):
        super(TelemetriaWindow, self).__init__()

        self.datatimeLabel = QLabel()
        self.logsfield = QTextEdit()
        self.inputfield = QLineEdit()
        self.map = QWebEngineView()
        self.indicators = QLabel()
        self.battary_temperature_graph = PlotWidget()
        self.battary_voltage_graph = PlotWidget()
        self.battary_amperage_graph = PlotWidget()
        self.pressure_graph = PlotWidget()
        self.accZ_graph = PlotWidget()
        self.monometr_pressure_graph = PlotWidget()

        self.indicators.setPixmap(QPixmap("4.png"))
        self.indicators.setScaledContents(True)

        main_layout = QHBoxLayout()

        self.graphLayout = QVBoxLayout()
        self.graphLayout.addWidget(self.pressure_graph)
        self.graphLayout.addWidget(self.monometr_pressure_graph)
        self.graphLayout.addWidget(self.battary_temperature_graph)
        self.graphLayout.addWidget(self.battary_voltage_graph)
        self.graphLayout.addWidget(self.battary_amperage_graph)
        self.graphLayout.addWidget(self.accZ_graph)
        main_layout.addLayout(self.graphLayout)

        data_layout = QVBoxLayout()
        data_layout.addWidget(self.datatimeLabel)
        data_layout.addWidget(self.logsfield)
        data_layout.addWidget(self.inputfield)
        bottom_data_layout = QHBoxLayout()
        bottom_data_layout.addWidget(self.map)
        bottom_data_layout.addWidget(self.indicators)
        data_layout.addLayout(bottom_data_layout)
        main_layout.addLayout(data_layout)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("Телеметрия")
        self.setGeometry(100, 200, 1000, 600)

        self.pressure_graph.setTitle("Внешнее Давление")
        self.monometr_pressure_graph.setTitle("Давление в шаре")
        self.battary_temperature_graph.setTitle("Температура АКБ")
        self.battary_voltage_graph.setTitle("Напряжение АКБ")
        self.battary_amperage_graph.setTitle("Ток АКБ")
        self.accZ_graph.setTitle("Учкорение по Z")
        self.inputfield.returnPressed.connect(self.update_text)

        self.load_html_content(m.get_root().render(), QUrl.fromLocalFile(os.path.abspath('')))

        self.plot_update_timer = QTimer()
        self.plot_update_timer.setInterval(800)
        self.plot_update_timer.timeout.connect(self.update_plot)
        self.plot_update_timer.start()

        self.map_update_timer = QTimer()
        self.map_update_timer.setInterval(2000)
        self.map_update_timer.timeout.connect(self.update_map)
        self.map_update_timer.start()

        self.data_pressure = np.zeros(100)
        self.data_monometr_pressure = np.zeros(100)
        self.data_battary_temperature = np.zeros(100)
        self.data_battary_voltage = np.zeros(100)
        self.data_battary_amperage = np.zeros(100)
        self.data_accZ = np.zeros(100)
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
        global prev_data
        data = serial_read.read_from_com_port("COM11", 115200)
        RTCtime = QDateTime.currentDateTime().toString("dd.MM.yyyy hh:mm:ss")
        mission_time = data[1], GPS_h = data[2], baro_h = data[3], shirota = data[4], dolgota = data[5]
        pressure = data[6], temperature = data[7], accZ = data[8], mono_pressure = data[9]
        battary_temperature = data[10], battary_voltage = data[11], battary_current = data[12]
        accX = data[13], accY = data[14], clapanN = data[15], clabsnS = data[16], nagrev = data[17]

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

        log_string = f"{RTCtime}\tвремя миссии: {mission_time}c\t{temperature}°C\tускорение х, y, z: {accX, accY, accZ}м/с\tАКБ: {battary_temperature}°C\t{battary_voltage}B\t{battary_current}А\nкоординаты: {shirota}°\t{dolgota}°\t{GPS_h}м\t{pressure}Па\t{baro_h}м (по давлению)\t\t{mono_pressure}Па(в шаре)\t\t{state}\t{nagrev_state}\n\n\n\n"

        self.data_pressure = np.append(self.data_pressure, pressure)
        self.data_monometr_pressure = np.append(self.data_monometr_pressure, mono_pressure)
        self.data_battary_temperature = np.append(self.data_battary_temperature, battary_temperature)
        self.data_battary_voltage = np.append(self.data_battary_voltage, battary_voltage)
        self.data_battary_amperage = np.zeros(self.data_battary_amperage, battary_current)
        self.data_accZ = np.zeros(self.data_accZ, accZ)

        prev_data = data
        self.x += 0.1

        self.pressure_graph.plot(self.x, self.data_pressure, clear=False, pen={'color': 'b', 'width': 4})
        self.monometr_pressure_graph.plot(self.x, self.data_monometr_pressure, clear=True, pen={'color': 'w', 'width': 4})
        self.battary_temperature_graph.plot(self.x, self.data_battary_temperature, clear=True, pen={'color': 'b', 'width': 4})
        self.battary_voltage_graph.plot(self.x, self.data_battary_voltage, clear=True, pen={'color': 'g', 'width': 4})
        self.battary_amperage_graph.plot(self.x, self.battary_amperage_graph, clear=True, pen={'color': 'm', 'width': 4})
        self.accZ_graph.plot(self.x, self.data_accZ, clear=True, pen={'color': 'c', 'width': 4})

        self.datetimeLabel.setText(f"{RTCtime}\t{shirota}° {dolgota}° {GPS_h}м")
        self.datetimeLabel.setStyleSheet("font-size: 22px; color: white; font-weight: bold;")

        self.logsfield.append(log_string)

    def update_text(self):
        # global port, ser
        file = open("logs.txt", 'w', encoding='utf-8')
        text = self.inputfield.text().strip()

        match text:
            case "зыз":
                text = "зыыыыыыыыыыыыыыыыыыыыыыыыыыыыз"
            case "open":
                text = "Система сдува запущена"
                # ser.write(b"1103_on\n")
            case "close":
                text = "Система надува запущена"
                # ser.write(b"1103_off\n")
            case "clear":
                text = ''
                self.logsfield.clear()
            case _:
                pass

        self.logsfield.append(text)
        file.write(text)
        file.close()
        self.inputfield.clear()

    def load_html_content(self, content, base_url):
        self.map.setHtml(content, baseUrl=base_url)

    def update_map(self):
        global m, marker, prev_data
        marker.location = [prev_data[5], prev_data[6]]
        m.location = [marker.location[0], marker.location[1]]
        html_content = m.get_root().render()
        self.load_html_content(html_content, QUrl.fromLocalFile(os.path.abspath('')))


if __name__ == "__main__":
    prev_data = []

    m = folium.Map(location=[55.9297334, 37.6173], zoom_start=10)
    marker = folium.Marker(location=[55.9297334, 37.6173], popup='Мое местоположение')
    marker.add_to(m)
    m.save('index.html')

    app = QApplication(sys.argv)
    mainWindow = TelemetriaWindow()
    mainWindow.show()
    sys.exit(app.exec_())
