import time
import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

print(getPort())

try:
    ser = serial.Serial(port=getPort(), baudrate=9600)
    print("Open successfully")
except Exception as e:
    print("Cannot open the port:", e)

def serial_read_data(ser, expected_id=None, max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        time.sleep(1)  # Thời gian chờ trước khi đọc
        bytesToRead = ser.inWaiting()
        if bytesToRead > 0:
            out = ser.read(bytesToRead)
            data_array = [b for b in out]
            print(f"Attempt {attempts}, Data received: {data_array}")
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                if expected_id is not None:
                    if data_array[0] == expected_id:
                        return value
                    else:
                        print(f"Unexpected ID: {data_array[0]}, expected: {expected_id}")
                else:
                    return value
    print("Max attempts reached, did not receive expected ID")
    return -1

def clear_buffer(ser):
    while ser.inWaiting() > 0:
        ser.read(ser.inWaiting())

# ==================================================
# =========     TEMP          ======================

soil_temperature = [10, 3, 0, 6, 0, 1, 101, 112]
def readTemperature():
    clear_buffer(ser)  # Xóa dữ liệu cũ
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser, expected_id=10) / 100

# ==================================================
# =========     SOIL MOISTURE        ===============

soil_moisture = [10, 3, 0, 7, 0, 1, 52, 176]
def readMoisture():
    clear_buffer(ser)  # Xóa dữ liệu cũ
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser, expected_id=10) / 100

# ==================================================
# =========     MIXER 1        =====================

mixer1_ON  = [1, 6, 0, 0, 0, 255, 201, 138]
mixer1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

def setMixer1(state):
    clear_buffer(ser)  # Xóa dữ liệu cũ
    if state:
        ser.write(mixer1_ON)
    else:
        ser.write(mixer1_OFF)
    time.sleep(1)
    print(serial_read_data(ser, expected_id=1))

# ==================================================
# =========     MIXER 2        =====================

mixer2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
mixer2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

def setMixer2(state):
    clear_buffer(ser)  # Xóa dữ liệu cũ
    if state:
        ser.write(mixer2_ON)
    else:
        ser.write(mixer2_OFF)
    time.sleep(1)
    print(serial_read_data(ser, expected_id=2))

# ==================================================
# =========     MIXER 3        =====================

mixer3_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
mixer3_OFF = [3, 6, 0, 0, 0, 0, 136, 40]

def setMixer3(state):
    clear_buffer(ser)  # Xóa dữ liệu cũ
    if state:
        ser.write(mixer3_ON)
    else:
        ser.write(mixer3_OFF)
    time.sleep(1)
    print(serial_read_data(ser, expected_id=3))

# ==================================================
# =========     SELECTOR 4        ==================

selector4_ON  = [4, 6, 0, 0, 0, 255, 201, 223]
selector4_OFF = [4, 6, 0, 0, 0, 0, 137, 159]

def setSelector4(state):
    clear_buffer(ser)  # Xóa dữ liệu cũ
    if state:
        ser.write(selector4_ON)
    else:
        ser.write(selector4_OFF)
    time.sleep(1)
    print(serial_read_data(ser, expected_id=4))

# ==================================================
# =========     SELECTOR 5        ==================

selector5_ON  = [5, 6, 0, 0, 0, 255, 200, 14]
selector5_OFF = [5, 6, 0, 0, 0, 0, 136, 78]

def setSelector5(state):
    clear_buffer(ser)  # Xóa dữ liệu cũ
    if state:
        ser.write(selector5_ON)
    else:
        ser.write(selector5_OFF)
    time.sleep(1)
    print(serial_read_data(ser, expected_id=5))

# ==================================================
# =========     SELECTOR 6        ==================

selector6_ON  = [6, 6, 0, 0, 0, 255, 200, 61]
selector6_OFF = [6, 6, 0, 0, 0, 0, 136, 125]

def setSelector6(state):
    clear_buffer(ser)  # Xóa dữ liệu cũ
    if state:
        ser.write(selector6_ON)
    else:
        ser.write(selector6_OFF)
    time.sleep(1)
    print(serial_read_data(ser, expected_id=6))

# ==================================================
# =========     PUMP IN 7         ==================

pumpin_ON  = [7, 6, 0, 0, 0, 255, 201, 236]
pumpin_OFF = [7, 6, 0, 0, 0, 0, 137, 172]

def setPumpIn(state):
    clear_buffer(ser)  # Xóa dữ liệu cũ
    if state:
        ser.write(pumpin_ON)
    else:
        ser.write(pumpin_OFF)
    time.sleep(1)
    print(serial_read_data(ser, expected_id=7))

# ==================================================
# =========     PUMP OUT 8        ==================

pumpout_ON  = [8, 6, 0, 0, 0, 255, 201, 19]
pumpout_OFF = [8, 6, 0, 0, 0, 0, 137, 83]

def setPumpOut(state):
    clear_buffer(ser)  # Xóa dữ liệu cũ
    if state:
        ser.write(pumpout_ON)
    else:
        ser.write(pumpout_OFF)
    time.sleep(1)
    print(serial_read_data(ser, expected_id=8))

# Test
# while True:
#     print("MIXER 1")
#     setMixer1(True)
#     time.sleep(2)
#     setMixer1(False)
#     time.sleep(2)

#     print("MIXER 2")
#     setMixer2(True)
#     time.sleep(2)
#     setMixer2(False)
#     time.sleep(2)

    # print("soil moisture:")
    # print(readMoisture())
    # time.sleep(2)

    # print("temp: ")
    # print(readTemperature())
    # time.sleep(2)
