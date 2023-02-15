# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from FlightPlan import *

app = Flask(__name__)


@app.route('/dashboard/')
def dashboard():
    return "Hello World!"


@app.route('/api/meteo/')
def meteo():
    dictionnaire = {
        'type': 'Prévision de température',
        'valeurs': [24, 24, 25, 26, 27, 28],
        'unite': "degrés Celcius"
    }
    return jsonify(dictionnaire)


@app.route('/api/FlightPlan/')
def FlightPlan():
    pts = [(41.275827, 1.987712), (41.276788, 1.987478), (41.275843, 1.988352),
           (41.276965, 1.989399), (41.276264, 1.989522), (41.277231, 1.988347)]

    # sorted_pts = sorted_points(pts)
    # plot_pts(sorted_pts, style=':', wait=True)

    # plt.axis('equal')

    # fp_points, stops_points =
    return create_flight_plan(pts, 5, 10)


if __name__ == "__main__":
    app.run(debug=True)
