<template>
    <div class="home">
        <!-- <img alt="Vue logo" src="../assets/logo.png" /> -->
        <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
        <button @click="testing">Test</button>
        <button @click="login()">login</button>
    </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import axios from "axios";

export default {
    name: "Home",
    methods: {
        testing() {
            this.$socket.client.emit("testing", "Test string");
        },
        login() {
            // console.log('loggin in')
            axios
                .get("https://127.0.0.1:5000/")
                .then((res) => {
                    console.log(res);
                })
                .catch((err) => {
                    console.log(err);
                })
        },
    },
};
</script>
