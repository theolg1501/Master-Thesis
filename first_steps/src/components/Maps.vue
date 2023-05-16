<template>
    <div>
        <div class="popup">
            <div class="popup-inner">
                <div style ="display: flex">
                    <div id='map'></div>
                    <div id = "wpTable">
                        <b-table :items="waypoints"></b-table>
                    </div>
                </div>
                <div style = "display: flex; margin-left: 20%">
                    <b-button style="width:20% margin-left:5% margin-top:5%" @click="load" variant="primary">Load Flight Plan</b-button>
                    <b-button style="width:20% margin-left:5% margin-top:5%" @click="save" variant="info">Save Flight Plan</b-button>
                    <b-button style="width:20% margin-left:5% margin-top:5%" @click="clear" variant="warning">Clear</b-button>
                    <b-button style="width:20% margin-left:5% margin-top:5%" @click="close" variant="danger">Close Map</b-button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { onMounted, ref} from 'vue'
import leaflet from 'leaflet'
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
    setup (props, context) {
        let map;
        let count = 0;
        let popup = leaflet.popup();
        let waypoints = ref([]);
        let tmpLine = undefined;
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
            }).addTo(map);
            map.on('click', onMapClick);
            map.on('mousemove', onMapOver);
            map.on('contextmenu', onRightClick);
        })

        function close(){
            context.emit('close')
        }

        function onMapClick(e){
            count = count + 1;
            console.log(e.latlng)
            if (count > 1) {
                let last = waypoints.value[waypoints.value.length-1];
                let distance = last.distanceTo(e.latlng).toFixed(0)/1000;
                let midpoint =new leaflet.LatLng((last.lat + e.latlng.lat)/2, (last.lng + e.latlng.lng)/2);
                leaflet.marker(midpoint, {opacity: 0.01}).addTo(map).bindTooltip(distance.toString(), {
                    permanent: true,
                    direction: 'center',
                    className: "my-labels"});
            }

            waypoints.value.push(e.latlng);
            // console.log('waypoints', waypoints);
            // console.log('waypoints val', waypoints.value);
            // console.log('waypoints lght', waypoints.value.length);
            if (waypoints.value.length > 1){
                leaflet.polyline(waypoints.value, {color: 'red'}).addTo(map);
            }

            let wp = leaflet.marker(e.latlng, {draggable:'true'}).addTo(map).bindTooltip(count.toString(),  {
                            permanent: true,
                            direction: 'center',
                            className: "my-labels"});
            
            wp.on('dragend', function(event){
                var marker = event.target;
                var position = marker.getLatLng();
                console.log('moving to ', position);

                marker.setLatLng(new leaflet.LatLng(position.lat, position.lng), {draggable: true})
                map.panTo(new leaflet.LatLng(position.lat, position.lng))
            })    
    
            // let wp = leaflet.marker(e.latlng, {draggable:'true'}).addTo(map).bindTooltip(count.toString(),  {
            //                 permanent: true,
            //                 direction: 'center',
            //                 className: "my-labels"
            //              });
        }
            

        function onMapOver(e){
            if (count> 0){
                let last = waypoints.value[waypoints.value.length-1];
                let distance = last.distanceTo(e.latlng).toFixed(0)/1000;
                let midpoint = new leaflet.LatLng((last.lat + e.latlng.lat)/2, (last.lng + e.latlng.lng)/2);
                popup
                .setLatLng(midpoint)
                .setContent( distance.toString())
                .openOn(map);
                if (tmpLine != undefined) {
                    tmpLine.remove(map)
                }
                tmpLine = leaflet.polyline([last,e.latlng], {color: 'red'}).addTo(map);
            }
        }

        function onRightClick(e){
            if (tmpLine != undefined) {
                    tmpLine.remove(map)
            }
            // leaflet.polyline(waypoints.value)
            leaflet.polyline(waypoints.value, {color: 'green'}).addTo(map);
        }

        function clear(){
            count = 0;
            waypoints.value = [];
            map.eachLayer((layer) =>{
                if(layer['_latlng']!=undefined)
                    layer.remove();
                if(layer['_path']!=undefined)
                    layer.remove();
            })
        }

        function save(){
            Swal.fire({
                title: "Save flight plan?",
                text: "Are you sure? ",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                confirmButtonText: "Yes!"
            }).then((result) => { 
                if (result.value) {
                    let data = JSON.stringify(waypoints.value)
                    axios.post("http://localhost:5000/data", data, {headers: {"Content-type": "application/json",}})
                    .then(response => {
                        Swal.fire('Done!');
                        context.emit('close');
                        console.log ('ok')});
                }
            });
        }

        function load(){
            axios.get('http://localhost:4000/data')
                .then(data => {
                    
                    let n = data.data.length;
                    if (n>0) {
                        waypoints.value = data.data[n-1];
                        data.data[n-1].forEach(wp => {
                            leaflet.marker(wp).addTo(map)
                        });
                    }
                })
            console.log('Load function')
        }


        return {
            close,
            onMapClick,
            onMapOver,
            onRightClick,
            clear,
            save,
            load,
            map,
            count,
            popup,
            waypoints,
            tmpLine
        }
    }
}
</script>

<style>
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
		padding: 32px;
        width: 95%;
        height: 95%;
}

#map{
    width:70%;
    height: 500px;
    border-style: solid;
}

.my-labels{
    background-color: rgb(194, 218, 147)
}
</style>