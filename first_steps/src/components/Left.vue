<template>
    <div class="LeftStyle">
        <div>
            <b-button style ="width:20%; margin:1%; margin-left:20%"  @click="startVideoFrame" variant="success">
                Start video frame 
            </b-button>
            <b-button style ="width:20%; margin:1%" @click="stopVideoFrame" variant="warning">
                Stop video frame 
            </b-button>
        </div>

        <div style="display:flex">
            <div  style ="width:70%">
                <canvas style="margin-left:5%; width: 400px; height: 300px; border-style: solid;" id= "output"></canvas>
            </div>
            
            <div class ="buttonColumn">
            <b-button style =" margin:1%" @click="mode = 'gray'" variant="info">
                Gray </b-button>
            <b-button style ="margin:1%" @click="mode = 'canny'" variant="success">
                Canny </b-button>
            <b-button style ="margin:1%" @click="mode = 'normal'" variant="warning">
                Normal </b-button>
            </div>
       </div>
    </div>
</template>

<script>
import { onMounted, defineComponent, inject, ref } from 'vue'
import * as cv from 'opencv.js'

export default defineComponent({
    setup () {
        let client = inject('mqttClient');
        let mode = ref ('normal')
        onMounted(() => {
            client.on('message', (topic, message) => {
                if (topic == 'videoFrame') {
                    const img = new Image();
                    img.src = "data:image/jpg;base64,"+message;
                    const canvas = document.getElementById('output');
                    const context = canvas.getContext('2d');
                    img.onload = () => { 
                        let dst;
                        // context.drawImage(img, 0, 0, img.width, img.height, 0, 0, canvas.width, canvas.height)

                        // let mat = cv.imread(img);
                        // let dst = new cv.Mat();
                        // cv.cvtColor(mat, dst, cv.COLOR_RGB2GRAY, 0);
                        // cv.imshow('output', dst)

                        if (mode.value == 'normal'){
                            dst = cv.imread (img);}
                        
                        if (mode.value == 'gray') {
                            let mat = cv.imread (img);
                            dst = new cv.Mat();
                            cv.cvtColor (mat, dst, cv.COLOR_RGB2GRAY,0);
                            mat.delete()}
                        
                        if (mode.value == 'canny') {
                            let mat = cv.imread (img);
                            dst = new cv.Mat();
                            cv.cvtColor (mat, dst, cv.COLOR_RGB2GRAY,0);
                            cv.Canny(mat, dst, 50, 100, 3, false);
                            mat.delete()}
                        
                        cv.imshow ('output', dst);
                    };
                }
            })
        })
        

        function startVideoFrame () {
            client.publish ("StartVideoStream")
            client.subscribe("videoFrame");
        }
         function stopVideoFrame () {
            client.publish ("StopVideoStream")
        }

        return {
            startVideoFrame,
            stopVideoFrame,
            client,
            mode
        }
    }
})
</script>
    
<style scoped>
    .LeftStyle {
        border-style: solid;
        border-color: blueviolet;
        width: 50%;
    }

    .buttonColumn {
    display: flex;
    justify-content: center;
    flex-direction: column;
    padding-top: 20px;
    width: 20%;
    border: 2px solid red;
    padding: 10px;
    border-radius: 25px;
    margin-left: 5%
    }

</style>