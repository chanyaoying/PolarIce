<!--Make Websocket connections from here-->
<!-- If not connected, prompt user for name -->
<template>
    <div>
        <div v-if="joined_nickname">
            Current Players: {{ currentPlayers }}
            <h1>Room ID: {{ roomID }}</h1>
            <br />
            <ul>
                <li v-for="(data, key) in chatHistory" :key="key">
                    {{ data }}
                </li>
            </ul>
            Send a message to the room: <br />
            <input type="text" placeholder="Enter message" v-model="message" />
            <button @click="sendMessage">Send Message</button>
            <button @click="leaveRoom">Leave Room</button>
        </div>

        <div v-else>
            <h1>Room ID: {{ roomID }}</h1>
            <br />
            Please enter your name to join the room: <br />
            <input type="text" placeholder="Your nickname" v-model="nickname" />
            <button @click="joinRoom(nickname)">Enter with Nickname</button>
        </div>
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
            this.chatHistory.push(data);
            this.getCurrentPlayers();
        },
        leave(data) {
            this.chatHistory.push(data)
            this.getCurrentPlayers();
        },
        receiveMessage(data) {
            this.chatHistory.push(data);
        },
        receivePlayers(data) {
            this.currentPlayers = data
        }
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
            this.$socket.client.emit('leave', {
                roomID: this.roomID,
                username: this.joined_nickname,
            });
            this.joined_nickname = ""
            this.chatHistory = [];
        },
        getCurrentPlayers() {
            // send request to the server asking for all players
            this.$socket.client.emit('getCurrentPlayers', {
                roomID: this.roomID,
            });
        }
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
    beforeDestroyed() {
        this.leaveRoom();
    },
};
</script>