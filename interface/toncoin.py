from serial_read import read_from_com_port
import time, os, sys, serial, ctypes
import folium
import numpy as np
from pyqtgraph import PlotWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QHBoxLayout, QLineEdit
from PyQt5.QtCore import QTimer, QDateTime, Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap


if __name__ == "__main__":
    while True:
        values = read_from_com_port("COM11", 115200, timeout1=2, write_timeout1=2)


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
        print(log_string)