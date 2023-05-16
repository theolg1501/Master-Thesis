<template>
  <button v-if = "!connected" class="ButtonConnect" @click = "toggle">Connect</button>
  <button v-if = "connected" class="ButtonDisconnect" @click = "toggle">Disconnect</button>
  <div v-if ="connected" class="main">
    <Top></Top>
    <div style="display:flex; height: 50%">
      <Left></Left>
      <Right></Right>
    </div>
    <Bottom></Bottom>
  </div>
</template>


<script>
import { onMounted, defineComponent, ref} from 'vue';
import Top from './components/Top.vue';
import Left from './components/Left.vue';
import Right from './components/Right.vue';
import Bottom from './components/Bottom.vue';
import Swal from 'sweetalert2';
import {io} from 'socket.io-client';

export default defineComponent({
  name: 'App',
  components: {
    Top,
    Left,
    Right,
    Bottom
  },
  setup (){
    let connected = ref (false);
    // const socket = io('http://localhost:5000')
    // onMounted(() => {
    //   socket.on('connected', (msg) => {
    //       Swal.fire({
    //             title: "Notification on connection",
    //             text: msg,
    //             type: "warning",
    //             showCancelButton: true,
    //             confirmButtonColor: "#3085d6",
    //             confirmButtonText: "Yes"
    //       }).then((result) => { // <--
    //             if (result.value) { // <-- if confirmed
    //               connected.value = true;
    //             }
    //       }); 
    //   });
    // })

    function toggle(){
      connected.value = !connected.value;
      // socket.emit('connectPlatform')
      // if (connected.value){
      //   client.publish("Connect", "");
      // }
    }
    return {
      toggle,
      connected,
      // socket,
    }
  },
});
</script>

<style>
  .main {
    height: 900px;
    border-style: double;
    border-color: black
  }
 .ButtonConnect {
  width: 90%;
  background-color: grey;
  color: red;
  margin: 5%;
  margin-top: 2%;
 } 
 .ButtonDisconnect {
  width: 90%;
  background-color: red;
  color: white;
  margin: 5%;
  margin-top: 1%;
  margin-bottom: 1%;
 } 

</style>
