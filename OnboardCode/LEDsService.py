import threading

import paho.mqtt.client as mqtt

import time
import board
import neopixel
import RPi.GPIO as GPIO



LEDSequenceOn = False


def led_sequence():
    global op_mode
    global LEDSequenceOn

    if op_mode == 'simulation':

        while LEDSequenceOn:
            print("RED")
            time.sleep(1)
            print("GREEN")
            time.sleep(1)
            print("YELLOW")
            time.sleep(1)
    else:
        while LEDSequenceOn:
            pixels[0] = (255, 0, 0)
            time.sleep(1)
            pixels[0] = (0, 255, 0)
            time.sleep(1)
            pixels[0] = (255, 255, 0)
            time.sleep(1)

def on_message(client, userdata, message):
    global LEDSequenceOn
    splited = message.topic.split("/")
    origin = splited[0]
    destination = splited[1]
    command = splited[2]
    print ('LEDs recibo ', message.topic)

    if command == "startLEDsSequence":
        print("Start LED sequence")
        LEDSequenceOn = True
        w = threading.Thread(target=led_sequence)
        w.start()

    if command == "stopLEDsSequence":
        print("Stop LED sequence")
        LEDSequenceOn = False

    if command == "LEDsSequenceForNSeconds":
        seconds = int(message.payload.decode("utf-8"))
        print("LED sequence for " + str(seconds) + " seconds")
        LEDSequenceOn = True
        w = threading.Thread(target=led_sequence)
        w.start()
        time.sleep(int(seconds))
        LEDSequenceOn = False

    if op_mode == 'simulation':
        if command == 'red':
            print('RED')
            time.sleep(5)
            print ('CLEAR')

        if command == 'green':
            print('GREEN')
            time.sleep(5)
            print('CLEAR')

        if command == 'blue':
            print('BLUE')
            time.sleep(5)
            print('CLEAR')

        if command == 'drop':
            print('DROP')

        if command == 'reset':
            print ('RESET')

        if command == 'bluei':
            print('BLUE')
        if command == 'redi':
            print('RED')
        if command == 'greeni':
            print('GREEN')
        if command == 'yellowi':
            print('YELLOW')
        if command == 'pinki':
            print('PINK')
        if command == 'whitei':
            print('WHITE')
        if command == 'blacki':
            print('BLACK')
        if command == 'clear':
            print('CLEAR')
    else:
        if command == 'red':
            pixels[0] = (255, 0, 0)
            time.sleep(5)
            pixels[0] = (0, 0, 0)

        if command == 'green':
            pixels[1] = (0, 255, 0)
            time.sleep(5)
            pixels[1] = (0, 0, 0)

        if command == 'blue':
            pixels[2] = (0, 0, 255)
            time.sleep(5)
            pixels[2] = (0, 0, 0)

        if command == 'drop':
            print ('drop real')
            p.ChangeDutyCycle(7.5)
            time.sleep (1)
            p.ChangeDutyCycle(2)


        if command == 'reset':
            p.ChangeDutyCycle(2.5)
        if command == 'bluei':
            pixels[0] = (0, 0, 255)
        if command == 'redi':
            pixels[0] = (107, 0, 0)
        if command == 'greeni':
            pixels[0] = (0, 255, 0)
        if command == 'yellowi':
            pixels[0] = (255, 255, 0)
        if command == 'pinki':
            pixels[0] = (255, 192, 203)
        if command == 'whitei':
            pixels[0] = (255, 255, 255)
        if command == 'blacki':
            pixels[0] = (10, 10, 10)
        if command == 'clear':
            pixels[0] = (0, 0, 0)


def LEDsService (connection_mode, operation_mode, external_broker, username, password):

    global op_mode
    global external_client
    global internal_client
    global pixels
    global p

    print ('Connection mode: ', connection_mode)
    print ('operation mode: ', operation_mode)
    op_mode = operation_mode


    pixels = neopixel.NeoPixel(board.D18, 5)
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
    p.start(2) 
    # The internal broker is always (global or local mode) at localhost:1884
    internal_broker_address = "localhost"
    internal_broker_port = 1884



    if connection_mode == 'global':
        external_broker_address = external_broker
    else:
        external_broker_address = 'localhost'


    print ('External broker: ', external_broker_address)


    # the external broker must run always in port 8000
    external_broker_port = 8000


    external_client = mqtt.Client("LEDs_external", transport="websockets")
    if external_broker_address == 'classpip.upc.edu':
        external_client.username_pw_set(username, password)
    external_client.on_message = on_message
    external_client.connect(external_broker_address, external_broker_port)


    internal_client = mqtt.Client("LEDs_internal")
    internal_client.on_message = on_message
    internal_client.connect(internal_broker_address, internal_broker_port)

    print("Waiting....")
    external_client.subscribe("+/LEDsService/#")
    internal_client.subscribe("+/LEDsService/#")
    internal_client.loop_start()
    external_client.loop_start()
    if operation_mode == 'simulation':
        external_client.loop_forever()
    else:
        external_client.loop_start()



if __name__ == '__main__':
    import sys

    connection_mode = sys.argv[1] # global or local
    operation_mode = sys.argv[2] # simulation or production
    username = None
    password = None
    if connection_mode == 'global':
        external_broker = sys.argv[3]
        if external_broker == 'classpip.upc.edu':
            username = sys.argv[4]
            password = sys.argv[5]
    else:
        external_broker = None
    LEDsService(connection_mode, operation_mode, external_broker, username, password)

