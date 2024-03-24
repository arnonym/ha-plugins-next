# mqtt.py
import paho.mqtt.client as mqtt
from command_client import CommandClient

class MQTTClient:
    def __init__(self, broker_address, port, username, password, topic, command_handler):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.broker_address = broker_address
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.command_handler = command_handler

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)

    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        command_list = CommandClient.list_to_json([msg.payload])
        for command in command_list:
            self.command_handler.handle_command(command, None)

    def connect(self):
        self.client.connect(self.broker_address, self.port, 60)

    def loop(self):
        self.client.loop()