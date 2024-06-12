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
    # return "/dev/ttyUSB1"

# portName = "COM3"
# portName = getPort()
print(getPort())

try:
    ser = serial.Serial(port=getPort(), baudrate=9600)
    print("Open successfully")
except:
    print("Can not open the port")

# đọc dữ liệu từ cổng nối tiếp, xử lý nó và trả về một giá trị cụ thể.
def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

# ==================================================
# =========     TEMP          ======================

soil_temperature = [10, 3, 0, 6, 0, 1, 101, 112]
def readTemperature():
    # kiểm tra và xóa bộ đệm dữ liệu cũ (nếu có) 
    # trước khi gửi yêu cầu mới.
    serial_read_data(ser)
    # yêu cầu đọc giá trị nhiệt độ từ thiết bị Modbus.
    ser.write(soil_temperature)
    time.sleep(1)
    # đọc dữ liệu trả về từ thiết bị. 
    # Giá trị trả về từ hàm này sẽ là kết quả đọc được từ thiết bị.
    return serial_read_data(ser)/100

# ==================================================
# =========     SOIL MOISTURE        ===============

soil_moisture = [10, 3, 0, 7, 0, 1, 52, 176]
def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)/100

# ==================================================
# =========     FLOW SENSOR       ==================

# flow_sensor = [1, 3, 0, 1, 0, 1, 213, 202]
def readFlow():
    # serial_read_data(ser)
    # ser.write(flow_sensor)
    # time.sleep(1)
    # return serial_read_data(ser)
    return 40

# ==================================================
# =========     SONAR SENSOR        ================

# sonar_sensor = [1, 3, 0, 2, 0, 1, 37, 202]
def readSonar():
    # serial_read_data(ser)
    # ser.write(sonar_sensor)
    # time.sleep(1)
    # return serial_read_data(ser)
    return 1

# ==================================================
# =========     MIXER 1        =====================

mixer1_ON  = [1, 6, 0, 0, 0, 255, 201, 138]
mixer1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

def setMixer1(state):
    if state == True:
        ser.write(mixer1_ON)
    else:
        ser.write(mixer1_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

# ==================================================
# =========     MIXER 2        =====================

mixer2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
mixer2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

def setMixer2(state):
    if state == True:
        ser.write(mixer2_ON)
    else:
        ser.write(mixer2_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

# ==================================================
# =========     MIXER 3        =====================

mixer3_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
mixer3_OFF = [3, 6, 0, 0, 0, 0, 136, 40]

def setMixer3(state):
    if state == True:
        ser.write(mixer3_ON)
    else:
        ser.write(mixer3_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

# ==================================================
# =========     SELECTOR 4        ==================

selector4_ON  = [4, 6, 0, 0, 0, 255, 201, 223]
selector4_OFF = [4, 6, 0, 0, 0, 0, 137, 159]

def setSelector4(state):
    if state == True:
        ser.write(selector4_ON)
    else:
        ser.write(selector4_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

# ==================================================
# =========     SELECTOR 5        ==================

selector5_ON  = [5, 6, 0, 0, 0, 255, 200, 14]
selector5_OFF = [5, 6, 0, 0, 0, 0, 136, 78]

def setSelector5(state):
    if state == True:
        ser.write(selector5_ON)
    else:
        ser.write(selector5_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

# ==================================================
# =========     SELECTOR 5        ==================

selector6_ON  = [6, 6, 0, 0, 0, 255, 200, 61]
selector6_OFF = [6, 6, 0, 0, 0, 0, 136, 125]

def setSelector6(state):
    if state == True:
        ser.write(selector6_ON)
    else:
        ser.write(selector6_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

# ==================================================
# =========     PUMP IN 7         ==================

pumpin_ON  = [7, 6, 0, 0, 0, 255, 201, 236]
pumpin_OFF = [7, 6, 0, 0, 0, 0, 137, 172]

def setPumpIn(state):
    if state == True:
        ser.write(pumpin_ON)
    else:
        ser.write(pumpin_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

# ==================================================
# =========     PUMP OUT 8        ==================

pumpout_ON  = [8, 6, 0, 0, 0, 255, 201, 19]
pumpout_OFF = [8, 6, 0, 0, 0, 0, 137, 83]

def setPumpOut(state):
    if state == True:
        ser.write(pumpout_ON)
    else:
        ser.write(pumpout_OFF)
    time.sleep(1)
    print(serial_read_data(ser))

while True:
    print("MIXER 1")
    setMixer1(True)
    time.sleep(2)
    setMixer1(False)
    time.sleep(2)

#     print("soil moisture:")
#     print(readMoisture())
#     time.sleep(2)

#     print("temp: ")
#     print(readTemperature())
#     time.sleep(2)

#     print("MIXER 2")
#     setMixer2(True)
#     time.sleep(2)
#     setMixer2(False)
#     time.sleep(2)

#     print("MIXER 3")
#     setMixer3(True)
#     time.sleep(2)
#     setMixer3(False)
#     time.sleep(2)

#     print("SELECTOR 1")
#     setSelector4(True)
#     time.sleep(2)
#     setSelector4(False)
#     time.sleep(2)

#     print("SELECTOR 2")
#     setSelector5(True)
#     time.sleep(2)
#     setSelector5(False)
#     time.sleep(2)

#     print("SELECTOR 3")
#     setSelector6(True)
#     time.sleep(2)
#     setSelector6(False)
#     time.sleep(2)

#     print("PUMP IN")
#     setPumpIn(True)
#     time.sleep(2)
#     setPumpIn(False)
#     time.sleep(2)

#     print("PUMP OUT")
#     setPumpOut(True)
#     time.sleep(2)
#     setPumpOut(False)
#     time.sleep(2)


# while True:
#     print("TEST SENSOR")

# #     print("flow:")
# #     print(readFlow())
# #     time.sleep(2)

# #     print("sonar:")
# #     print(readSonar())
# #     time.sleep(2)
