import time
import datetime
import statistics

from task import *
from scheduler import *

from rs485 import *
from mqtt_client import *
from config import *

class SCH_Controller:
    def __init__(self, scheduler):
        self.fertilizer_id1 = "0"
        self.fertilizer_id2 = "0"
        self.fertilizer_id3 = "0"
        self.area_id4 = "0"
        self.area_id5 = "0"
        self.area_id6 = "0"
        self.circle = "0"   
        self.start_time = "0" 
        self.end_time = "0"
        self.adjusted_end_time = None
        self.client1 = None
        self.client2 = None
        self.counter = 10
        self.state = "IDLE"
        self.previous_state_start_time = datetime.datetime.now()

        self.moisture_readings = []
        self.temperature_readings = []
        
        self.scheduler = Scheduler() # khoi tao scheduler

    # ===============================================
    # ======== TK 111111 ============================

    def connected_tk1(self, client1):
        print("Ket noi thanh cong ...")
        for topic in AIO_FEED_IDs_1:
            client1.subscribe(topic)

    def subscribe_tk1(self, client1, userdata, mid, granted_qos):
        print("Subscribe thanh cong ...")

    def disconnected_tk1(self, client1):
        print("Ngat ket noi ...")
        sys.exit(1)

    def message_handler_tk1(self, client1, feed_id, payload):
        if feed_id == "fertilizer-id1":
            self.fertilizer_id1 = payload
            print("fer_id1", self.fertilizer_id1)
        elif feed_id == "fertilizer-id2":
            self.fertilizer_id2 = payload
            print("fer_id2", self.fertilizer_id2)
        elif feed_id == "fertilizer-id3":
            self.fertilizer_id3 = payload
            print("fer_id3", self.fertilizer_id3)
        elif feed_id == "area-id4":
            self.area_id4 = payload
            print("area_id4", self.area_id4)
        elif feed_id == "area-id5":
            self.area_id5 = payload
            print("area_id5", self.area_id5)
        elif feed_id == "area-id6":
            self.area_id6 = payload
            print("area_id6", self.area_id6)
        elif feed_id == "circle":
            self.circle = payload
            print("circle", self.circle)
        elif feed_id == "clock":
            self.start_time, self.end_time = payload.split(" - ")
            print("Start time:", self.start_time)
            print("End time:", self.end_time)

            self.end_time = datetime.datetime.strptime(self.end_time, "%H:%M")
            circle_timedelta = datetime.timedelta(minutes=int(self.circle))
            self.adjusted_end_time = self.end_time - circle_timedelta

    # ===============================================
    # ======== TK 22222 ============================

    def connected_tk2(self, client2):
        print("Ket noi thanh cong ...")
        for topic in AIO_FEED_IDs_2:
            client2.subscribe(topic)

    def subscribe_tk2(self, client2, userdata, mid, granted_qos):
        print("Subscribe thanh cong ...")

    def disconnected_tk2(self, client2):
        print("Ngat ket noi ...")
        sys.exit(1)

    def message_tk2(self, client2 , feed_id , payload):
        # print("Nhan du lieu: " + payload + ", feed id: " + feed_id)
        print("")

    # ==============================================
    # ======= FILTER DATA ==========================

    # thêm giá trị mới vào danh sách và loại bỏ giá trị cũ nhất 
    # nếu danh sách đã đạt đến độ dài tối đa.
    def add_reading(self, readings, new_reading, max_len=10):
        if len(readings) >= max_len:
            readings.pop(0)
        readings.append(new_reading)

    # kiểm tra xem giá trị mới có nằm trong phạm vi chấp nhận được không 
    # dựa trên trung bình và phương sai của các giá trị trước đó.
    def is_within_variance(self, readings, new_reading, threshold=3.0):
        if len(readings) < 5:  # Not enough data to compare variance
            return True
        mean = statistics.mean(readings)
        variance = statistics.variance(readings)
        return abs(new_reading - mean) <= threshold * variance

    # lọc và gửi dữ liệu 
    def update_soil_sensor(self):
        new_moisture = readMoisture()
        new_temperature = readTemperature()

        # Filter moisture readings
        if self.is_within_variance(self.moisture_readings, new_moisture) and new_moisture != 0:
            self.add_reading(self.moisture_readings, new_moisture)
            print("moisture: ", new_moisture)
            self.client2.publish("soil-moisture", new_moisture)
        else:
            print("moisture reading out of variance: ", new_moisture)

        # Filter temperature readings
        if self.is_within_variance(self.temperature_readings, new_temperature) and new_temperature != 0:
            self.add_reading(self.temperature_readings, new_temperature)
            print("soil temp: ", new_temperature)
            self.client2.publish("temperature", new_temperature)
        else:
            print("temperature reading out of variance: ", new_temperature)

    # =====================================
    # =====================================

    def run(self):
        # gọi hàm process_state
        self.scheduler.SCH_Init()
        # self.scheduler.SCH_Add_Task(self.update_soil_sensor, 0, 30000) #delay = 0, period = 1s
        self.scheduler.SCH_Add_Task(self.process_state, 0, 1000)  # delay = 0, period = 10s
        while True:
            self.scheduler.SCH_Update() 
            self.scheduler.SCH_Dispatch_Tasks()
            # time.sleep(0.1) # 100ms
            time.sleep(1) # 1s

    # ========= FSM ============================
    def process_state(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        if self.state == "IDLE":
            print("STATE IDLE")
            self.client1.publish("notification", 0)

            if current_time == self.start_time:
                self.state = "MIXER_1"
                self.client1.publish("active", 1)
                self.previous_state_start_time = now

        elif self.state == "MIXER_1":
            print("STATE MIXER_1")
            self.client1.publish("notification", 1)
            setMixer1(True)
            elapsed_time = (now - self.previous_state_start_time).total_seconds()
            if int(readFlow()) >= int(self.fertilizer_id1) or elapsed_time >= int(self.fertilizer_id1) / 2:
                setMixer1(False)
                self.state = "MIXER_2"
                self.previous_state_start_time = now

        elif self.state == "MIXER_2":
            print("STATE MIXER_2")
            self.client1.publish("notification", 2)
            setMixer2(True)
            elapsed_time = (now - self.previous_state_start_time).total_seconds()
            if int(readFlow()) >= int(self.fertilizer_id2) or elapsed_time >= int(self.fertilizer_id2) / 2:
                setMixer2(False)
                self.state = "MIXER_3"
                self.previous_state_start_time = now

        elif self.state == "MIXER_3":
            print("STATE MIXER_3")
            self.client1.publish("notification", 3)
            setMixer3(True)
            elapsed_time = (now - self.previous_state_start_time).total_seconds()
            if int(readFlow()) >= int(self.fertilizer_id3) or elapsed_time >= int(self.fertilizer_id3) / 2:
                setMixer3(False)
                self.state = "PUMP_IN"
                self.previous_state_start_time = now

        elif self.state == "PUMP_IN":
            print("STATE PUMP_IN")
            self.client1.publish("notification", 4)
            setPumpIn(True)
            elapsed_time = (now - self.previous_state_start_time).total_seconds()
            if int(readSonar()) <= 100 or elapsed_time >= 60:
                setPumpIn(False)
                self.state = "SELECTOR"
                self.previous_state_start_time = now

        elif self.state == "SELECTOR":
            print("STATE SELECTOR")
            if self.area_id4 == "1":
                setSelector4(True)
            if self.area_id5 == "1":
                setSelector5(True)
            if self.area_id6 == "1":
                setSelector6(True)

            elapsed_time = (now - self.previous_state_start_time).total_seconds()
            if self.area_id4 == "1" or self.area_id5 == "1" or self.area_id6 == "1":
                self.state = "PUMP_OUT"
                self.previous_state_start_time = now
            if elapsed_time >= 60:
                self.state = "IDLE"

        elif self.state == "PUMP_OUT":
            print("STATE PUMP_OUT")
            self.client1.publish("notification", 5)
            setPumpOut(True)
            elapsed_time = (now - self.previous_state_start_time).total_seconds()
            if int(readSonar()) >= 200 or elapsed_time >= 60:
                setPumpOut(False)
                self.state = "NEXT_CYCLE"
                self.previous_state_start_time = now

        elif self.state == "NEXT_CYCLE":
            print("STATE NEXT_CYCLE")
            setMixer1(False)
            setMixer2(False)
            setMixer3(False)
            setSelector4(False)
            setSelector5(False)
            setSelector6(False)
            setPumpOut(False)
            setPumpIn(False)

            if now.time() <= self.adjusted_end_time.time():
                self.client1.publish("notification", 1)
                self.state = "MIXER_1"
            else:
                self.client1.publish("notification", 6)
                self.client1.publish("active", 0)
                self.state = "IDLE"

# controller.py

def create_clients(controller):
    controller.client1 = create_mqtt_client(
        AIO_USERNAME_1, AIO_KEY_1,
        controller.connected_tk1, 
        controller.disconnected_tk1, 
        controller.message_handler_tk1, 
        controller.subscribe_tk1
    )
    controller.client2 = create_mqtt_client(
        AIO_USERNAME_2, AIO_KEY_2, 
        controller.connected_tk2, 
        controller.disconnected_tk2, 
        controller.message_tk2, 
        controller.subscribe_tk2
    )

