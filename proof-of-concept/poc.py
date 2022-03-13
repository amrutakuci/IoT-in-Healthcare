import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import time
import board
import adafruit_dht
import psutil
# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D23)

def helloworld(self,params,packet):
    print('Received Message from AWS IoT core')
    print('Topic: ' + packet.topic)
    print('Payload : ', (packet.payload))
myMQTTClient = AWSIoTMQTTClient("iotid")
myMQTTClient.configureEndpoint("a9tnrtc4mez4n-ats.iot.us-east-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials("/home/pi/Documents/Amruta/root.pem","/home/pi/Documents/Amruta/private.pem.key","/home/pi/Documents/Amruta/certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
print('Initializing IoT core topic')
myMQTTClient.connect()

myMQTTClient.subscribe("home/helloworld", 1, helloworld)


while True:
    try:
        temp = sensor.temperature
        humidity = sensor.humidity
        print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
        json_data = { "temperature" : temp, "humidity" : humidity}
        myMQTTClient.publish('home/data',json.dumps(json_data),1)
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error
    time.sleep(5)
    
