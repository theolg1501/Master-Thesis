<template>
    <div class="popup">
        <div class="popup-inner">
            <h1 style="text-align: center ; margin-bottom: 5%">Parameters</h1>
            
            <div style="display: flex; height: 25%;">
                <h2  style="text-align: center; width: 30%; margin-left: 5%;">Camera's parameters</h2>
                <div style="width:60%; margin-left: 5%;">
                    <div style="display: flex; margin-bottom: 1%;">
                        <h3 style="width:20%; margin-right: 5%;">HFOV</h3>
                        <b-form-input style="text-align:center; width:70%; margin-right: 5%;" v-model="hfov" id="hfov" placeholder="Enter the HFOV of the camera in degres."></b-form-input>
                    </div>
                
                
                    <div style="display: flex;">
                        <h3 style="width:20%; margin-right: 5%;">VFOV</h3>
                        <b-form-input style="text-align:center; width:70%; margin-right: 5%;" v-model="vfov" id="vfov" placeholder="Enter the VFOV of the flight in degres."></b-form-input>
                    </div>
                </div>

            </div>

            <div style="display: flex; height: 25%;">
                <h2  style="text-align: center; width: 30%; margin-left: 5%;">Images' parameters</h2>
                <div style="width:60%; margin-left: 5%;">
                    <div style="display: flex;">
                        <h3 for="h-overlap-slider" style="width:20%; margin-right: 5%;">Horizontal Overlap</h3>
                        <b-form-input style="width:60%;" id="h-overlap-slider" v-model = "h_overlap" type="range" min="0" max="100"></b-form-input>
                        <h3 style="width:10%; margin-left:5%;"> {{ h_overlap }} % </h3>
                    </div>

                    <div style="display: flex;">
                        <h3 for="v-overlap-slider" style="width:20%; margin-right: 5%;">Vertical Overlap</h3>
                        <b-form-input style="width:60%;" id="v-overlap-slider" v-model = "v_overlap" type="range" min="0" max="100"></b-form-input>
                        <h3 style="width:10%; margin-left:5%;"> {{ v_overlap }} % </h3>
                    </div>
                </div>
            </div>

            <div style="display: flex; height: 25%;">
                <h2  style="text-align: center; width: 30%; margin-left: 5%;">Flight'parameters</h2>
                <div style="width:60%; margin-left: 5%;">
                    <div style="display: flex;">
                        <h3 style="width:20%; margin-right: 5%;">Height</h3>
                        <b-form-input style="text-align:center; width:70%; margin-right: 5%;" v-model="height" id="height" placeholder="Enter the height of the flight in meter."></b-form-input>
                    </div>
                </div>
            </div>

            <div style="height: 25%;">
                <b-button style="width:50%; margin-left:10%" @click="writeParameters" variant="warning" size = "lg">Send Parameters</b-button>
                <b-button style="width:20%; margin-left:10%" @click="close" variant="danger" size = "lg">Close</b-button>
            </div>

                        
        </div>
    </div>
</template>

<script>
import {ref, inject} from 'vue'
import Swal from 'sweetalert2'
export default {
    // props: {
    //     distances_length_and_width: 
    // },

    setup (props, context) {
        let hfov = ref(undefined);
        let vfov = ref(undefined);
        let h_overlap = ref (undefined);
        let v_overlap = ref (undefined);
        let height = ref(undefined);
        let client = inject('mqttClient');
        const emitter = inject('emitter');

        client.on('message', (topic, message) => {
            if (topic == 'createdParameters') {
                console.log('Loading of d_length / d_width ...')
                let msg = JSON.parse(message);
                console.log('Transforming of message ...');
                let d_length = msg['d_length'];
                let d_width = msg['d_width'];
                console.log('d_length : ', d_length);
                console.log('d_width : ', d_width);
                // emitter.emit('distances_length_and_width', {'d_length': d_length, 'd_width': d_width});
            }
        })

        function close(){
            context.emit('close')
        }
        
        function writeParameters(){
            // console.log('typeof', typeof(Number(hfov.value)))
            // console.log('hfov.value', hfov.value)
            // console.log('hfov :', Number(hfov.value))
            // console.log('vfov :', Number(vfov.value))
            // console.log ('h overlap: ', h_overlap.value / 100)
            // console.log ('v overlap: ', v_overlap.value / 100)
            // console.log('height :', Number(height.value))

            const parameters = {
                hfov: Number(hfov.value),
                vfov: Number(vfov.value),
                h_overlap: h_overlap.value / 100,
                v_overlap: v_overlap.value / 100,
                height : Number(height.value),
            }

            console.log('Parameters : ', parameters)
            
            Swal.fire({
                title: 'Write parameters ?',
                text : "Are you sure? You won't be able to revert this!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                confirmButtonText: "Yes, write parameters!"
            }).then((result) => {
                if (result.value){
                    let message = JSON.stringify(parameters);
                    client.publish('writeParameters', message);
                    client.subscribe('createdParameters');
                    Swal.fire('Done!');
                    context.emit('close');
                }
            })
            
        }

        return {
            close,
            writeParameters,
            emitter,
            h_overlap,
            v_overlap,
            hfov,
            vfov,
            height,
            client,
        }
    }
}
</script>

<style scoped>

h1 {
  display: block;
  font-size: 2em;
  font-weight: bold;
}

h2 {
  display: block;
  font-size: 1.3em;
  font-weight: bold;
}

h3 {
  display: block;
  font-size: 1.0em;
  font-weight: bold;
}
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
		padding: 2%;
        width: 70%;
        height: 90%;
}
</style>