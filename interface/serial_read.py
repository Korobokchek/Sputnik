import serial


def read_from_com_port(port, baudrate, timeout=1):
    ser = serial.Serial(port, baudrate, timeout=timeout)
    try:
        if ser.isOpen():
            print(f"Соединение установлено на порте {port}")
            while True:
                data = ser.readline().decode().strip()
                # data = ser.readline().strip()
                if data:
                    print("Принято:", data)
    except serial.SerialException as e:
        print("Произошла ошибка при открытии порта:", e)
    finally:
        ser.close()


if __name__ == "__main__":
    port = 'COM11'
    baudrate = 115200
    read_from_com_port(port, baudrate)