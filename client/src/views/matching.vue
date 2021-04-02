<!--Make Websocket connections from here-->
<!-- If not connected, prompt user for name -->
<template>
    <div>
        <h1>Room ID: {{ roomID }}</h1><br>
        <b-container style="width:70%">
            <b-card>
                <h2>Your best friends are: </h2>



                <br>
            </b-card>
        </b-container>
    </div>
</template>

<style scoped>
    h1{
        margin-top: 10px;
        font-family: Arial, Helvetica, sans-serif;
        font-weight: bold;
    }
    h2{
        margin-top: 50px;
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }

</style>

<script>
import axios from "axios";

export default {
    name: "playGame",
    sockets: {
        connect(data) {
            console.log("Users: " + data);
        },
        disconnect(data) {
            console.log("Users: " + data);
        },
        join(data) {
            // receive from server
            console.log("data :>> ", data);
        },
        receiveMessage(data) {
            this.chatHistory.push(data);
        },
    },
    data: () => ({
        message: "",
        chatHistory: [],
    }),
    methods: {

    },
    computed: {
        roomID() {
            return this.$route.params.roomID;
        },
    },
    created() {
        // Check if room is live
        // While checking, the client will be briefly connected to the websocket before being redirected.
        // Huge security concern, but not within the scope of this course.
        // If we were to fix this, we would not use asynchronous checking.
        axios
            .get("http://127.0.0.1:5001/live?roomID=" + this.roomID)
            .then((res) => {
                if (!res.data.live) {
                    this.$router.push("/matching");
                }
            })
            .catch((err) => {
                console.log("err :>> ", err);
            });
    },
};
</script>