<template>
    <div class="popup">
        <div class="popup-inner">
            <h1 style="text-align: center ; margin-bottom: 5%">Parameters</h1>
            
            <div>
                <b-form-group label="Name:" label-for="nested-street" label-cols-sm="3" label-align-sm="right">
                    <b-form-input id="nested-street" v-model="name"></b-form-input>
                </b-form-group>
            </div> 
            
            <b-input-group style = "width:80%; margin-left: 10%" >
                <h4 >Speed: {{speed}}</h4>
                <b-form-input  v-model = "speed" type="range" min="0" max="100"></b-form-input>
            </b-input-group>
            
            <div style = "display:flex">
                <div style = "width: 45%; margin: 1%">
                    <b-card bg-variant="light">
                        <b-form-group label="RadioButton Options:" label-align-sm="right" v-slot="{ ariaDescribedby }">
                            <b-form-radio-group class="pt-2" :options="['Air', 'Courier', 'Mail']" :aria-describedby="ariaDescribedby" v-model="radioButtonSelected"></b-form-radio-group>
                        </b-form-group>
                    </b-card>
                </div>

                <div style = "width: 45%; margin: 1%">
                    <b-card bg-variant="light">
                        <b-form-group label="CheckBox Options:" label-align-sm="right" v-slot="{ ariaDescribedby }">
                            <b-form-checkbox-group id="checkbox-group-1" class="pt-2" name="flavour-2" :options="checkBoxOptions" :aria-describedby="ariaDescribedby" v-model="selected"></b-form-checkbox-group>
                        </b-form-group>
                    </b-card>
                </div>
            </div>

            <b-button style="width:40%;margin-left:10%" @click="writeParameters" variant="warning" size = "lg">Send Parameters</b-button>
            <b-button style="width:20%;margin-left:10%" @click="close" variant="danger" size = "lg">Close</b-button>
            
        </div>
    </div>
</template>

<script>
import {ref, inject} from 'vue'
import Swal from 'sweetalert2'
export default {
    setup (props, context) {
        let name = ref (undefined);
        let speed = ref (undefined);
        let radioButtonSelected = ref (undefined);
        let checkBoxOptions= ref ( [
            { text: 'Orange', value: 'orange' },
            { text: 'Apple', value: 'apple' },
            { text: 'Pineapple', value: 'pineapple' },
            { text: 'Grape', value: 'grape'},
            { text: 'Otro', value: 'otro'}]);

        let selected = ref (undefined);
        let client = inject('mqttClient');

        function close(){
            context.emit('close')
        }
        
        function writeParameters(){
            console.log('name :', name.value)
            console.log('speed :', speed.value)
            console.log ('radioButtonSelected: ', radioButtonSelected.value)
            console.log ('selected: ', selected.value)

            const parameters = {
                selected: selected.value,
                radioButtonSelected: radioButtonSelected.value,
                name: name.value,
                speed: speed.value
            }
            
            Swal.fire({
                title: 'Write parameters ?',
                text : "Are you sure? You won't be able to revert this!",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                confirmButtonText: "Yes, write parameters!"
            }).then((result) => {
                if (result.value){
                    let message = JSON.stringify(parameters)
                    client.publish('writeParameters', message)
                    Swal.fire('Done!');
                    context.emit('close')  
                }
            })
            
        }

        return {
            close,
            writeParameters,
            radioButtonSelected,
            name,
            speed,
            checkBoxOptions,
            selected,
            client,
        }
    }
}
</script>

<style scoped>
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
        width: 600px;
        height: 500px;
}
</style>