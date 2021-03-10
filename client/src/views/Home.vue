<template>
    <div class="home">
        <button @click="testing">Test</button>
        <button @click="login()">Login</button>
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
                    if (res.data.code == 400) { // if not logged in
                        window.location.href = "https://127.0.0.1:5000/login"; // route to login endpoint
                    } else {
                        console.log("here", res.data.code);
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        },
    },
};
</script>
