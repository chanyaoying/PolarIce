<template>
    <div>
        {{ userData }}
        <input type="text /" />
        <button @click="createRoom()">Create Room</button>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: "allRoom",
    data: () => ({
        userData: '',
    }),
    created() {
        console.log('dumb bij :>> ');
        axios.get('https://127.0.0.1:5000/').then((res) => {
            console.log('res :>> ', res)
            this.userData = res.data
        }).catch((err) => {
            console.log('err :>> ', err); 
        });
        console.log('this.userData :>> ', this.userData);
    }
}
</script>