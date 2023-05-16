<template>
    <div class="RightStyle">
        <b-table class="myTable" sticky-header striped hover :items="userList" :fields="['name', 'age', 'Delete']">
            <template v-slot:cell(Delete)="{ item }">
                <span><b-btn @click="deleteItem(item)"><i className="bi bi-trash3-fill" style='color:red'></i></b-btn></span>
            </template>
        </b-table>
    </div>
</template>

<script>
import { defineComponent, ref, inject} from 'vue'

export default defineComponent( {
    setup () {
        let userList = ref([]);
        const emitter = inject('emitter')
        emitter.on ('newUser', (user)=>{
            // console.log('New user in Right component ', user)
            userList.value.push(user)
            console.log ('List ', userList.value)
        }); 
        function deleteItem (item) {
            this.userList = this.userList.filter(user => user.name != item.name);
        }


        return {
            userList,
            deleteItem
        }
    }
})
</script>

<style scoped>
    .RightStyle {
        border-style: solid;
        border-color: red;
        width: 50%;
    }
    .myTable {
        width:80%;
        height:50px;
        margin-left: 15%;
        margin-top: 1%;
        border-style: solid;
    }
    
</style>