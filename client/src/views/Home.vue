<template>
    <div class="home">
        <img src="../assets/PolarIcelogo.png"> <br>

        <h1 style="color: red">{{ errorMessage }}</h1>
        <button @click="login()">Login</button> <br />
        <input type="text" placeholder="Room ID" v-model="roomID" />
      <button @click="joinRoom">Join Room</button>
        <b-button>LOL</b-button>
    </div>
</template>

<style scoped>
    img{
        width:20%;
    }
</style>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import axios from "axios";

export default {
    name: "Home",
    data: () => ({
        roomID: "",
        errorMessage: "",
    }),
    methods: {
        joinRoom() {
            // check if room is live
            axios
                .get("http://127.0.0.1:5001/live?roomID=" + this.roomID)
                .then((res) => {
                    if (res.data.live) {
                        this.errorMessage = "";
                        this.$router.push("/playGame/" + this.roomID);
                    } else {
                        this.errorMessage = `${this.roomID} is not live. Try "testRoom".`;
                    }
                    this.roomID = "";
                })
                .catch((err) => {
                    console.log("err :>> ", err);
                });
        },
        login() {
            axios
                .get("https://127.0.0.1:5000/")
                .then((res) => {
                    console.log("we did it: ", res);
                })
                .catch((err) => {
                    try {
                        let status = err.response.status;
                        if (status == 400) {
                            console.log("Redirecting to login page.");
                            window.location.href =
                                "https://127.0.0.1:5000/login";
                        }
                    } catch (error) {
                        console.log("error :>> ", error);
                        console.log("err :>> ", err);
                    }
                });
        },
    },
};
</script>
