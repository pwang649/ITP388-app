from flask import Flask, render_template, request
from flask_mqtt import Mqtt
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_KEEPALIVE'] = 60  # set the time interval for sending a ping to the broker to 60 seconds

mqtt = Mqtt(app)

@mqtt.on_connect()
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))
    # subscribe to topics of interest here

# Default message callback. Please use custom callbacks.
@mqtt.on_message()
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

@app.route("/")
def home():
    return render_template("index.html")

# GET request endpoint 2
@app.route("/send", methods=["POST", "GET"])
def send():
    msg = ''
    if 'Message' in request.args.keys():
        msg = request.args['Message']
        mqtt.publish("ITP388/test", msg)
        #client.publish("ITP388/test", msg)
    return render_template("index.html", returnMsg=msg)

#
# if __name__ == "__main__":
#     # this section is covered in publisher_and_subscriber_example.py
#     client = mqtt.Client()
#     client.on_message = on_message
#     client.on_connect = on_connect
#     client.connect(host="broker.hivemq.com", port=1883, keepalive=60)
#     client.loop_start()