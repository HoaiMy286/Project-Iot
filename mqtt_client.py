from Adafruit_IO import MQTTClient
import sys

def create_mqtt_client(username, key, on_connect, on_disconnect, on_message, on_subscribe):
    client = MQTTClient(username, key)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.connect()
    client.loop_background()
    return client
