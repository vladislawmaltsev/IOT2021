import random
import threading
import time
import json

from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
port = 1883
topic1 = "vmk/team/r"
topic2 = "vmk/team/c"
client_id = f'python-mqtt-0'
worker_id = f'python-mqtt-1'

publisher = mqtt_client.Client('5')
publisher.connect(broker, port)

def connect_mqtt(id, broker) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            print(broker)
            pass
        else:
            pass
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(id)
    return client

light_publisher = connect_mqtt()
light_publisher.loop_start()

sensors_per = []

def on_message(client, userdata, msg):
    from ast import literal_eval
    import json
    data = literal_eval(msg.payload.decode('utf8'))
    global sensors_per
    sensors_per = data
    print(sensors_per)
    print('Incoming message topic: ' + msg.topic)

    if msg.topic.startswith('tb/mqtt-integration-work/sensors/Sensor-1/rx/twoway'):
        #print('This is two way call, responding now')
        responseMsg = "{\"value\":\"200\"}"
        #print('Sending a response message: ' + responseMsg)
        publisher.publish("vmk/team/c", json.dumps(responseMsg))

        if len(sensors_per) == 2:
            client.publish(topicTelemetry,  sensors_per[0])
            client.publish('v1/devices/me/rpc/response/1',sensors_per[0])
        return

def subscribe(client: mqtt_client):
    client.subscribe(topic1)
    client.on_message = on_message

def publish(client):
    while True:
        if len(sensors_per) == 2:
            result = client.publish(topicTelemetry, json.dumps(sensors_per[0]))
            #print("PUBLISHING LIGHT: ", json.dumps(sensors_per[0]))
        time.sleep(30)

def publishHumidity(client):
    while True:
        if len(sensors_per) == 2:
            result = client.publish(topicTelemetry, json.dumps(sensors_per[1]))
            #print("PUBLISHING HUMIDITY: ", json.dumps(sensors_per[1]))
        time.sleep(30)

def publishTemp(client):
    while True:
        if len(sensors_per) == 3:
            result = client.publish(topicTelemetry, json.dumps(sensors_per[2]))
            #print("PUBLISHING HUMIDITY: ", json.dumps(sensors_per[1]))
        time.sleep(30)


def publishPressure(client):
    while True:
        if len(sensors_per) == 4:
            result = client.publish(topicTelemetry, json.dumps(sensors_per[3]))
            #print("PUBLISHING HUMIDITY: ", json.dumps(sensors_per[1]))
        time.sleep(30)

def run():
    import threading
    thread1 = threading.Thread(target=publish, args=[light_publisher])
    thread1.start()
    client = connect_mqtt('2', broker)
    subscribe(client)
    thread2 = threading.Thread(target=publishHumidity, args=[clientHumidity])
    thread2.start()
    thread3 = threading.Thread(target=publishHumidity, args=[clientTemp])
    thread3.start()
    thread4 = threading.Thread(target=publishHumidity, args=[clientPressure])
    thread4.start()
    clientHumidity = connect_mqtt('2', broker)
    subscribe(clientHumidity)
    clientHumidity.loop_forever()
    client.loop_forever()

def exec():
    run()

if __name__ == "__main__":
    exec()