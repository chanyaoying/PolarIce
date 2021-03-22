<!--Make Websocket connections from here-->
<!-- If not connected, prompt user for name -->
<template>
    <div>
        <div v-if="joined_nickname">
            <h1>Room ID: {{ roomID }}</h1>
            <br />

            <ul>
                <li v-for="(data, key) in chatHistory" :key="key">
                    {{ data }}
                </li>
            </ul>
            Send a message to the room: <br />
            <!--             
            <input type="text" placeholder="Enter message" v-model="message" />
            <button @click="sendMessage">Send Message</button>
            <button @click="leaveRoom">Leave Room</button> -->

            <b-input-group id="message" class="mt-3">
                <b-form-input
                    type="text"
                    v-model="message"
                    @keyup.enter="sendMessage"
                    placeholder="Enter message"
                ></b-form-input>
                <b-input-group-append>
                    <b-button @click="sendMessage" variant="dark"
                        >Send Message</b-button
                    >
                </b-input-group-append>
            </b-input-group>
            <br /><br />
            <h2>Current Players: {{ currentPlayers }}</h2>
            <br /><br />
            <b-button @click="leaveRoom" variant="primary">Leave Room</b-button>
        </div>

        <div v-else>
            <h1>Room ID: {{ roomID }}</h1>
            <br />
            Please enter your name to join the room: <br />

            <b-input-group id="name" class="mt-3">
                <b-form-input
                    type="text"
                    v-model="nickname"
                    @keyup.enter="joinRoom(nickname)"
                    placeholder="Your nickname"
                ></b-form-input>
                <b-input-group-append>
                    <b-button @click="joinRoom(nickname)" variant="dark"
                        >Enter</b-button
                    >
                </b-input-group-append>
            </b-input-group>
        </div>

        <b-button class="btn-lg" id="start" variant="success">Start</b-button>
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
            this.getCurrentPlayers();
        },
        join(data) {
            this.chatHistory.push(data);
            this.getCurrentPlayers();
        },
        leave(data) {
            this.chatHistory.push(data);
            this.getCurrentPlayers();
        },
        receiveMessage(data) {
            this.chatHistory.push(data);
        },
        receivePlayers(data) {
            this.currentPlayers = data;
        },
    },
    data: () => ({
        message: "",
        chatHistory: [],
        currentPlayers: [],
        nickname: "",
        joined_nickname: "",
    }),
    methods: {
        sendMessage() {
            this.$socket.client.emit("sendMessage", {
                roomID: this.roomID,
                nickname: this.joined_nickname,
                msg: this.message,
            }); // by who
            this.message = "";
        },
        joinRoom(nickname) {
            // socket: join room
            this.$socket.client.emit("join", {
                roomID: this.roomID,
                username: nickname,
            });
            console.log("you have joined the room!");
            // reset nickname, set joined_nickname
            this.nickname = "";
            this.joined_nickname = nickname;
        },
        leaveRoom() {
            this.$socket.client.emit("leave", {
                roomID: this.roomID,
                username: this.joined_nickname,
            });
            this.joined_nickname = "";
            this.chatHistory = [];
        },
        getCurrentPlayers() {
            // send request to the server asking for all players
            this.$socket.client.emit("getCurrentPlayers", {
                roomID: this.roomID,
            });
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
                    // room is not live
                    this.$router.push("/playGame");
                }
            })
            .catch((err) => {
                console.log("err :>> ", err);
            });
    },
    mounted() {
        
    },
};
</script>

<style scoped>
h1 {
    margin-top: 10px;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: bold;
}
#name {
    width: 400px;
    margin: auto;
}
#message {
    width: 400px;
    margin: auto;
}
#start {
    position: fixed;
    bottom: 15px;
    right: 15px;
}
</style>