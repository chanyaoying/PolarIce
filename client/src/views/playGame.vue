<!--Make Websocket connections from here-->
<!-- If not connected, prompt user for name -->
<template>
    <div>
        <h1>Room ID: {{ roomID }}</h1>
        <br />
        <ul>
            <li v-for="chat in chatHistory" :key="chat">
                {{ chat }}
            </li>
        </ul>
        <input type="text" placeholder="Enter message" v-model="message" />
        <button @click="sendMessage">Send Message</button>
    </div>
</template>

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
        sendMessage() {
            this.$socket.client.emit("sendMessage", {
                roomID: this.roomID,
                msg: this.message,
            }); // by who
            this.message = "";
        },
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
                    this.$router.push("/playGame");
                }
            })
            .catch((err) => {
                console.log("err :>> ", err);
            });
    },
};
</script>