<template>
    <div>
        {{ userData }}
        <button @click="created()"> prof details </button>
        <button @click="createRoom()">Create Room</button>
        <h1>{this.userData}</h1>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    name: "allRoom",
    data: () => ({
        userData: '',
    }),
    methods: {
        created() {
            axios
                .get('https://127.0.0.1:5000/').then((res) => {
                    console.log('result :>> ', res)
                    this.userData = res.data
                }).catch((err) => {
                    console.log('err :>> ', err); 
            });
            console.log('this.userData :>> ', this.userData);
        }
    }
}
</script>