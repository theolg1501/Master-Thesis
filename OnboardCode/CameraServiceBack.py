

import cv2 as cv

import paho.mqtt.client as mqtt
import base64
import threading
import time

import json

from ColorDetector import ColorDetector


def send_video_stream(origin, client):
    global sending_video_stream
    global cap
    topic_to_publish = f"cameraService/{origin}/videoFrame"

    while sending_video_stream:
        # Read Frame
        ret, frame = cap.read()
        if ret:
            _, image_buffer = cv.imencode(".jpg", frame)
            jpg_as_text = base64.b64encode(image_buffer)
            client.publish(topic_to_publish, jpg_as_text)
            time.sleep(0.2)


def send_video_for_calibration(origin, client):
    global sending_video_for_calibration
    global cap
    global colorDetector
    topic_to_publish = f"cameraService/{origin}/videoFrame"

    while sending_video_for_calibration:
        # Read Frame
        ret, frame = cap.read()
        if ret:
            frame = colorDetector.MarkFrameForCalibration(frame)
            _, image_buffer = cv.imencode(".jpg", frame)
            jpg_as_text = base64.b64encode(image_buffer)
            client.publish(topic_to_publish, jpg_as_text)
            time.sleep(0.2)


def send_video_with_colors(origin, client):
    global finding_colors
    global cap
    global colorDetector
    topic_to_publish = f"cameraService/{origin}/videoFrameWithColor"

    while finding_colors:
        # Read Frame
        ret, frame = cap.read()
        if ret:
            frame, color = colorDetector.DetectColor(frame)
            _, image_buffer = cv.imencode(".jpg", frame)
            frame_as_text = base64.b64encode(image_buffer)
            base64_string = frame_as_text.decode("utf-8")
            frame_with_colorJson = {"frame": base64_string, "color": color}
            frame_with_color = json.dumps(frame_with_colorJson)
            client.publish(topic_to_publish, frame_with_color)
            time.sleep(0.2)


def process_message(message, client):

    global sending_video_stream
    global sending_video_for_calibration
    global finding_colors
    global cap
    global colorDetector

    splited = message.topic.split("/")
    origin = splited[0]
    command = splited[2]
    print("recibo ", command, "de ", origin)

    if command == "takePicture":
        print("Take picture")
        ret = False
        for n in range(1, 20):
            # this loop is required to discard first frames
            ret, frame = cap.read()
        _, image_buffer = cv.imencode(".jpg", frame)
        # Converting into encoded bytes
        jpg_as_text = base64.b64encode(image_buffer)
        client.publish("cameraService/" + origin + "/picture", jpg_as_text)

    if command == "startVideoStream":
        print("start video stream")
        sending_video_stream = True
        w = threading.Thread(
            target=send_video_stream,
            args=(origin, client),
        )
        w.start()

    if command == "stopVideoStream":
        print("stop video stream")
        sending_video_stream = False

    if command == "markFrameForCalibration":
        print("markFrameForCalibration")
        sending_video_for_calibration = True
        w = threading.Thread(
            target=send_video_for_calibration,
            args=(origin, client),
        )
        w.start()
    if command == "stopCalibration":
        print("stop calibration")
        sending_video_for_calibration = False
    if command == "getDefaultColorValues":
        yellow, green, blueS, blueL, pink, purple = colorDetector.DameValores()
        colorsJson = {
            "yellow": yellow,
            "green": green,
            "blueS": blueS,
            "blueL": blueL,
            "pink": pink,
            "purple": purple,
        }
        colors = json.dumps(colorsJson)
        print("envio: ", colorsJson)
        client.publish("cameraService/" + origin + "/colorValues", colors)
    if command == "getColorValues":
        colorDetector.TomaValores()
        print("ya he tomado los valroe")
        yellow, green, blueS, blueL, pink, purple = colorDetector.DameValores()
        colorsJson = {
            "yellow": yellow,
            "green": green,
            "blueS": blueS,
            "blueL": blueL,
            "pink": pink,
            "purple": purple,
        }
        print("voy a enviar: ", colorsJson)
        colors = json.dumps(colorsJson)
        print("envio: ", colorsJson)
        client.publish("cameraService/" + origin + "/colorValues", colors)

    if command == "takeValues":
        colorDetector.TomaValores()

    if command == "startFindingColor":
        finding_colors = True
        w = threading.Thread(
            target=send_video_with_colors,
            args=(origin, client),
        )
        w.start()
    if command == "stopFindingColor":
        finding_colors = False




def on_internal_message(client, userdata, message):
    print("recibo internal ", message.topic)
    global internal_client
    process_message(message, internal_client)


def on_external_message(client, userdata, message):
    print("recibo external ", message.topic)

    global external_client
    process_message(message, external_client)


def CameraService(connection_mode, operation_mode, external_broker, username, password):
    global op_mode
    global external_client
    global internal_client
    global state
    global cap
    global colorDetector

    sending_video_stream = False

    cap = cv.VideoCapture(0)  # video capture source camera (Here webcam of lap>

    colorDetector = ColorDetector()

    print("Camera ready")

    print("Connection mode: ", connection_mode)
    print("Operation mode: ", operation_mode)
    op_mode = operation_mode

    # The internal broker is always (global or local mode) at localhost:1884
    internal_broker_address = "localhost"
    internal_broker_port = 1884

    if connection_mode == "global":
        external_broker_address = external_broker
    else:
        external_broker_address = "localhost"

    print("External broker: ", external_broker_address)

    # the external broker must run always in port 8000
    external_broker_port = 8000

    external_client = mqtt.Client("Camera_external", transport="websockets")
    if external_broker_address == "classpip.upc.edu":
        external_client.username_pw_set(username, password)

    external_client.on_message = on_external_message
    external_client.connect(external_broker_address, external_broker_port)

    internal_client = mqtt.Client("Camera_internal")
    internal_client.on_message = on_internal_message
    internal_client.connect(internal_broker_address, internal_broker_port)

    print("Waiting....")
    external_client.subscribe("+/cameraService/#", 2)
    internal_client.subscribe("+/cameraService/#")
    internal_client.loop_start()
    external_client.loop_forever()


if __name__ == "__main__":
    import sys

    connection_mode = sys.argv[1]  # global or local
    operation_mode = sys.argv[2]  # simulation or production
    username = None
    password = None
    if connection_mode == "global":
        external_broker = sys.argv[3]
        if external_broker == "classpip.upc.edu":
            username = sys.argv[4]
            password = sys.argv[5]
    else:
        external_broker = None

    CameraService(connection_mode, operation_mode, external_broker, username, password)
