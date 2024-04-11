import serial


def read_from_com_port(port, baudrate, timeout1=2, write_timeout1=2):
    ser = serial.Serial(port, baudrate, timeout=timeout1, write_timeout=write_timeout1)
    try:
        if ser.isOpen():
            print(f"Соединение установлено на порте {port}")
            while True:
                data = ser.readline().decode().strip().split(';')
                if data:
                    # print("Принято:", data)
                    return data
    except serial.SerialException as e:
        print("Произошла ошибка при открытии порта:", e)
    finally:
        ser.close()


if __name__ == "__main__":
    port = 'COM11'
    baudrate = 115200
    while True:
        print(read_from_com_port(port, baudrate))