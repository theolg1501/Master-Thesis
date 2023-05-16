import { createApp } from 'vue'
import App from './App.vue'

// https://cdmoro.github.io/bootstrap-vue-3/
import BootstrapVue3 from 'bootstrap-vue-3'
import  BootstrapVueIcons  from 'bootstrap-vue-3'  // Icons

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import 'bootstrap-icons/font/bootstrap-icons.css'  // Icons

// https://www.npmjs.com/package/vue-sweetalert2

// https://stackoverflow.com/questions/66537320/vue-3-event-bus-with-composition-api
import mitt from 'mitt';                  // Import mitt
const emitter = mitt();   

// https://www.emqx.com/en/blog/how-to-use-mqtt-in-vue
import mqtt, { MqttClient } from 'mqtt'


//https://leafletjs.com/examples/quick-start/

const app = createApp(App)
app.provide('emitter', emitter);          // ✅ Provide as `emitter`
let client : MqttClient;
try {
    // client = mqtt.connect('ws://broker.hivemq.com:8000/mqtt')
    // client = mqtt.connect('mqtt://localhost:8000')
    client = mqtt.connect('mqtt://10.10.10.1:8000')
    client.on('connect', ()=>{
        client.publish('webApplication/server/Connect', '')
        console.log('Connection succeeded !')
        app.provide('mqttClient', client)
    })
} 
catch (error){
    console.log('mqtt.connect error', error)
}

app.use(BootstrapVue3)
app.use(BootstrapVueIcons)  // Icons
app.mount('#app')

