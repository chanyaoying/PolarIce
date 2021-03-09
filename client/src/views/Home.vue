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
                    if (res.data.code == 400) {
                        location.replace("https://127.0.0.1:5000/login");
                    } else {
                        console.log("you dubm bij :>> ", res.data.code);
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        },
    },
};
</script>
