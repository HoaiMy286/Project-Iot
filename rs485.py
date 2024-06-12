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
except:
    print("Cannot open the port")

def serial_read_data(ser, expected_id, expected_response_size=7, timeout=2):
    start_time = time.time()
    buffer = []

    while time.time() - start_time < timeout:
        bytesToRead = ser.inWaiting()
        if bytesToRead > 0:
            out = ser.read(bytesToRead)
            buffer.extend(out)
            print(f"Buffer: {buffer}")
            
            if len(buffer) >= expected_response_size:
                if buffer[0] == expected_id:
                    value = buffer[-4] * 256 + buffer[-3]
                    return value
    
    return -1

# ==================================================
# =========     TEMP          ======================

soil_temperature = [10, 3, 0, 6, 0, 1, 101, 112]
def readTemperature():
    serial_read_data(ser, expected_id=10)
    ser.write(bytearray(soil_temperature))
    time.sleep(1)
    return serial_read_data(ser, expected_id=10) / 100

# ==================================================
# =========     SOIL MOISTURE        ===============

soil_moisture = [10, 3, 0, 7, 0, 1, 52, 176]
def readMoisture():
    serial_read_data(ser, expected_id=10)
    ser.write(bytearray(soil_moisture))
    time.sleep(1)
    return serial_read_data(ser, expected_id=10) / 100

# ==================================================
# =========     FLOW SENSOR       ==================

def readFlow():
    return 40

# ==================================================
# =========     SONAR SENSOR        ================

def readSonar():
    return 1

# ==================================================
# =========     MIXER 1        =====================

mixer1_ON  = [1, 6, 0, 0, 0, 255, 201, 138]
mixer1_OFF = [1, 6, 0, 0, 0, 0, 137, 202]

def setMixer1(state):
    if state:
        ser.write(bytearray(mixer1_ON))
    else:
        ser.write(bytearray(mixer1_OFF))
    time.sleep(1)
    print(serial_read_data(ser, expected_id=1))

# ==================================================
# =========     MIXER 2        =====================

mixer2_ON  = [2, 6, 0, 0, 0, 255, 201, 185]
mixer2_OFF = [2, 6, 0, 0, 0, 0, 137, 249]

def setMixer2(state):
    if state:
        ser.write(bytearray(mixer2_ON))
    else:
        ser.write(bytearray(mixer2_OFF))
    time.sleep(1)
    print(serial_read_data(ser, expected_id=2))

# ==================================================
# =========     MIXER 3        =====================

mixer3_ON  = [3, 6, 0, 0, 0, 255, 200, 104]
mixer3_OFF = [3, 6, 0, 0, 0, 0, 136, 40]

def setMixer3(state):
    if state:
        ser.write(bytearray(mixer3_ON))
    else:
        ser.write(bytearray(mixer3_OFF))
    time.sleep(1)
    print(serial_read_data(ser, expected_id=3))

# ==================================================
# =========     SELECTOR 4        ==================

selector4_ON  = [4, 6, 0, 0, 0, 255, 201, 223]
selector4_OFF = [4, 6, 0, 0, 0, 0, 137, 159]

def setSelector4(state):
    if state:
        ser.write(bytearray(selector4_ON))
    else:
        ser.write(bytearray(selector4_OFF))
    time.sleep(1)
    print(serial_read_data(ser, expected_id=4))

# ==================================================
# =========     SELECTOR 5        ==================

selector5_ON  = [5, 6, 0, 0, 0, 255, 200, 14]
selector5_OFF = [5, 6, 0, 0, 0, 0, 136, 78]

def setSelector5(state):
    if state:
        ser.write(bytearray(selector5_ON))
    else:
        ser.write(bytearray(selector5_OFF))
    time.sleep(1)
    print(serial_read_data(ser, expected_id=5))

# ==================================================
# =========     SELECTOR 6        ==================

selector6_ON  = [6, 6, 0, 0, 0, 255, 200, 61]
selector6_OFF = [6, 6, 0, 0, 0, 0, 136, 125]

def setSelector6(state):
    if state:
        ser.write(bytearray(selector6_ON))
    else:
        ser.write(bytearray(selector6_OFF))
    time.sleep(1)
    print(serial_read_data(ser, expected_id=6))

# ==================================================
# =========     PUMP IN 7         ==================

pumpin_ON  = [7, 6, 0, 0, 0, 255, 201, 236]
pumpin_OFF = [7, 6, 0, 0, 0, 0, 137, 172]

def setPumpIn(state):
    if state:
        ser.write(bytearray(pumpin_ON))
    else:
        ser.write(bytearray(pumpin_OFF))
    time.sleep(1)
    print(serial_read_data(ser, expected_id=7))

# ==================================================
# =========     PUMP OUT 8        ==================

pumpout_ON  = [8, 6, 0, 0, 0, 255, 201, 19]
pumpout_OFF = [8, 6, 0, 0, 0, 0, 137, 83]

def setPumpOut(state):
    if state:
        ser.write(bytearray(pumpout_ON))
    else:
        ser.write(bytearray(pumpout_OFF))
    time.sleep(1)
    print(serial_read_data(ser, expected_id=8))

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
#     print("flow:")
#     print(readFlow())
#     time.sleep(2)

#     print("sonar:")
#     print(readSonar())
#     time.sleep(2)