<!--Make Websocket connections from here-->
<!-- If not connected, prompt user for name -->
<template>
    <div>
        <h1>Room ID: {{ rid }}</h1>
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
            this.chatHistory.push(data)
        }
    },
    data: () => ({
        message: "",
        chatHistory: [],
    }),
    methods: {
        sendMessage() {
            console.log(this.message);
            this.$socket.client.emit("sendMessage", {roomID: 1337, msg: this.message}); // by who
            this.message = "";
        },
    },
    computed: {
        rid() {
            return this.$route.params.roomID;
        },
    },
};
</script>