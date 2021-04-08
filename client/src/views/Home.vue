<template>
    <div class="home">

        <b-img :src="require('../assets/PolarIcelogo.png')"> </b-img><br>

        <h1 style="color: red">{{ errorMessage }}</h1>
        
        <b-button @click="login()" variant="dark">Login</b-button> <br/>

        <b-input-group id="join" class="mt-3">
            <b-form-input id="roomid" type="text" v-model="roomID" placeholder="PIN" ></b-form-input>
            <b-input-group-append>
            <b-button @click="joinRoom" >Join Room</b-button>
            </b-input-group-append>
        </b-input-group>

    </div>
</template>

<style scoped>
    img{
        width:20%;
        margin-top: 20px;
    }
    #join{
        width:400px;
        margin:auto;
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
                // .get(process.env.VUE_APP_app_endpoint)
                // .get("https://467fac702a80.ngrok.io") #replace with ngrok endpoint
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
                                // console.log("here" + process.env.VUE_APP_app_endpoint + "/login")
                                process.env.VUE_APP_app_endpoint + "/login";
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
