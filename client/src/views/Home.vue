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
            axios
                .get("https://127.0.0.1:5000/")
                .then((res) => {
                    console.log("we did it: ", res)
                })
                .catch((err) => {
                    try {
                        let status = err.response.status;
                        if (status == 400) {
                            console.log("Redirecting to login page.")
                            window.location.href = "https://127.0.0.1:5000/login";
                        }
                    } catch (error) {
                        console.log('error :>> ', error);
                        console.log('err :>> ', err);
                    }
                    
                });
        },
    },
};
</script>
