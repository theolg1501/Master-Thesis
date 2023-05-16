<template>
    <div>
        <div class="popup">
            <div class="popup-inner">
                <div style ="display: flex; height:89%">
                    <div id='map' style="height: 100%; width: 65%"></div>
                    <div style="width: 35%;">
                        <div style="margin:0%">
                            <b-form-group v-slot="{ ariaDescribedby }">
                                <b-form-radio-group style="width:100%; margin-left:15%;" v-model="viewChooseParameters" 
                                    :options= "['Parameters', 'List of points']"
                                    :aria-describedby="ariaDescribedby"
                                    buttons></b-form-radio-group>
                            </b-form-group>
                        </div>
                        
                        <div v-if="viewChooseParameters === 'Parameters'">  
                            <!-- <h1 style="text-align: center ; margin-bottom: 5%">Parameters</h1> -->
            
                            <div id="CamerasParametersSelection" style="height: 30%;">
                                <h2  style="text-align: center;">Camera's parameters</h2>
                                <div style="margin-left: 2%;">
                                    <div style="display: flex; margin-bottom: 1%;">
                                        <h3 style="width:30%; text-align: center;">HFOV</h3>
                                        <b-form-input style="text-align:center; width:70%;" v-model="hfov" id="hfov" placeholder="Camera's HFOV in degres."></b-form-input>
                                    </div>
                                
                                    <div style="display: flex; margin-bottom: 1%;">
                                        <h3 style="width:30%; text-align: center;">VFOV</h3>
                                        <b-form-input style="text-align:center; width:70%;" v-model="vfov" id="vfov" placeholder="Camera's VFOV in degres."></b-form-input>
                                    </div>
                                </div>
                            </div>

                           <div id="ImagesParametersSelection" style="height: 30%;">
                                <h2  style="text-align: center;">Images' parameters</h2>
                                <div style="margin-left: 5%;">
                                    <div>
                                        <h3 for="h-overlap-slider">Horizontal Overlap : {{ h_overlap }} % </h3>
                                        <b-form-input id="h-overlap-slider" v-model = "h_overlap" type="range" min="0" max="100"></b-form-input>
                                    </div>

                                    <div>
                                        <h3 for="v-overlap-slider">Vertical Overlap :  {{ v_overlap }} % </h3>
                                        <b-form-input id="v-overlap-slider" v-model = "v_overlap" type="range" min="0" max="100"></b-form-input>
                                    </div>
                                </div>
                            </div>
 
                            <div id="FlightParametersSelection" style="height: 30%;">
                                <h2  style="text-align: center;">Flight'parameters</h2>
                                <div style="margin-left: 5%;">
                                    <div style="display: flex;">
                                        <h3 style="width:30%; text-align: center;">Height</h3>
                                        <b-form-input style="text-align:center; width:70%;" v-model="height" id="height" placeholder="Flight's height in meter."></b-form-input>
                                    </div>
                                </div>
                            </div>

                            <div style="height: 10%; display: grid; margin-top: 2%; margin-left: 2%;">
                                <b-button style="align-items: center;" @click="calculateParameters" variant="warning" size = "lg">Calculate Parameters</b-button>
                                <!-- <b-button style="width:20%; margin-left:10%" @click="close" variant="danger" size = "lg">Close</b-button> -->
                            </div>
                        </div>

                        <div v-else-if="viewChooseParameters === 'List of points'">
                            <div style = "height: ; width: 100%; margin: 1%; margin-left: 1.5%;">
                                <b-card bg-variant="light">
                                    <b-form-group label="List of points :" label-align-sm="center" v-slot="{ ariaDescribedby }">
                                        <b-form-radio-group class="pt-2" :options="['Selected Points', 'Waypoints', 'Stops Points']" :aria-describedby="ariaDescribedby" v-model="viewPointsSelected"></b-form-radio-group>
                                    </b-form-group>
                                </b-card>
                            </div>
            
                            <div v-if="viewPointsSelected === 'Waypoints'" id = "fpTable" style="height: 300px; overflow-y: scroll;">
                                <b-table :items="fp_formatted_to_show">
                                    <!-- <template v-slot:cell(Delete)="{ item }">
                                        <span><b-btn @click="deleteItem(item)"><i className="bi bi-trash3-fill" style='color:red'></i></b-btn></span>
                                    </template> -->
                                </b-table>
                            </div>

                            <div v-else-if="viewPointsSelected === 'Stops Points'" id = "stopsTable" style="height: 300px; overflow-y: scroll;">
                                <b-table sticky-header :items="stops_formatted_to_show"></b-table>
                            </div>

                            <div v-else id = "wpTable" style="height: 300px; overflow-y: scroll;">
                                <b-table :items="points"></b-table>
                            </div>
                        </div>
                    </div>
                    
                </div>
                <div style = "display: flex; height: 11%">
                    <!-- <b-button style="width:20% margin-left:5% margin-top:5%" @click="load" variant="primary">Load Flight Plan</b-button> -->
                    
                    <b-input-group prepend="Distance between images :" style = "width:30%; margin:1%; margin-left: 0%; margin-bottom:0%;">
                        <b-form-input placeholder="Length" v-model="d_length"></b-form-input>
                        <b-form-input placeholder="Width" v-model="d_width"></b-form-input>
                    </b-input-group>

                    <b-button style="width:19%; margin-left:1%; margin-top:1%;" @click="calculateFlightPlan" variant="info">Calculate Flight Plan</b-button>
                    <b-button style="width:19%; margin-left:1%; margin-top:1%" @click="clear" variant="warning">Clear</b-button>
                    <div style="width:19%; margin-left:1%; margin-top:1%;">
                        <b-button style="width:49.5%;" @click="sendWaypoints" variant="success">Send FP</b-button>
                        <b-button style="width:49.5%; margin-left:1%;" @click="sendPicturesPoints" variant="success">Send PicPoints</b-button>
                    </div>
                    <b-button style="width:19%; margin-left:1%; margin-top:1%" @click="close" variant="danger">Close Flight Plan</b-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { onMounted, ref, inject} from 'vue'
import leaflet from 'leaflet'
import Swal from 'sweetalert2'
// import Paho from 'paho-mqtt'
// import axios from 'axios'

// import io from 'socket.io-client'
// import * as mqtt from 'mqtt'
// import transport from 'mqtt'


export default {
    setup (props, context) {
        let client = inject('mqttClient');
        const emitter = inject('emitter');
        let map;
        let viewChooseParameters = ref('Parameters');
        let viewPointsSelected = ref('Selected Points');
        let points = ref([]);
        // let drone_position;
        // let drone_position_marker = leaflet.marker([0, 0], {draggable: 'false'});
        let count_points = 0;
        let hfov = ref(undefined);
        let vfov = ref(undefined);
        let h_overlap = ref(50);
        let v_overlap = ref(50);
        let height = ref(undefined);
        let d_length = ref(undefined);
        let d_width = ref(undefined);

        let fp;
        let stops;
        let fp_polyline;

        let fp_formatted;
        let stops_formatted;

        let fp_formatted_to_show = ref([]);
        let stops_formatted_to_show = ref([]);

        let geofence_polyline = leaflet.polyline([[41.27643580, 1.98821960], [41.27619490, 1.98833760], [41.27636320, 1.98911820], [41.27658190, 1.98901760], [41.27643580, 1.98821960]], {color: 'blue'}); 

        let drone_marker_icon = leaflet.icon({
            iconUrl: 'drone_marker_icon.png',
            iconSize: [41, 41],
            iconAnchor: [12, 30],
            iconBackground: 'transparent',
            // popupAnchor:[1, -34],
        });

        
        onMounted(() => {
            map = leaflet.map('map').setView([41.276486, 1.9886], 19);
            // leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            //      maxZoom: 21,
            //      attribution: '© OpenStreetMap'
            //  }).addTo(map);  
            let token =  "pk.eyJ1IjoibWlndWVsdmFsZXJvIiwiYSI6ImNsMjk3MGk0MDBnaGEzdG1tbGFjbWRmM2MifQ.JZZ6tJwPN28fo3ldg37liA";
        
            leaflet.tileLayer('https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.png?access_token='+token, {
                maxZoom: 23,
                attribution: 'Mapbox'

            })
            
            .addTo(map);

            geofence_polyline.addTo(map);

            let drone_position_marker = leaflet.marker([0, 0], {icon: drone_marker_icon}).addTo(map);

            map.on('click', onMapClick);
            // map.on('mousemove', onMapOver);
            // map.on('contextmenu', onRightClick);

            client.on('message', (topic, message) => {
                let splited = topic.split("/")
                let origin = splited[0]
                let destination = splited[1]
                let command = splited[2]
                if (command != 'telemetryInfo'){
                    console.log('New message : ', {'Topic': topic, 'Origin': origin, 'Destination': destination, 'Commande': command})
                }
                
                if (command == 'createdFlightPlan') {
                    console.log('Loading of fp ...');
                    let msg = JSON.parse(message);

                    if (typeof fp !== 'undefined') {
                        console.log("Deleting the previous flightPlan's Polyline.");
                        fp_polyline.remove(map);
                        // map.removeLayer(fp_polyline);
                    }

                    fp = msg['flight_points'];
                    stops = msg['stops_points'];
                    
                    fp_formatted = [];        
                    stops_formatted = [];

                    fp_formatted.push(fp.map(point => ({ lat: point[0], lng: point[1] })));
                    stops_formatted.push(stops.map(point => ({ lat: point[0], lng: point[1] })));

                    let lista_fp = [fp.map(point => ({ lat: point[0], lng: point[1] }))];
                    let lista_stops = [stops.map(point => ({ lat: point[0], lng: point[1] }))]

                    fp_formatted_to_show.value = lista_fp[0];
                    stops_formatted_to_show.value = lista_stops[0];

                    // fp_formatted.value = [{'lat': 70, 'lng':5}, {'lat': 70, 'lng':5}, {'lat': 70, 'lng':5}];
                    // fp_formatted = fp_formatted.concat(fp.map(point => ({ lat: point[0], lng: point[1] })));
                
                    // for (var i = 0; i < 5; i++){
                    //     let item = {lat: fp[i][0], lng : fp[i][1]};
                    //     fp_formatted_to_show.value.push(item);
                    // }

                    // console.log(points);
                    console.log('Flight Plan received :', fp);
                    console.log('fp formatted :', fp_formatted);
                    console.log('fp formatted to show:', fp_formatted_to_show);

                             
                    fp_polyline = leaflet.polyline(fp, {color: 'green'}).addTo(map);
                    viewPointsSelected.value = 'Waypoints';
                }

                
                if (command == 'calculatedParameters') {
                    console.log('Loading of distances between images ...')
                    let msg = JSON.parse(message);
                    // console.log('Transforming of message ...');
                    d_length.value = msg['d_length'];
                    d_width.value = msg['d_width'];
                    Swal.fire('Distances between images needed written !');
                    console.log('Distances processed', d_length, d_width)
                    // emitter.emit('distances_length_and_width', {'d_length': d_length, 'd_width': d_width});
                }

                if (command == 'telemetryInfo') {
                    let msg = JSON.parse(message);

                    drone_position_marker.setLatLng([msg['lat'], msg['lon']]);
                }
            })
        })
            

        function close(){
            context.emit('close')
        }

        function onMapClick(e) {
            count_points++;

            console.log('onMapClick :', e.latlng)

            // console.log('Distances :', d_length, d_width )

            // 
            // console.log('Type of distances : ', typeof this.distances_length_and_width); // Vérifiez si le type est bien un objet
            // console.log('Length : ', this.distances_length_and_width.d_length); // Vérifiez si la propriété est bien définie
            // console.log('Length crochets : ', this.distances_length_and_width['d_length']);

            let wp = leaflet.marker(e.latlng, {draggable: 'true'})
                .addTo(map)
                .bindTooltip((count_points - 1).toString(), {
                    permanent: true,
                    direction: "center",
                    className: "my-labels",
                });
            
            wp.index = points.value.length;  // to keep the index of the point associated to this marker.

            points.value.push(e.latlng);

            if (count_points == 1) {
                viewChooseParameters.value = 'List of points';
            }

            if (points.value.length > 1) {
                redrawPolyline();
            }

            wp.on('dragend', function(event) {
                var marker = event.target;
                var position = marker.getLatLng();
                console.log('moving to ', position);
                
                let index = marker.index;

                console.log('index of the point changed', index);

                if (index > -1) {
                    points.value[index] = position;
                }
                
                redrawPolyline();

            });
        }

        function redrawPolyline() {
            map.eachLayer(function (layer) {
                if (layer instanceof leaflet.Polyline) {
                    map.removeLayer(layer);
                }
            });

            geofence_polyline.addTo(map);

            leaflet.polyline(points.value, {color: 'red'}).addTo(map);
        }


        function clear(){
            count_points = 0;
            points.value = [];
            fp = undefined;
            stops = undefined;
            fp_formatted.value = [];
            stops_formatted.value = [];
            fp_formatted_to_show = ref([]);
            stops_formatted_to_show = ref([]);
            // showWpTable.value = true
            map.eachLayer((layer) => {
                if(layer['_latlng']!=undefined)
                    layer.remove();
                if(layer['_path']!=undefined)
                    layer.remove();
            })
        }


        function sendWaypoints(){
            Swal.fire({
                title: "Send Waypoints ?",
                text: "Do you want to send the waypoints calculated to the Autopilot ?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Send it !',
                confirmButtonColor: "#3085d6",
                cancelButtonText: `Don't send it.`,
            })
                .then((result) => {
                if (result.value) {
                    // let waypoints = {
                    //     coordinates: fp,
                    // };

                    let waypointsJSON = JSON.stringify(fp_formatted[0]);
                    
                    // console.log('Waypoints json :', waypointsJSON);
                    // console.log('Waypoints sent (fp):', fp);
                    // console.log('Waypoints sent in JSON format :', waypoints);
                    client.publish('webApplication/autopilotService/executeFlightPlan', waypointsJSON);  
                    Swal.fire('Sent !', '', 'success');
                }
                })
        }

        function sendPicturesPoints(){
            Swal.fire({
                title: "Send Pictures Points ?",
                text: "Do you want to send the Pictures Points calculated to the Camera ?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Send it !',
                confirmButtonColor: "#3085d6",
                cancelButtonText: `Don't send it.`,
            })
                .then((result) => {
                if (result.value) {
                    let PicturesPoints = {
                        coordinates: stops,
                    };

                    let PicturesPointsJSON = JSON.stringify(PicturesPoints);

                    // console.log('Pictures points sent :', PicturesPoints);
                    // console.log('Pictures points sent in JSON format :', PicturesPointsJSON);
                    client.publish('webApplication/cameraService/executePicturesPlan', PicturesPointsJSON);
                    Swal.fire('Sent !', '', 'success')
                }
                })
        }


        function calculateFlightPlan(){
            Swal.fire({
                title: "Send parameters ?",
                text: "Are you sure that you want to send the parameters to calculate the flight plan ? ",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                confirmButtonText: "Yes!"
            })
                .then((result) => { 
                if (result.value) {
                    // client = mqtt.client(transport="websockets")
                    // client.connect()
                    // Creation of the JSON object with the list and the parameters needed
                    let data = {
                            points: points.value,
                            d_length: d_length.value,
                            d_width: d_width.value,
                    };

                    // console.log('Points and distances from FP', data);

                    let dataJSON = JSON.stringify(data);

                    // console.log('Datas JSON : ', dataToSend);

                    // To send the datas 
                    console.log('Points and distances sent from FP.', data);
                    client.publish('webApplication/server/createFlightPlan', dataJSON);
                    client.subscribe('server/webApplication/createdFlightPlan');

                    // .catch(error => {
                    //     console.error(error);
                    // })
                }
            });
        }

        function calculateParameters(){
            const parameters = {
                hfov: Number(hfov.value),
                vfov: Number(vfov.value),
                h_overlap: h_overlap.value / 100,
                v_overlap: v_overlap.value / 100,
                height : Number(height.value),
            }

            console.log('Parameters chosen :', parameters)
            
            Swal.fire({
                title: 'Write parameters ?',
                text : "Are you sure? You won't be able to revert this!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                confirmButtonText: "Yes, write parameters!"
            }).then((result) => {
                if (result.value){
                    let parametersJSON = JSON.stringify(parameters);
                    client.publish('webApplication/server/calculateParameters', parametersJSON);
                    client.subscribe('server/webApplication/calculatedParameters');
                }
            })
            
        }


        return {
            close,
            onMapClick,
            clear, 
            calculateFlightPlan,
            calculateParameters,
            sendWaypoints,
            sendPicturesPoints,
            viewChooseParameters,
            viewPointsSelected,
            points,
            h_overlap,
            v_overlap,
            hfov,
            vfov,
            height,
            d_length,
            d_width,
            fp,
            stops,
            fp_formatted,
            fp_formatted_to_show,
            stops_formatted,
            stops_formatted_to_show,
            emitter,
        }

    
    }
}
</script>

<style>
/* h1 {
  display: block;
  font-size: 2em;
  font-weight: bold;
}

h2 {
  display: block;
  font-size: 0.7em;
  font-weight: bold;
} */

/* .h3 {
  display: block;
  font-size: 0.1em;
  font-weight: bold;
} */

.popup {
	position: fixed;
	top: 0;
	left: 0;
	right: 0;
	bottom: 0;
  
	z-index: 99;
	background-color: rgba(0, 0, 0, 0.2);
	
	display: flex; 
	align-items: center;
	justify-content: center;
	
}

.popup-inner {
		background: #FFF;
		padding: 1%;
        width: 98.5%;
        height: 98.5%;
}

#map{
    width:70%;
    height: 500px;
    border-style: solid;
}

.my-labels{
    background-color: rgb(194, 218, 147)
}

.fpTable{
    height: 50px;
}
</style>