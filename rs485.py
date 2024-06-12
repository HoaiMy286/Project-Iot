import time
import serial.tools.list_ports
import serial

# Hàm để lấy cổng COM của thiết bị
def getPort():
    ports = serial.tools.list_ports.comports()
    commPort = None
    for port in ports:
        if "USB" in port.description:  # Kiểm tra cổng COM có chứa "USB" trong mô tả
            commPort = port.device
    return commPort

# Khởi tạo kết nối serial
ser = serial.Serial(port=getPort(), baudrate=9600)

# Hàm đọc dữ liệu từ buffer serial
def read_serial_buffer():
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        return data_array
    return []

# Hàm gửi phản hồi cho đến khi nhận được giá trị mong muốn (bật hoặc tắt)
def send_feedback(expected_id, expected_response_size=7, timeout=2):
    start_time = time.time()
    buffer = []

    while time.time() - start_time < timeout:
        data_array = read_serial_buffer()
        if data_array:
            buffer.extend(data_array)
            print(f"Buffer: {buffer}")
            if len(buffer) >= expected_response_size and buffer[0] == expected_id:
                value = buffer[-4] * 256 + buffer[-3]
                return value
    return -1

# ==================================================
# =========     TEMP          ======================

soil_temperature = [10, 3, 0, 6, 0, 1, 101, 112]
def readTemperature():
    ser.write(bytearray(soil_temperature))
    return send_feedback(expected_id=10) / 100

# ==================================================
# =========     SOIL MOISTURE        ===============

soil_moisture = [10, 3, 0, 7, 0, 1, 52, 176]
def readMoisture():
    ser.write(bytearray(soil_moisture))
    return send_feedback(expected_id=10) / 100

# ==================================================
# =========     MIXER 1        =====================

mixer1_ON  = [1, 6, 0, 0, 0, 255, 201, 138]
mixer1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

def setMixer1(state):
    if state:
        ser.write(bytearray(mixer1_ON))
    else:
        ser.write(bytearray(mixer1_OFF))
    print(send_feedback(expected_id=1))

# ==================================================
# =========     MIXER 2        =====================

mixer2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
mixer2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

def setMixer2(state):
    if state:
        ser.write(bytearray(mixer2_ON))
    else:
        ser.write(bytearray(mixer2_OFF))
    print(send_feedback(expected_id=2))

# ==================================================
# =========     PUMP IN        =====================

pumpin_ON  = [7, 6, 0, 0, 0, 255, 201, 236]
pumpin_OFF = [7, 6, 0, 0, 0, 0, 137, 172]

def setPumpIn(state):
    if state:
        ser.write(bytearray(pumpin_ON))
    else:
        ser.write(bytearray(pumpin_OFF))
    print(send_feedback(expected_id=7))

# ==================================================
# =========     PUMP OUT        =====================

pumpout_ON  = [8, 6, 0, 0, 0, 255, 201, 19]
pumpout_OFF = [8, 6, 0, 0, 0, 0, 137, 83]

def setPumpOut(state):
    if state:
        ser.write(bytearray(pumpout_ON))
    else:
        ser.write(bytearray(pumpout_OFF))
    print(send_feedback(expected_id=8))

while True:
    print("MIXER 1")
    setMixer1(True)
    time.sleep(2)
    setMixer1(False)
    time.sleep(2)
