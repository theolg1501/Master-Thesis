import json

import paho.mqtt.client as mqtt
import requests
from matplotlib import pyplot as plt

import FlightPlan as FP
import calculateParameters as CP

global_broker_address = 'localhost'  # "broker.hivemq.com"
global_broker_port = 8000


# API_URL = "http://localhost:8080/"


def on_message_function(cli, userdata, message):
    global client

    # splited = message.topic.split("/")
    # origin = splited[0]
    # destination = splited[1]
    # command = splited[2]

    if message.topic == 'Connect':
        print('Connection and subscription.')
        client.subscribe('createFlightPlan')
        client.subscribe('getValue')
        client.subscribe('calculateParameters')
        client.subscribe('StartVideoStream')
        print('Connected.')

    if message.topic == "createFlightPlan":
        print('Flight plan creation.')
        msg = json.loads(message.payload.decode("utf-8"))  # print('msg =\n', msg)

        list_pts = []
        points = msg['points']  # print('points =\n', points)

        for point in points:
            new_point = point['lat'], point['lng']
            list_pts.append(new_point)  # print('list_created :\n', list_pts)

        flight_points, stops = FP.create_flight_plan(list_pts, float(msg['d_length']), float(msg['d_width']))
        result = {'flight_points': flight_points, 'stops_points': stops}

        client.publish('createdFlightPlan', json.dumps(result))
        print('Flight plan created and sent !')

        """Plots, not necessary."""
        # # print('axis')
        # plt.axis()
        # # print('first_plot')
        # FP.plot_pts(list_pts, style='-', color='y', wait=True)
        # sorted_pts = FP.sorted_points(list_pts)
        # # print('second_plot')
        # FP.plot_pts(sorted_pts, style=':', color='b', wait=True)
        # # print('last_plot')
        # FP.plot_pts(flight_points, style='-', color='r', wait=True)
        # FP.plot_pts(stops, style='--', color='g', wait=False)

    if message.topic == "calculateParameters":
        print('Calculate distances between photos.')
        msg = json.loads(message.payload.decode("utf-8"))

        hfov = msg['hfov']
        vfov = msg['vfov']
        h_overlap = msg['h_overlap']
        v_overlap = msg['v_overlap']
        height = msg['height']
        # print('hfov : ', hfov, '\nvfov : ', vfov, '\nh_overlap : ', h_overlap, '\nv_overlap : ', v_overlap, '\nheight : ', height)
        # print(type(h_overlap), type(hfov))
        d_length, d_width = CP.calculate_distance_between_photos(height, h_overlap, v_overlap, hfov, vfov)

        result = {'d_length': d_length, 'd_width': d_width}

        client.publish('calculatedParameters', json.dumps(result))
        print('Distances between photos calculated.')


if __name__ == '__main__':
    client = mqtt.Client(transport="websockets")
    # client = mqtt.Client("ComputeService")
    client.on_message = on_message_function

    client.connect(global_broker_address, global_broker_port)
    client.subscribe('Connect')
    print("Waiting commands")

    # By the moment, the data service only can store positions (sent by the autopilot service)
    # and provide the stored positions
    # client.subscribe("autopilotService/dataService/storePosition")
    # client.subscribe("+/dataService/getStoredPositions")
    # client.subscribe("+/ComputeService/createFlightPlan")
    client.loop_forever()
