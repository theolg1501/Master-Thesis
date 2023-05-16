<template>
    <div class="TopStyle">
        <div style = "display: flex;">
            <b-button @click ="AlertClicked" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="primary">Alert</b-button>
            <b-button @click ="showOldParametersPopUp = true" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="secondary">Old_Parameters</b-button>
            <OldParameters v-if="showOldParametersPopUp" @close="closeOldParameters">
            </OldParameters>
            <!-- <b-button @click ="showChooseParameters = true" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="secondary">Parameters</b-button> -->
            <ChooseParameters v-if="showChooseParameters" @close="closeChooseParameters">
            </ChooseParameters>
            <b-button @click ="connectDrone" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="success">Connect Drone</b-button>
            <!-- <b-form-input style="width: 5%; height: 20%; margin-top:1%" disable = "True" v-model="value" size="lg"></b-form-input> -->
            <b-button @click="showMap= !showMap" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="danger">Show Map</b-button>
            <Maps v-if="showMap" @close="closeMap"></Maps>
            <b-button @click="showFlightPlan= !showFlightPlan" style="margin: 1%; margin-left: 2.5%; margin-right: 2.5%; width: 15%" variant="danger">Make a Flight Plan</b-button>
            <FlightPlan v-if="showFlightPlan" @close="closeFlightPlan"></FlightPlan>
        </div>
        <b-input-group prepend="New user" style = "margin: 1%; width:50%; margin-left: 22%; margin-top: 1%">
            <b-form-input placeholder="name here" v-model="username"></b-form-input>
            <b-form-input placeholder="age here" v-model="age"></b-form-input>
            <b-input-group-append>
            <b-button @click ="InputUsername" variant="info">Enter</b-button>
            </b-input-group-append>
        </b-input-group>
    </div>
</template>

<script>
import { onMounted, defineComponent, ref, inject} from 'vue'
import Swal from 'sweetalert2'
import OldParameters from './OldParameters.vue'
import ChooseParameters from './ChooseParameters.vue'
import Maps from './Maps.vue'
import FlightPlan from './FlightPlan.vue'

export default defineComponent({
    components: {
        OldParameters,
        ChooseParameters,
        Maps,
        FlightPlan,
    },

    setup () {
        let username = ref(undefined);
        let age = ref(undefined);
        let showOldParametersPopUp = ref(false);
        let showChooseParameters = ref(false);
        let showMap = ref(false);
        let showFlightPlan = ref(false);
        let value = ref(undefined);
        const emitter = inject('emitter');
        let client = inject('mqttClient');
        // let distances_length_and_width;
        // let d_length = ref(undefined);
        // let d_width = ref(undefined);
        
        // emitter.on('distances_length_and_width', (distances)=>{
        //     console.log('Parameters in Top.vue', distances)
        //     distances_length_and_width = {'d_length': distances['d_length'], 'd_width': distances['d_width']}
        //     // d_length.value = distances['d_length']
        //     // d_width.value = distances['d_width']
        //     console.log('distances :', distances_length_and_width)
        //     console.log('type of ', typeof distances_length_and_width)
        //     // console.log('distances type :', typeof(distances_length_and_width['d_length']))
        //     // console.log('d_width in TOP', d_width)
        //     // emitter.emit('parameters', {'d_length': d_length, 'd_width': d_width});
        // });

        
        onMounted(() => {
            client.on('message', (topic, message) => {
                if (topic == 'Value') {
                    value.value = message
                }
            })
        })
        function AlertClicked(){
            Swal.fire('Alert Clicked')
            //console.log("Primary Clicked !!!")
        }

        function InputUsername(){
            console.log('name: ', username.value, 'age: ', age.value)
            emitter.emit('newUser', {'name':username.value, 'age':age.value});
            username.value = undefined;
            age.value = undefined;
        }
        function closeOldParameters() {
            showOldParametersPopUp.value= false
        }

        function closeChooseParameters() {
            showChooseParameters.value= false
        }

        function closeMap() {
            showMap.value= false
        }

        function closeFlightPlan() {
            showFlightPlan.value= false
        }

        function connectDrone(){
            // client.publish('getValue', "")
            // client.subscribe("Value")
            client.publish('webApplication/autopilotService/connect', '');
            client.subscribe('autopilotService/webApplication/telemetryInfo');
            client.publish('webApplication/camaraService/connect', '');

            //value.value = 33
            // return 33
        }

        return {
            AlertClicked,
            InputUsername,
            closeOldParameters,            
            closeChooseParameters,
            closeMap,
            closeFlightPlan,
            connectDrone,
            username,
            age,
            emitter,
            showOldParametersPopUp,
            showChooseParameters,
            showMap,
            showFlightPlan,
            value,
            // distances_length_and_width,
            // d_length,
            // d_width,
        }
    }
})
</script>

<style scoped>
    .TopStyle {
        border-style: solid;
        border-color: green;
        /* height: 20%; */
    }

</style>